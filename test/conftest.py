from pytest import fixture

from elife_api_validator.schema_finder import PathBasedSchemaFinder
from elife_api_validator.validators import JSONResponseValidator


@fixture
def finder():
    return PathBasedSchemaFinder('test/test_schemas')


@fixture
def validator(finder):
    return JSONResponseValidator(schema_finder=finder)
