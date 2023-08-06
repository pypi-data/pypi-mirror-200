"""Build CQL queries from Pydantic models."""
import datetime
import inspect
import typing
from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

import caseswitcher
import pydantic
from cassandra.cluster import Session
from cassandra.query import PreparedStatement, UNSET_VALUE
from pydantic import BaseModel
from pydantic.generics import GenericModel

NoneType = type(None)  # `types.NoneType` is not compatible python <= 3.9.
ModelType = TypeVar("ModelType", bound=BaseModel)


class PaginatedResult(GenericModel, Generic[ModelType]):
    """Results and paging state of a paged result."""

    results: list[ModelType]
    paging_state: Optional[bytes] = None


class TableMetadata(BaseModel):
    """Stores data about a Cassandra table."""

    partition_keys: list[str]
    clustering_keys: Optional[list[str]] = None
    index: Optional[list[str]] = None


# noinspection SqlNoDataSourceInspection
class QueryBuilder(Generic[ModelType]):
    """Class to build CQL queries from Pydantic models."""

    def __init__(
        self,
        session: Session,
        keyspace: str,
        model_type: Type[ModelType],
        metadata: TableMetadata,
    ) -> None:
        """Init an instance the QueryBuilder class.

        :param session: Cassandra driver session.
        :param keyspace: Keyspace of the tables.
        :param model_type: Type of model this instance will manage.
        :param metadata: Metadata about this table.
        """
        self._session = session
        self._keyspace = keyspace or session.keyspace
        self._model_type = model_type
        self._metadata = metadata
        self._keys = metadata.partition_keys + (metadata.clustering_keys or [])
        self._tablename = caseswitcher.to_snake(model_type.__name__)
        self._indent = " " * 2
        self._find_one_statement: Optional[PreparedStatement] = None
        self._insert_statement: Optional[PreparedStatement] = None
        self._upsert_statement: Optional[PreparedStatement] = None
        self._update_statement: Optional[PreparedStatement] = None
        self._delete_statement: Optional[PreparedStatement] = None
        self._find_many_statements: dict[str, PreparedStatement] = {}
        self._cql_set_fields = {
            k: cql_type
            for k, v in self._model_type.__fields__.items()
            if "SET" in (cql_type := _py_type_to_cql(v.annotation))
        }

    def sync(self) -> None:
        """Create this table if it doesn't exist."""
        for query in self._get_create_table_queries():
            self._session.execute(query=query)

    async def find_one(self, keys: dict[str, Any]) -> Optional[ModelType]:
        """Get one record mapped to the appropriate model.

        :param keys: The key of the record to retrieve.
        :return: A model representing the record if one is found.
        """
        self._find_one_statement = self._session.prepare(
            self._get_find_query(self._keys)
        )
        # noinspection PyAttributeOutsideInit
        self.__dict__["find_one"] = self._find_one  # type: ignore
        return await self._find_one(keys)

    async def find_many(
        self,
        where: Optional[dict[str, Any]] = None,
        page_size: Optional[int] = None,
        paging_state: Optional[bytes] = None,
    ) -> PaginatedResult[ModelType]:
        """Get many records mapped to the appropriate model.

        :param where: Columns to filter on.
        :param page_size: Number of records to get.
        :param paging_state: State of pagination.
        :return: A model representing the record if one is found.
        """
        # 5000 is cassandra-driver default.
        page_size = 5000 if page_size is None else page_size
        where = where if where is not None else {}
        # Determine which columns will be `? =` vs `? CONTAINS`.
        contains_columns = [
            k
            for k, v in where.items()
            if self._cql_set_fields.get(k) and not isinstance(v, list)
        ]
        contains_columns.sort()
        filter_columns = [key for key in where if key not in contains_columns]
        filter_columns.sort()
        # Create unique string to cache this statement once made.
        filter_signature = ".".join(filter_columns) + ".." + ".".join(contains_columns)
        # Get or create the prepared statement.
        query = self._find_many_statements.get(filter_signature)
        if query is None:
            query = self._session.prepare(
                self._get_find_query(filter_columns, contains_columns)
            )
        # Get values with pagination.
        self._session.default_fetch_size = page_size
        values = [where[c] for c in filter_columns + contains_columns]
        if paging_state is not None:
            results = self._session.execute(query, values, paging_state=paging_state)
        else:
            results = self._session.execute(query, values)
        models = []
        for i, row in enumerate(results):
            # noinspection PyProtectedMember
            models.append(self._deserialize(row))
            if i == page_size - 1:
                break
        return PaginatedResult(results=models, paging_state=results.paging_state)

    async def insert(self, model: ModelType) -> None:
        """Insert a record from a model.

        :param model: Model representing row to insert.
        :return: None.
        """
        self._insert_statement = self._session.prepare(self._get_insert_query())
        # noinspection PyAttributeOutsideInit
        self.__dict__["insert"] = self._insert  # type: ignore
        return await self._insert(model)

    async def upsert(self, model: ModelType) -> None:
        """Upsert a record from a model.

        :param model: Model representing row to upsert.
        :return: None.
        """
        self._upsert_statement = self._session.prepare(self._get_upsert_query())
        # noinspection PyAttributeOutsideInit
        self.__dict__["upsert"] = self._upsert  # type: ignore
        return await self._upsert(model)

    async def update(self, model: ModelType) -> None:
        """Update a record from a model.

        :param model: Model representing row to update.
        :return: None.
        """
        self._update_statement = self._session.prepare(self._get_update_query())
        # noinspection PyAttributeOutsideInit
        self.__dict__["update"] = self._update  # type: ignore
        return await self._update(model)

    async def delete(self, keys: dict[str, Any]) -> None:
        """Delete a record from a model.

        :param keys: Keys of the record to delete.
        :return: None.
        """
        self._delete_statement = self._session.prepare(self._get_delete_query())
        # noinspection PyAttributeOutsideInit
        self.__dict__["delete"] = self._delete  # type: ignore
        return await self._delete(keys)

    async def _find_one(self, keys: dict[str, Any]) -> Optional[ModelType]:
        """Private find_one method.

        Replaces public method after first call in order to lazy load
        the prepared statements without needing a None check on all
        subsequent calls.
        """
        result = self._session.execute(
            query=self._find_one_statement, parameters=keys
        ).one()
        try:
            # noinspection PyProtectedMember
            return self._deserialize(result)
        except AttributeError:
            return None

    async def _insert(self, model: ModelType) -> None:
        """Private insert method.

        Replaces public method after first call in order to lazy load
        the prepared statements without needing a None check on all
        subsequent calls.
        """
        parameters = [
            model.__dict__[k] if model.__dict__[k] is not None else UNSET_VALUE
            for k in model.__fields__
        ]
        self._session.execute(query=self._insert_statement, parameters=parameters)

    async def _upsert(self, model: ModelType) -> None:
        """Private upsert method.

        Replaces public method after first call in order to lazy load
        the prepared statements without needing a None check on all
        subsequent calls.
        """
        parameters = [
            model.__dict__[k] if model.__dict__[k] is not None else UNSET_VALUE
            for k in model.__fields__
        ]
        self._session.execute(query=self._upsert_statement, parameters=parameters)

    async def _update(self, model: ModelType) -> None:
        """Private update method.

        Replaces public method after first call in order to lazy load
        the prepared statements without needing a None check on all
        subsequent calls.
        """
        parameters = [
            model.__dict__[k] if model.__dict__[k] is not None else UNSET_VALUE
            for k in model.__fields__
            if k not in self._keys
        ] + [model.__dict__[k] for k in self._keys]
        self._session.execute(query=self._update_statement, parameters=parameters)

    async def _delete(self, keys: dict[str, Any]) -> None:
        """Private delete method.

        Replaces public method after first call in order to lazy load
        the prepared statements without needing a None check on all
        subsequent calls.
        """
        self._session.execute(query=self._delete_statement, parameters=keys)

    def _deserialize(self, row: Any) -> ModelType:
        """Deserialize CQL row to Pydantic model."""
        if self._cql_set_fields:
            # noinspection PyProtectedMember
            row_dict: dict = row._asdict()  # type: ignore
            return self._model_type(
                **{
                    k: v if k not in self._cql_set_fields else list(v or [])
                    for k, v in row_dict.items()
                }
            )
        # If no special translations need to be done replace this method
        # with wrapper for `_asdict()`.
        # noinspection PyProtectedMember
        self._deserialize = lambda r: self._model_type(**r._asdict())  # type: ignore
        return self._deserialize(row)

    def _get_create_table_queries(self) -> list[str]:
        # Create string for primary key.
        partitioning_keys = ", ".join(self._metadata.partition_keys)
        if self._metadata.clustering_keys:
            clustering_keys = ", " + ", ".join(self._metadata.clustering_keys)
        else:
            clustering_keys = ""

        # Create string for columns.
        columns = f",\n{self._indent}".join(
            [
                f"{k} {_py_type_to_cql(v.annotation)}"
                for k, v in self._model_type.__fields__.items()
            ]
        )

        # Create string for indexed columns.
        index_queries = [
            f"CREATE CUSTOM INDEX ON {self._keyspace}.{self._tablename} ({idx})\n"
            "USING 'StorageAttachedIndex';"
            for idx in self._metadata.index or []
        ]

        # Put it all together.
        table_query = inspect.cleandoc(
            f"""
            CREATE TABLE {self._keyspace}.{self._tablename} (
              {{columns}},
              PRIMARY KEY (({partitioning_keys}){clustering_keys})
            );
            """
        ).format(columns=columns)
        return [table_query] + index_queries

    def _get_find_query(
        self, filter_columns: list[str], list_contains: Optional[list[str]] = None
    ) -> str:
        list_contains = list_contains if list_contains is not None else []
        value_where = [f"{k} = :{k}" for k in filter_columns]
        list_where = [f"{k} CONTAINS :{k}" for k in list_contains]
        where = f"\n{self._indent}AND ".join(value_where + list_where)
        return inspect.cleandoc(
            f"""
            SELECT
              *
            FROM
              {self._keyspace}.{self._tablename}
            WHERE
              {{where}};
            """
        ).format(where=where)

    def _get_insert_query(self) -> str:
        columns = ",".join(self._model_type.__fields__)
        place_holders = ",".join([f":{k}" for k in self._model_type.__fields__])
        return inspect.cleandoc(
            f"""
            INSERT INTO
              {self._keyspace}.{self._tablename} ({columns})
            VALUES
              ({place_holders});
            """
        )

    def _get_upsert_query(self) -> str:
        columns = ",".join(self._model_type.__fields__)
        place_holders = ",".join([f":{k}" for k in self._model_type.__fields__])
        return inspect.cleandoc(
            f"""
            INSERT INTO
              {self._keyspace}.{self._tablename} ({columns})
            VALUES
              ({place_holders})
            IF NOT EXISTS;
            """
        )

    def _get_update_query(self) -> str:
        set_placeholders = f",\n{self._indent}".join(
            f"{c} = ?" for c in self._model_type.__fields__ if c not in self._keys
        )
        where = f"\n{self._indent}AND ".join(f"{k} = ?" for k in self._keys)
        return inspect.cleandoc(
            f"""
            UPDATE
              {self._keyspace}.{self._tablename}
            SET
              {{set_placeholders}}
            WHERE
              {{where}};
            """
        ).format(set_placeholders=set_placeholders, where=where)

    def _get_delete_query(self) -> str:
        where = f"\n{self._indent}AND ".join(f"{k} = :{k}" for k in self._keys)
        return inspect.cleandoc(
            f"""
            DELETE FROM
              {self._keyspace}.{self._tablename}
            WHERE
              {{where}};
            """
        ).format(where=where)


def _py_type_to_cql(type_: Type) -> str:
    origin = typing.get_origin(type_)
    if origin is dict:
        k_type, v_type = typing.get_args(type_)
        k_type = _py_type_to_cql(k_type)
        v_type = _py_type_to_cql(v_type)
        return f"MAP<{k_type}, {v_type}>"
    try:
        # If list or set.
        if (
            origin is list
            or issubclass(type_, pydantic.types.ConstrainedList)
            or origin is set
            or issubclass(type_, pydantic.types.ConstrainedSet)
        ):
            args = typing.get_args(type_)
            v_type = _py_type_to_cql(args[0]) if args else "TEXT"
            return f"SET<{v_type}>"
    except TypeError:
        pass  # `issubclass` raises TypeError for many potential values of type_.
    if origin and origin == typing.Union:
        type_choices = [
            it
            for it in typing.get_args(type_)
            if not issubclass(it, NoneType)  # type: ignore
        ]
        if len(type_choices) == 1:
            return _py_type_to_cql(type_choices[0])
    return {
        bool: "BOOLEAN",
        int: "INT",
        float: "DECIMAL",
        str: "TEXT",
        dict: "MAP<TEXT, TEXT>",
        list: "SET<TEXT>",
        set: "SET<TEXT>",
        UUID: "UUID",
        datetime.datetime: "TIMESTAMP",
        datetime.date: "DATE",
        datetime.time: "TIME",
    }[type_]
