import os
from abc import ABC, abstractmethod

from elife_api_validator import SCHEMA_DIRECTORY
from elife_api_validator.exceptions import SchemaNotFound
from elife_api_validator.media_type import MediaType


class SchemaFinder(ABC):
    @property
    @abstractmethod
    def schema_dir(self):
        raise NotImplementedError

    @abstractmethod
    def find_schema_for(self, media_type: MediaType):
        raise NotImplementedError


class PathBasedSchemaFinder(SchemaFinder):

    error_content_type = 'application/problem+json'
    ext = 'json'

    def __init__(self, schema_dir: str = '') -> None:
        self._schema_dir = schema_dir

    def find_schema_for(self, media_type: MediaType) -> str:
        """Attempts to find the schema file path for a given content type.

        >>> media_type = MediaType('application/vnd.elife.valid-data+json; version=1')
        >>> finder = PathBasedSchemaFinder(schema_dir='test/test_schemas')
        >>> print(finder.find_schema_for(media_type)
        'test/test_schemas/valid-data.v1.json'

        :param :media_type: :class: `MediaType`
        :rtype: str
        """
        if media_type.content_type == self.error_content_type:
            return os.path.join(self.schema_dir, 'error.v1.json')

        path = os.path.join(self.schema_dir, media_type.get_type_str() + '.{}'.format(self.ext))

        if os.path.exists(path):
            return path
        else:
            raise SchemaNotFound('for {}'.format(path))

    @property
    def schema_dir(self):
        if not self._schema_dir:
            self._schema_dir = SCHEMA_DIRECTORY
        return self._schema_dir

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(self.__class__.__name__, self.schema_dir)
