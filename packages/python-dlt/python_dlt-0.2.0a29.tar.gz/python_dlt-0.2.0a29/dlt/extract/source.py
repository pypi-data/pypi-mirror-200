import contextlib
from copy import copy, deepcopy
import makefun
import inspect
from collections.abc import Mapping as C_Mapping
from typing import AsyncIterable, AsyncIterator, ClassVar, Callable, Dict, Iterable, Iterator, List, Sequence, Union, cast, Any
from dlt.common.configuration.resolve import inject_section
from dlt.common.configuration.specs import known_sections
from dlt.common.configuration.specs.config_section_context import ConfigSectionContext


from dlt.common.schema import Schema
from dlt.common.schema.utils import new_table
from dlt.common.schema.typing import TColumnSchema, TPartialTableSchema, TTableSchemaColumns, TWriteDisposition
from dlt.common.typing import AnyFun, TDataItem, TDataItems, NoneType, TFun
from dlt.common.configuration.container import Container
from dlt.common.pipeline import PipelineContext, SupportsPipelineRun
from dlt.common.utils import flatten_list_or_items, get_callable_name

from dlt.extract.typing import DataItemWithMeta, ItemTransformFunc, TableNameMeta, TFunHintTemplate, TTableHintTemplate, TTableSchemaTemplate, FilterItem, MapItem, YieldMapItem
from dlt.extract.pipe import Pipe, ManagedPipeIterator
from dlt.extract.exceptions import (
    InvalidTransformerDataTypeGeneratorFunctionRequired, InvalidParentResourceDataType, InvalidParentResourceIsAFunction, InvalidResourceDataType, InvalidResourceDataTypeFunctionNotAGenerator, InvalidResourceDataTypeIsNone, InvalidTransformerGeneratorFunction,
    DataItemRequiredForDynamicTableHints, InconsistentTableTemplate, InvalidResourceDataTypeAsync, InvalidResourceDataTypeBasic,
    InvalidResourceDataTypeMultiplePipes, ParametrizedResourceUnbound, ResourceNameMissing, ResourceNotATransformer, ResourcesNotFoundError, SourceExhausted, TableNameMissing, DeletingResourcesNotSupported)


def with_table_name(item: TDataItems, table_name: str) -> DataItemWithMeta:
    """Marks `item` to be dispatched to table `table_name` when yielded from resource function."""
    return DataItemWithMeta(TableNameMeta(table_name), item)


class DltResourceSchema:
    def __init__(self, name: str, table_schema_template: TTableSchemaTemplate = None):
        self.__qualname__ = self.__name__ = self.name = name
        self._table_name_hint_fun: TFunHintTemplate[str] = None
        self._table_has_other_dynamic_hints: bool = False
        self._table_schema_template: TTableSchemaTemplate = None
        self._table_schema: TPartialTableSchema = None
        if table_schema_template:
            self.set_template(table_schema_template)

    @property
    def table_name(self) -> str:
        """Get table name to which resource loads data. Raises in case of table names derived from data."""
        if self._table_name_hint_fun:
            raise DataItemRequiredForDynamicTableHints(self.name)
        return self._table_schema_template["name"] if self._table_schema_template else self.name  # type: ignore

    def table_schema(self, item: TDataItem =  None) -> TPartialTableSchema:
        """Computes the table schema based on hints and column definitions passed during resource creation. `item` parameter is used to resolve table hints based on data"""
        if not self._table_schema_template:
            # if table template is not present, generate partial table from name
            if not self._table_schema:
                self._table_schema = new_table(self.name)
            return self._table_schema

        def _resolve_hint(hint: TTableHintTemplate[Any]) -> Any:
            if callable(hint):
                return hint(item)
            else:
                return hint

        # if table template present and has dynamic hints, the data item must be provided
        if self._table_name_hint_fun:
            if item is None:
                raise DataItemRequiredForDynamicTableHints(self.name)
            else:
                return cast(TPartialTableSchema, {k: _resolve_hint(v) for k, v in self._table_schema_template.items()})
        else:
            return cast(TPartialTableSchema, self._table_schema_template)

    def apply_hints(
        self,
        table_name: TTableHintTemplate[str] = None,
        parent_table_name: TTableHintTemplate[str] = None,
        write_disposition: TTableHintTemplate[TWriteDisposition] = None,
        columns: TTableHintTemplate[TTableSchemaColumns] = None,
    ) -> None:
        """Allows to create or modify existing table schema by setting provided hints. Accepts hints based on data."""
        t = None
        if not self._table_schema_template:
            # if there's no template yet, create and set new one
            t = self.new_table_template(table_name, parent_table_name, write_disposition, columns)
        else:
            # set single hints
            t = deepcopy(self._table_schema_template)
            if table_name:
                t["name"] = table_name
            if parent_table_name:
                t["parent"] = parent_table_name
            if write_disposition:
                t["write_disposition"] = write_disposition
            if columns:
                t["columns"] = columns
        self.set_template(t)

    def set_template(self, table_schema_template: TTableSchemaTemplate) -> None:
        # if "name" is callable in the template then the table schema requires actual data item to be inferred
        name_hint = table_schema_template["name"]
        if callable(name_hint):
            self._table_name_hint_fun = name_hint
        else:
            self._table_name_hint_fun = None
        # check if any other hints in the table template should be inferred from data
        self._table_has_other_dynamic_hints = any(callable(v) for k, v in table_schema_template.items() if k != "name")
        self._table_schema_template = table_schema_template

    @staticmethod
    def new_table_template(
        table_name: TTableHintTemplate[str],
        parent_table_name: TTableHintTemplate[str] = None,
        write_disposition: TTableHintTemplate[TWriteDisposition] = None,
        columns: TTableHintTemplate[TTableSchemaColumns] = None,
        ) -> TTableSchemaTemplate:
        if not table_name:
            raise TableNameMissing()
        # create a table schema template where hints can be functions taking TDataItem
        if isinstance(columns, C_Mapping):
            # new_table accepts a sequence
            column_list: List[TColumnSchema] = []
            for name, column in columns.items():
                column["name"] = name
                column_list.append(column)
            columns = column_list  # type: ignore

        new_template: TTableSchemaTemplate = new_table(table_name, parent_table_name, write_disposition=write_disposition, columns=columns)  # type: ignore
        # if any of the hints is a function then name must be as well
        if any(callable(v) for k, v in new_template.items() if k != "name") and not callable(table_name):
            raise InconsistentTableTemplate(f"Table name {table_name} must be a function if any other table hint is a function")
        return new_template


class DltResource(Iterable[TDataItem], DltResourceSchema):

    Empty: ClassVar["DltResource"] = None

    def __init__(self, pipe: Pipe, table_schema_template: TTableSchemaTemplate, selected: bool):
        # TODO: allow resource to take name independent from pipe name
        self.name = pipe.name
        self.selected = selected
        self._pipe = pipe
        super().__init__(self.name, table_schema_template)

    @classmethod
    def from_data(cls, data: Any, name: str = None, table_schema_template: TTableSchemaTemplate = None, selected: bool = True, depends_on: Union["DltResource", Pipe] = None) -> "DltResource":

        if data is None:
            raise InvalidResourceDataTypeIsNone(name, data, NoneType)  # type: ignore

        if isinstance(data, DltResource):
            return data

        if isinstance(data, Pipe):
            return cls(data, table_schema_template, selected)

        if callable(data):
            name = name or get_callable_name(data)

        # if generator, take name from it
        if inspect.isgenerator(data):
            name = name or get_callable_name(data)  # type: ignore

        # name is mandatory
        if not name:
            raise ResourceNameMissing()

        # several iterable types are not allowed and must be excluded right away
        if isinstance(data, (AsyncIterator, AsyncIterable)):
            raise InvalidResourceDataTypeAsync(name, data, type(data))
        if isinstance(data, (str, dict)):
            raise InvalidResourceDataTypeBasic(name, data, type(data))

        # check if depends_on is a valid resource
        parent_pipe: Pipe = None
        if depends_on is not None:
            DltResource._ensure_valid_transformer_resource(name, data)
            parent_pipe = DltResource._get_parent_pipe(name, depends_on)

        # create resource from iterator, iterable or generator function
        if isinstance(data, (Iterable, Iterator)) or callable(data):
            pipe = Pipe.from_data(name, data, parent=parent_pipe)
            return cls(pipe, table_schema_template, selected)
        else:
            # some other data type that is not supported
            raise InvalidResourceDataType(name, data, type(data), f"The data type is {type(data).__name__}")

    @property
    def is_transformer(self) -> bool:
        """Checks if the resource is a transformer that takes data from another resource"""
        return self._pipe.has_parent

    @property
    def is_parametrized(self) -> bool:
        """Checks if resource has unbound parameters"""
        try:
            self._pipe.ensure_gen_bound()
            return False
        except (TypeError, ParametrizedResourceUnbound):
            return True

    def pipe_data_from(self, data_from: Union["DltResource", Pipe]) -> None:
        """Replaces the parent in the transformer resource pipe from which the data is piped."""
        if self.is_transformer:
            DltResource._ensure_valid_transformer_resource(self.name, self._pipe.gen)
        else:
            raise ResourceNotATransformer(self.name, "Cannot pipe data into resource that is not a transformer.")
        parent_pipe = self._get_parent_pipe(self.name, data_from)
        self._pipe.parent = parent_pipe

    def add_pipe(self, data: Any) -> None:
        """Creates additional pipe for the resource from the specified data"""
        # TODO: (1) self resource cannot be a transformer (2) if data is resource both self must and it must be selected/unselected + cannot be tranformer
        raise InvalidResourceDataTypeMultiplePipes(self.name, data, type(data))

    def select_tables(self, *table_names: Iterable[str]) -> "DltResource":
        """For resources that dynamically dispatch data to several tables allows to select tables that will receive data, effectively filtering out other data items.

            Both `with_table_name` marker and data-based (function) table name hints are supported.
        """
        def _filter(item: TDataItem, meta: Any = None) -> bool:
            is_in_meta = isinstance(meta, TableNameMeta) and meta.table_name in table_names
            is_in_dyn = self._table_name_hint_fun and self._table_name_hint_fun(item) in table_names
            return is_in_meta or is_in_dyn

        # add filtering function at the end of pipe
        self.add_filter(_filter)
        return self

    def bind(self, *args: Any, **kwargs: Any) -> "DltResource":
        """Binds the parametrized resource to passed arguments. Modifies resource pipe in place. Does not evaluate generators or iterators."""
        gen = self._wrap_gen_step(*args, **kwargs)
        if isinstance(gen, DltResource):
            # replace resource in place
            old_pipe = self._pipe
            self.__dict__.clear()
            self.__dict__.update(gen.__dict__)
            # keep old pipe instance
            self._pipe = old_pipe
            self._pipe.__dict__.clear()
            # write props from new pipe instance
            self._pipe.__dict__.update(gen._pipe.__dict__)
        elif isinstance(gen, Pipe):
            # just replace pipe
            self._pipe.__dict__.clear()
            # write props from new pipe instance
            self._pipe.__dict__.update(gen.__dict__)
        else:
            # replace gen element
            self._pipe.replace_gen(gen)
        return self

    def add_map(self, item_map: ItemTransformFunc[TDataItem], insert_at: int = None) -> "DltResource":  # noqa: A003
        """Adds mapping function defined in `item_map` to the resource pipe at position `inserted_at`

        `item_map` receives single data items, `dlt` will enumerate any lists of data items automatically

        Args:
            item_map (ItemTransformFunc[TDataItem]): A function taking a single data item and optional meta argument. Returns transformed data item.
            insert_at (int, optional): At which step in pipe to insert the mapping. Defaults to None which inserts after last step

        Returns:
            "DltResource": returns self
        """
        if insert_at is None:
            self._pipe.append_step(MapItem(item_map))
        else:
            self._pipe.insert_step(MapItem(item_map), insert_at)
        return self

    def add_yield_map(self, item_map: ItemTransformFunc[Iterator[TDataItem]], insert_at: int = None) -> "DltResource":  # noqa: A003
        """Adds generating function defined in `item_map` to the resource pipe at position `inserted_at`

        `item_map` receives single data items, `dlt` will enumerate any lists of data items automatically. It may yield 0 or more data items and be used to
        ie. pivot an item into sequence of rows.

        Args:
            item_map (ItemTransformFunc[Iterator[TDataItem]]): A function taking a single data item and optional meta argument. Yields 0 or more data items.
            insert_at (int, optional): At which step in pipe to insert the generator. Defaults to None which inserts after last step

        Returns:
            "DltResource": returns self
        """
        if insert_at is None:
            self._pipe.append_step(YieldMapItem(item_map))
        else:
            self._pipe.insert_step(YieldMapItem(item_map), insert_at)
        return self

    def add_filter(self, item_filter: ItemTransformFunc[bool], insert_at: int = None) -> "DltResource":  # noqa: A003
        """Adds filter defined in `item_filter` to the resource pipe at position `inserted_at`

        `item_filter` receives single data items, `dlt` will enumerate any lists of data items automatically

        Args:
            item_filter (ItemTransformFunc[bool]): A function taking a single data item and optional meta argument. Returns bool. If True, item is kept
            insert_at (int, optional): At which step in pipe to insert the filter. Defaults to None which inserts after last step
        Returns:
            "DltResource": returns self
        """
        if insert_at is None:
            self._pipe.append_step(FilterItem(item_filter))
        else:
            self._pipe.insert_step(FilterItem(item_filter), insert_at)
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> "DltResource":
        """Binds the parametrized resources to passed arguments. Creates and returns a bound resource. Generators and iterators are not evaluated."""
        gen = self._wrap_gen_step(*args, **kwargs)
        if isinstance(gen, DltResource):
            return gen
        else:
            r = DltResource.from_data(gen, self.name, self._table_schema_template, self.selected, self._pipe.parent)
            if isinstance(gen, Pipe):
                return r
            # clone existing pipe
            r._pipe = self._pipe._clone(keep_pipe_id=False)
            # replace with bound generator
            r._pipe.replace_gen(gen)
            return r

    def _wrap_gen_step(self, *args: Any, **kwargs: Any) -> Any:
        """Finds and wraps with `args` + `kwargs` the callable generating step in the resource pipe."""
        head = self._pipe.gen
        _data: Any = None
        if not callable(head):
            # just provoke a call to raise default exception
            head()  # type: ignore
            raise AssertionError()

        # simulate the call to the underlying callable
        skip_items_arg = 1 if self.is_transformer else 0  # skip the data item argument for transformers
        sig = inspect.signature(head)
        no_item_sig = sig.replace(parameters=list(sig.parameters.values())[skip_items_arg:])
        try:
            no_item_sig.bind(*args, **kwargs)
        except TypeError as v_ex:
            raise TypeError(f"{get_callable_name(head)}(): " + str(v_ex))

        # create wrappers with partial
        if self.is_transformer:
            # also provide optional meta so pipe does not need to update arguments

            def _tx_partial(item: TDataItems, *, meta: Any = None) -> Any:
                # print(f"ITEM:{item},{args}{kwargs}")
                if "meta" in kwargs:
                    kwargs["meta"] = meta
                return head(item, *args, **kwargs)  # type: ignore

            _data = makefun.wraps(head, new_sig=inspect.signature(_tx_partial))(_tx_partial)
        else:
            if inspect.isgeneratorfunction(inspect.unwrap(head)) or inspect.isgenerator(head):
                # always wrap generators and generator functions. evaluate only at runtime!

                def _partial() -> Any:
                    return head(*args, **kwargs)  # type: ignore

                _data = makefun.wraps(head, new_sig=inspect.signature(_partial))(_partial)
            else:
                # call regular function to check what is inside
                _data = head(*args, **kwargs)
                # accept if resource is returned
                if not isinstance(_data, (DltResource, Pipe)):
                    raise InvalidResourceDataTypeFunctionNotAGenerator(self.name, head, type(head))

        return _data

    def __or__(self, transform: Union["DltResource", AnyFun]) -> "DltResource":
        """Allows to pipe data from across resources and transform functions with | operator"""
        # print(f"{resource.name} | {self.name} -> {resource.name}[{resource.is_transformer}]")
        if isinstance(transform, DltResource):
            transform.pipe_data_from(self)
            # return transformed resource for chaining
            return transform
        else:
            # map or yield map
            if inspect.isgeneratorfunction(inspect.unwrap(transform)):
                return self.add_yield_map(transform)
            else:
                return self.add_map(transform)

    def __iter__(self) -> Iterator[TDataItem]:
        return flatten_list_or_items(map(lambda item: item.item, ManagedPipeIterator.from_pipe(self._pipe)))

    def __str__(self) -> str:
        info = f"DltResource {self.name}:"
        if self.is_transformer:
            info += f"\nThis resource is a transformer and takes data items from {self._pipe.parent.name}"
        else:
            if self._pipe.is_data_bound:
                if self.is_parametrized:
                    head_sig = inspect.signature(self._pipe.gen)  # type: ignore
                    info += f"\nThis resource is parametrized and takes the following arguments {head_sig}. You must call this resource before loading."
                else:
                    info += "\nIf you want to see the data items in the resource you must iterate it or convert to list ie. list(resource). Note that, like any iterator, you can iterate the resource only once."
            else:
                info += "\nThis resource is not bound to the data"
        info += f"\nInstance: info: (data pipe id:{self._pipe._pipe_id}) at {id(self)}"
        return info

    @staticmethod
    def _ensure_valid_transformer_resource(name: str, data: Any) -> None:
        # resource must be a callable with single argument
        if callable(data):
            valid_code = DltResource.validate_transformer_generator_function(data)
            if valid_code != 0:
                raise InvalidTransformerGeneratorFunction(name, get_callable_name(data), inspect.signature(data), valid_code)
        else:
            raise InvalidTransformerDataTypeGeneratorFunctionRequired(name, data, type(data))

    @staticmethod
    def _get_parent_pipe(name: str, data_from: Union["DltResource", Pipe]) -> Pipe:
        # parent resource
        if isinstance(data_from, Pipe):
            return data_from
        elif isinstance(data_from, DltResource):
            return data_from._pipe
        else:
            # if this is generator function provide nicer exception
            if callable(data_from):
                raise InvalidParentResourceIsAFunction(name, get_callable_name(data_from))
            else:
                raise InvalidParentResourceDataType(name, data_from, type(data_from))

    @staticmethod
    def validate_transformer_generator_function(f: AnyFun) -> int:
        sig = inspect.signature(f)
        if len(sig.parameters) == 0:
            return 1
        # transformer may take only one positional only argument
        pos_only_len = sum(1 for p in sig.parameters.values() if p.kind == p.POSITIONAL_ONLY)
        if pos_only_len > 1:
            return 2
        first_ar = next(iter(sig.parameters.values()))
        # and pos only must be first
        if pos_only_len == 1 and first_ar.kind != first_ar.POSITIONAL_ONLY:
            return 2
        # first arg must be positional or kw_pos
        if first_ar.kind not in (first_ar.POSITIONAL_ONLY, first_ar.POSITIONAL_OR_KEYWORD):
            return 3
        return 0


# produce Empty resource singleton
DltResource.Empty = DltResource(Pipe(None), None, False)
TUnboundDltResource = Callable[[], DltResource]


class DltResourceDict(Dict[str, DltResource]):
    def __init__(self, source_name: str) -> None:
        super().__init__()
        self.source_name = source_name
        self._recently_added: List[DltResource] = []

    @property
    def selected(self) -> Dict[str, DltResource]:
        return {k:v for k,v in self.items() if v.selected}

    @property
    def pipes(self) -> List[Pipe]:
        # TODO: many resources may share the same pipe so return ordered set
        return [r._pipe for r in self.values()]

    @property
    def selected_pipes(self) -> Sequence[Pipe]:
        # TODO: many resources may share the same pipe so return ordered set
        return [r._pipe for r in self.values() if r.selected]

    def select(self, *resource_names: str) -> Dict[str, DltResource]:
        # checks if keys are present
        for name in resource_names:
            if name not in self:
                # if any key is missing, display the full info
                raise ResourcesNotFoundError(self.source_name, set(self.keys()), set(resource_names))
        # set the selected flags
        for resource in self.values():
            self[resource.name].selected = resource.name in resource_names
        return self.selected

    def find_by_pipe(self, pipe: Pipe) -> DltResource:
        # TODO: many resources may share the same pipe so return a list and also filter the resources by self._enabled_resource_names
        # identify pipes by _pipe_id
        return next(r for r in self.values() if r._pipe._pipe_id is pipe._pipe_id)

    def clone_new_pipes(self) -> None:
        cloned_pipes = ManagedPipeIterator.clone_pipes([r._pipe for r in self.values() if r in self._recently_added])
        # replace pipes in resources, the cloned_pipes preserve parent connections
        for cloned in cloned_pipes:
            self.find_by_pipe(cloned)._pipe = cloned
        self._recently_added.clear()

    def __setitem__(self, resource_name: str, resource: DltResource) -> None:
        # make shallow copy of the resource
        resource = copy(resource)
        # now set it in dict
        self._recently_added.append(resource)
        return super().__setitem__(resource_name, resource)

    def __delitem__(self, resource_name: str) -> None:
        raise DeletingResourcesNotSupported(self.source_name, resource_name)


class DltSource(Iterable[TDataItem]):
    """Groups several `dlt resources` under a single schema and allows to perform operations on them.

    ### Summary
    The instance of this class is created whenever you call the `dlt.source` decorated function. It automates several functions for you:
    * You can pass this instance to `dlt` `run` method in order to load all data present in the `dlt resources`.
    * You can select and deselect resources that you want to load via `with_resources` method
    * You can access the resources (which are `DltResource` instances) as source attributes
    * It implements `Iterable` interface so you can get all the data from the resources yourself and without dlt pipeline present.
    * You can get the `schema` for the source and all the resources within it.
    * You can use a `run` method to load the data with a default instance of dlt pipeline.
    """
    def __init__(self, name: str, section: str, schema: Schema, resources: Sequence[DltResource] = None) -> None:
        self.name = name
        self.section = section
        self.exhausted = False
        """Tells if iterator associated with a source is exhausted"""
        self._schema = schema
        self._resources: DltResourceDict = DltResourceDict(self.name)
        if resources:
            for resource in resources:
                self._add_resource(resource.name, resource)
            self._resources.clone_new_pipes()

    @classmethod
    def from_data(cls, name: str, section: str, schema: Schema, data: Any) -> "DltSource":
        """Converts any `data` supported by `dlt` `run` method into `dlt source` with a name `section`.`name` and `schema` schema."""
        # creates source from various forms of data
        if isinstance(data, DltSource):
            return data

        # in case of sequence, enumerate items and convert them into resources
        if isinstance(data, Sequence):
            resources = [DltResource.from_data(i) for i in data]
        else:
            resources = [DltResource.from_data(data)]

        return cls(name, section, schema, resources)


    @property
    def resources(self) -> DltResourceDict:
        """A dictionary of all resources present in the source, where the key is a resource name."""
        return self._resources

    @property
    def selected_resources(self) -> Dict[str, DltResource]:
        """A dictionary of all the resources that are selected to be loaded."""
        return self._resources.selected

    @property
    def schema(self) -> Schema:
        return self._schema

    @schema.setter
    def schema(self, value: Schema) -> None:
        self._schema = value

    def discover_schema(self) -> Schema:
        # extract tables from all resources and update internal schema
        for r in self.selected_resources.values():
            # names must be normalized here
            with contextlib.suppress(DataItemRequiredForDynamicTableHints):
                partial_table = self._schema.normalize_table_identifiers(r.table_schema())
                self._schema.update_schema(partial_table)
        return self._schema

    def with_resources(self, *resource_names: str) -> "DltSource":
        """A convenience method to select one of more resources to be loaded. Returns a source with the specified resources selected."""
        self._resources.select(*resource_names)
        return self

    @property
    def run(self) -> SupportsPipelineRun:
        """A convenience method that will call `run` run on the currently active `dlt` pipeline. If pipeline instance is not found, one with default settings will be created."""
        self_run: SupportsPipelineRun = makefun.partial(Container()[PipelineContext].pipeline().run, *(), data=self)
        return self_run

    def _add_resource(self, name: str, resource: DltResource) -> None:
        if self.exhausted:
            raise SourceExhausted(self.name)

        if name in self._resources:
            # for resources with the same name try to add the resource as an another pipe
            self._resources[name].add_pipe(resource)
        else:
            self._resources[name] = resource
            # remember that resource got cloned when set into dict
            super().__setattr__(name, self._resources[name])

    def __getattr__(self, resource_name: str) -> DltResource:
        return self._resources[resource_name]

    def __setattr__(self, name: str, value: Any) -> None:
        if isinstance(value, DltResource):
            # TODO: refactor adding resources. 1. resource dict should be read only 2. we should correct the parent pipes after cloning 3. allow replacing existing resources
            self._add_resource(name, value)
        else:
            super().__setattr__(name, value)

    def __iter__(self) -> Iterator[TDataItem]:
        with inject_section(ConfigSectionContext(sections=(known_sections.SOURCES, self.section, self.name))):
            # evaluate the pipes in the section context
            pipe_iterator: ManagedPipeIterator = ManagedPipeIterator.from_pipes(self._resources.selected_pipes)  # type: ignore
        # keep same context during evaluation
        context = inject_section(ConfigSectionContext(sections=(known_sections.SOURCES, self.section, self.name)))
        pipe_iterator.set_context_manager(context)
        _iter = map(lambda item: item.item, pipe_iterator)
        self.exhausted = True
        return flatten_list_or_items(_iter)

    def __str__(self) -> str:
        info = f"DltSource {self.name} section {self.section} contains {len(self.resources)} resource(s) of which {len(self.selected_resources)} are selected"
        for r in self.resources.values():
            selected_info = "selected" if r.selected else "not selected"
            if r.is_transformer:
                info += f"\ntransformer {r.name} is {selected_info} and takes data from {r._pipe.parent.name}"
            else:
                info += f"\nresource {r.name} is {selected_info}"
        if self.exhausted:
            info += "\nSource is already iterated and cannot be used again ie. to display or load data."
        else:
            info += "\nIf you want to see the data items in this source you must iterate it or convert to list ie. list(source)."
        info += " Note that, like any iterator, you can iterate the source only once."
        info += f"\ninstance id: {id(self)}"
        return info
