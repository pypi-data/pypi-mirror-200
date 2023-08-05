import hashlib
import importlib
import inspect
import pickle as pkl
import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.schema import type_from_arrow_schema
from sarus_data_spec.config import ROUTING
from sarus_data_spec.dataspec_validator.typing import PEPKind
from sarus_data_spec.manager.asyncio.utils import async_iter
from sarus_data_spec.manager.ops.asyncio.base import (
    DatasetImplementation,
    DatasetStaticChecker,
    DataspecStaticChecker,
    ScalarImplementation,
)
from sarus_data_spec.schema import schema as schema_builder
from sarus_data_spec.transform import external, transform_id
import sarus_data_spec.manager.typing as smt
import sarus_data_spec.protobuf as sp
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st

from .protection_utils import (
    ExternalOpImplementation,
    extract_data_from_pe,
    pandas_merge_pe,
)


class ExternalScalarStaticChecker(DataspecStaticChecker):
    async def private_queries(self) -> t.List[st.PrivateQuery]:
        """Return the PrivateQueries summarizing DP characteristics."""
        implementation = external_implementation(self.dataspec)
        args, kwargs = external_arguments(self.dataspec)
        return await implementation.private_queries(*args, **kwargs)

    def is_dp(self) -> bool:
        """Checks if the transform is DP and compatible with the arguments."""
        op_implementation = external_implementation(self.dataspec)
        args, kwargs = external_arguments(self.dataspec)
        return op_implementation.is_dp(*args, **kwargs)

    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PEP arguments are PEP and aligned
            (i.e. same PEP token)
            - other dataspecs arguments are public
        """
        op_implementation = external_implementation(self.dataspec)
        args, kwargs = external_arguments(self.dataspec)

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None or not dp_implementation.is_dp(
            *args, **kwargs
        ):
            return False

        pep_args, non_pep_args = group_by_pep(
            dp_implementation, *args, **kwargs
        )

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return False

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in dp_implementation.allowed_pep_args:
            return False

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return False

        return True

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        op_implementation = external_implementation(self.dataspec)
        py_args, py_kwargs, ds_args_pos = serialized_external_arguments(
            self.dataspec
        )

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return None

        dp_transform_id = dp_implementation.transform_id
        assert dp_transform_id is not None

        return external(
            dp_transform_id,
            py_args=py_args,
            py_kwargs=py_kwargs,
            ds_args_pos=ds_args_pos,
        )


class ExternalDatasetStaticChecker(
    ExternalScalarStaticChecker, DatasetStaticChecker
):
    def __init__(self, dataset: st.Dataset):
        super().__init__(dataset)
        self.dataset = dataset

    def pep_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """Return the current dataspec's PEP token."""
        op_implementation = external_implementation(self.dataspec)
        transform_args, transform_kwargs = external_arguments(self.dataspec)

        if len(op_implementation.allowed_pep_args) == 0:
            return None

        pep_args, non_pep_args = group_by_pep(
            op_implementation, *transform_args, **transform_kwargs
        )

        pep_kind = op_implementation.pep_kind(
            *transform_args, **transform_kwargs
        )
        if pep_kind == PEPKind.NOT_PEP:
            return None

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return None

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in op_implementation.allowed_pep_args:
            return None

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return None

        # The result is PEP, now check if it's aligned with the input(s)
        input_token = pep_tokens[0]
        assert input_token is not None
        if pep_kind == PEPKind.TOKEN_PRESERVING:
            output_token = input_token
        else:
            h = hashlib.md5()
            h.update(input_token.encode("ascii"))
            h.update(self.dataspec.transform().protobuf().SerializeToString())
            output_token = h.hexdigest()

        return output_token

    async def schema(self) -> st.Schema:
        """Computes the schema of the dataspec.

        The schema is computed by computing the synthetic data value and
        converting the Pyarrow schema to a Sarus schema.q
        """
        syn_variant = self.dataset.variant(kind=st.ConstraintKind.SYNTHETIC)
        assert syn_variant is not None
        assert syn_variant.prototype() == sp.Dataset

        syn_dataset = t.cast(st.Dataset, syn_variant)
        arrow_iterator = await syn_dataset.async_to_arrow(batch_size=1)
        first_batch = await arrow_iterator.__anext__()
        schema = first_batch.schema

        schema_type = type_from_arrow_schema(schema)
        if self.dataset.is_pep() and not schema_type.has_protected_format():
            # The synthetic schema might not have the protection, we need to
            # add it in this case
            schema_type = sdt.protected_type(schema_type)

        return schema_builder(self.dataset, schema_type=schema_type)


class ExternalDatasetOp(DatasetImplementation):
    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        op_implementation = external_implementation(self.dataset)
        transform_args, transform_kwargs = external_arguments(self.dataset)

        data_args, data_kwargs, pe_candidates = await evaluate_arguments(
            *transform_args, **transform_kwargs
        )
        static_checker = ExternalScalarStaticChecker(self.dataset)
        if self.dataset.is_pep() or static_checker.is_dp():
            # If we reach this part then there should be only one input PE
            pe = next(iter(pe_candidates), None)
            if pe is None:
                raise ValueError(
                    "The dataset was infered PEP but has no input PE"
                )
            # For now, PE in external ops are only viewed as pd.DataFrames
            if not all([candidate.equals(pe) for candidate in pe_candidates]):
                raise ValueError(
                    "The dataset is PEP but has several differing"
                    " input PE values"
                )

        if static_checker.is_dp():
            # We also pass the PE for DP implementations
            data = await op_implementation.call(
                *data_args, **data_kwargs, pe=pe, dataspec=self.dataset
            )
        else:
            data = await op_implementation.call(*data_args, **data_kwargs)

        if self.dataset.is_pep():
            # We guarantee that the data.index is a reliable way to trace how
            # the rows were rearranged
            assert pe is not None
            pe = pe.loc[data.index]
        else:
            pe = None

        if isinstance(data, pd.DataFrame):
            table = pandas_merge_pe(data, pe)
            return async_iter(table.to_batches(max_chunksize=batch_size))

        else:
            raise TypeError(f"Cannot convert {type(data)} to Arrow batches.")


class ExternalScalarOp(ScalarImplementation):
    async def value(self) -> t.Any:
        op_implementation = external_implementation(self.scalar)
        transform_args, transform_kwargs = external_arguments(self.scalar)

        data_args, data_kwargs, pe_candidates = await evaluate_arguments(
            *transform_args, **transform_kwargs
        )

        static_checker = ExternalScalarStaticChecker(self.scalar)
        if static_checker.is_dp():
            # If we reach this part then there should be only one input PE
            pe = next(iter(pe_candidates), None)
            if pe is None:
                raise ValueError(
                    "The dataset was infered PEP but has no input PE"
                )
            # For now, PE in external ops are only viewed as pd.DataFrames
            if not all([candidate.equals(pe) for candidate in pe_candidates]):
                raise ValueError(
                    "The dataset is PEP but has several differing"
                    " input PE values"
                )
            # We also pass the PE for DP implementations
            data = await op_implementation.call(
                *data_args, **data_kwargs, pe=pe, dataspec=self.scalar
            )
        else:
            data = await op_implementation.call(*data_args, **data_kwargs)

        return data


def group_by_pep(
    op_implementation: smt.ExternalOpImplementation,
    *args: t.Any,
    **kwargs: t.Any,
) -> t.Tuple[t.Dict[str, st.DataSpec], t.Dict[str, st.DataSpec]]:
    """Get Dataspec arguments and split them between PEP and non PEP.

    This also identifies positional arguments by names based on the `call`
    signature.
    """
    # Add name to positional arguments to identify them by their names
    n_args = len(args)
    argument_names = list(
        inspect.signature(op_implementation.call).parameters.keys()
    )
    """
    Example :
    In [1]: def foo(a, b=3):
    ...:     return a+b
    ...:

    In [2]: list(inspect.signature(foo).parameters.keys())
    Out[2]: ['a', 'b']
    """
    for arg_name, arg_val in zip(argument_names[:n_args], args):
        # put all args in kwargs
        kwargs[arg_name] = arg_val

    # Keep only dataspec args and split PEP from non PEP
    dataspec_args = {
        arg_name: arg
        for arg_name, arg in kwargs.items()
        if isinstance(arg, st.DataSpec)
    }
    pep_args = {
        arg_name: arg
        for arg_name, arg in dataspec_args.items()
        if arg.is_pep()
    }
    non_pep_args = {
        arg_name: arg
        for arg_name, arg in dataspec_args.items()
        if arg_name not in pep_args
    }
    return pep_args, non_pep_args


def serialized_external_arguments(
    dataspec: st.DataSpec,
) -> t.Tuple[t.Dict[int, t.Any], t.Dict[str, t.Any], t.List[int]]:
    """Return the external arguments serialized in the protobuf."""
    transform = dataspec.transform()
    assert transform and transform.is_external()

    transform_spec = dataspec.transform().protobuf().spec
    external_args = pkl.loads(transform_spec.external.named_arguments)
    py_args = external_args["py_args"]
    py_kwargs = external_args["py_kwargs"]
    ds_args_pos = external_args["ds_args_pos"]
    return py_args, py_kwargs, ds_args_pos


def external_arguments(
    dataspec: st.DataSpec,
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
    """Return all the external arguments.

    This returns arguments serialized in the protobufs as well as Dataspecs.
    """
    py_args, py_kwargs, ds_args_pos = serialized_external_arguments(dataspec)

    ds_args, ds_kwargs = dataspec.parents()
    pos_values = {pos: val for pos, val in zip(ds_args_pos, ds_args)}
    kwargs = {**py_kwargs, **ds_kwargs}
    pos_args = {**pos_values, **py_args}
    args = [pos_args[i] for i in range(len(pos_args))]
    return args, kwargs


def external_implementation(
    dataspec: st.DataSpec,
) -> smt.ExternalOpImplementation:
    """Return the implementation of an external op from a DataSpec.

    The mapping is done by the config file.
    """
    transform = dataspec.transform()
    assert transform and transform.is_external()
    library, op_name = transform_id(transform).split(".")
    if op_name not in ROUTING["external"][library]:
        raise NotImplementedError(
            f"Routing: {op_name} not in {list(ROUTING['external'][library].keys())}"  # noqa: E501
        )

    implementation_name = ROUTING["external"][library][op_name]
    module = importlib.import_module(
        f"sarus_data_spec.manager.ops.asyncio.processor.external.{library}"
    )
    op_implementation = getattr(module, implementation_name)

    if not isinstance(op_implementation, type):
        op_implementation = type(
            implementation_name,
            (ExternalOpImplementation,),
            {
                "call": staticmethod(op_implementation),
                "transform_id": transform_id,
            },
        )

    return t.cast(smt.ExternalOpImplementation, op_implementation(dataspec))


async def evaluate_arguments(
    *args: t.Any, **kwargs: t.Any
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any], t.List[t.Any]]:
    """Evaluate sarus dataspecs and extract the PE.

    Compute the value of Dataspec arguments. Extract all the protections and
    return them in a list.
    """
    data_pe_args = [await extract_data_from_pe(arg) for arg in args]
    data_args = [data for data, _ in data_pe_args]
    pe_args = [pe for _, pe in data_pe_args]

    data_pe_kwargs = {
        name: await extract_data_from_pe(arg) for name, arg in kwargs.items()
    }
    data_kwargs = {name: data for name, (data, _) in data_pe_kwargs.items()}
    pe_kwargs = [pe for _, pe in data_pe_kwargs.values()]

    pe_candidates = list(filter(lambda x: x is not None, pe_args + pe_kwargs))

    return data_args, data_kwargs, pe_candidates
