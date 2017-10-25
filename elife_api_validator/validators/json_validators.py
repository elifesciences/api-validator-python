from abc import ABC, abstractmethod
import json
from typing import Optional

from jsonschema import validate as validate_json
from jsonschema import ValidationError

from elife_api_validator.exceptions import InvalidContentType, JSONDataNotFound
from elife_api_validator.media_type import MediaType
from elife_api_validator.validators.response_validator import ResponseValidator
from elife_api_validator.schema_finder import PathBasedSchemaFinder, SchemaFinder


class Response(ABC):
    @property
    @abstractmethod
    def headers(self) -> dict:
        raise NotImplementedError


class JSONResponseValidator(ResponseValidator):

    valid_type_pattern = 'application\/([a-z-\.]*\+)json'

    def __init__(self, schema_finder: SchemaFinder = PathBasedSchemaFinder()) -> None:
        """
        :param schema_finder: :class: `SchemaFinder`
        """
        self.schema_finder = schema_finder

    @staticmethod
    def _extract_response_data(response: Response) -> Optional[dict]:
        """Attempt to extract JSON data from the response.
        We currently support the following Response types:

        - werkzeug.wrappers.Response
        - requests.Response

        :param response:
        :return:
        """
        data = None

        try:
            # handles werkzeug.wrappers.Response
            data = json.loads(response.data.decode('UTF-8'))
        except AttributeError:
            # handles requests.Response type
            data = response.json()
        finally:
            if data:
                return data
            else:
                raise JSONDataNotFound('Unable to find JSON data in the response')

    @staticmethod
    def _format_json_str(data: str) -> str:
        """Formats a string containing JSON data into a readable,
        indented form.

        :param data: str
        :rtype: str
        """
        return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))

    def validate(self, response: Response) -> bool:
        """

        :param response:
        :return:
        """
        media_type = MediaType(content_type=response.headers.get('Content-Type'))

        if not media_type.matches_type(pattern=self.valid_type_pattern):
            raise InvalidContentType('{} is an invalid type'.format(media_type.content_type))

        schema_path = self.schema_finder.find_schema_for(media_type=media_type)

        data = self._extract_response_data(response)

        try:
            with open(schema_path) as schema_file:
                validate_json(data, schema=json.load(schema_file))
        except ValidationError as err:

            output = '{0},\n\ndata: {1}\n\nschema: {2}'.format(err.message,
                                                               self._format_json_str(err.instance),
                                                               self._format_json_str(err.schema))
            raise ValidationError(output)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.schema_finder)
