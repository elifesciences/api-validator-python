import os
import re
from abc import ABC, abstractmethod

from elife_api_validator import SCHEMA_DIRECTORY
from elife_api_validator.exceptions import SchemaNotFound
from elife_api_validator.media_type import MediaType


class SchemaFinder(ABC):
    @abstractmethod
    def find_schema_for(self, media_type: MediaType):
        raise NotImplementedError


class PathBasedSchemaFinder(SchemaFinder):

    error_media_type = 'application/problem+json'
    ext = 'json'

    def __init__(self, schema_dir: str = SCHEMA_DIRECTORY) -> None:
        """
        :param schema_dir: str
        """
        self.schema_dir = schema_dir

    @staticmethod
    def get_schema_name(media_type: MediaType) -> str:
        """Returns a formatted content type string.

        >>> media_type = MediaType('application/vnd.elife.article-list+json; version=1')
        >>> print(PathBasedSchemaFinder().get_schema_name(media_type))
        'article-list.v1'

        :rtype: str
        """
        schema_name = ''
        result = re.search(r'(?<=\.)[a-z-]*?(?=\+)', media_type.type)
        if result:
            schema_name = result.group()

        return '{name}.v{version}'.format(name=schema_name,
                                          version=media_type.params.get('version', '1'))

    def find_schema_for(self, media_type: MediaType) -> str:
        """Attempts to find the schema file path for a given content type.

        >>> media_type = MediaType('application/vnd.elife.valid-data+json; version=1')
        >>> finder = PathBasedSchemaFinder(schema_dir='test/test_schemas')
        >>> print(finder.find_schema_for(media_type)
        'test/test_schemas/valid-data.v1.json'

        :param :media_type: :class: `MediaType`
        :rtype: str
        """
        schema_dir = os.sep.join(self.schema_dir.split('/'))
        if str(media_type) == self.error_media_type:
            return os.path.join(schema_dir, 'error.v1.json')

        path = os.path.join(schema_dir,
                            self.get_schema_name(media_type) + '.{}'.format(self.ext))

        if os.path.exists(path):
            return path
        else:
            raise SchemaNotFound('for {}'.format(path))

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(self.__class__.__name__, self.schema_dir)
