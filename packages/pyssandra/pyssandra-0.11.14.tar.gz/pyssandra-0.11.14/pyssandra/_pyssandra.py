"""Module to provide class to decorate models as tables."""
from typing import Callable, Optional, Type

from cassandra.cluster import Session
from pydantic import BaseModel

from pyssandra._query_builder import ModelType, QueryBuilder, TableMetadata


class Pyssandra:
    """Class to register models as Cassandra Tables."""

    def __init__(self, session: Session, keyspace: str) -> None:
        """Init an instance of the Pyssandra class.

        :param session: Cassandra session to use.
        :param keyspace: Keyspace of the tables.
        """
        self.models: list[Type[BaseModel]] = []
        self._session = session
        self._keyspace = keyspace
        self._model_type_to_query_builder: dict[Type[BaseModel], QueryBuilder] = {}

    def __getitem__(self, item: Type[ModelType]) -> QueryBuilder[ModelType]:
        """Get a `QueryBuilder` for the given model.

        :param item: Model representing a table.
        :return: A `QueryBuilder` for the given model.
        """
        return self._model_type_to_query_builder[item]

    def table(
        self,
        partition_keys: list[str],
        clustering_keys: Optional[list[str]] = None,
        index: Optional[list[str]] = None,
    ) -> Callable[[Type[ModelType]], Type[ModelType]]:
        """Register a model as a database table.

        :param partition_keys: Table partition keys.
        :param clustering_keys: Table clustering keys.
        :param index: Table indexed columns.
        :return: Wrapper for the decorated table.
        """
        table_meta = TableMetadata(
            partition_keys=partition_keys, clustering_keys=clustering_keys, index=index
        )

        def _wrapper(cls: Type[ModelType]) -> Type[ModelType]:
            self.models.append(cls)
            query_builder = QueryBuilder(self._session, self._keyspace, cls, table_meta)
            self._model_type_to_query_builder[cls] = query_builder
            return cls

        return _wrapper
