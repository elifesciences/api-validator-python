from jsonschema import validate as validate_json

from elife_api_validator.validators.message_validator import MessageValidator
from elife_api_validator.schema_finder import PathBasedSchemaFinder, SchemaFinder


class JSONResponseValidator(MessageValidator):

    def __init__(self, schema_finder: SchemaFinder = None):
        """

        :param schema_finder:
        """
        self._schema_finder = schema_finder

    def validate(self, respsonse):
        '''
        # validate(message):

        - check for content type but no body error
        - check for body but no content type error
        - check for empty content type

        - check media type, raise 'message has invalid content-type header' if invalid

        - check media type matches type ('~application\/([a-z-\.]*\+)json~')


        - Grab schema for media type

        - check message body against schema for is valid
        - pass back violations for Exception

        '''
        pass

    @property
    def schema_finder(self):
        if not self._schema_finder:
            self._schema_finder = PathBasedSchemaFinder()
        return self.schema_finder

