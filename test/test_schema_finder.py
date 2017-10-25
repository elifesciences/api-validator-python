import pytest

from elife_api_validator import SCHEMA_DIRECTORY
from elife_api_validator.exceptions import SchemaNotFound
from elife_api_validator.media_type import MediaType
from elife_api_validator.schema_finder import PathBasedSchemaFinder


def test_it_has_schema_directory_by_default_on_init():
    finder = PathBasedSchemaFinder()
    assert finder.schema_dir == SCHEMA_DIRECTORY


def test_it_can_return_correct_repr():
    custom_dir = 'some/custom_dir'
    finder = PathBasedSchemaFinder(schema_dir=custom_dir)
    assert repr(finder) == "PathBasedSchemaFinder({!r})".format(custom_dir)


def test_it_can_have_a_custom_schema_directory_passed_to_init():
    custom_dir = 'some/custom_dir'
    finder = PathBasedSchemaFinder(schema_dir=custom_dir)
    assert finder.schema_dir == custom_dir


def test_it_fails_if_schema_cannot_be_found():
    finder = PathBasedSchemaFinder(schema_dir='test/test_schemas')

    with pytest.raises(SchemaNotFound):
        media_type = MediaType('application/invlalid.type')
        finder.find_schema_for(media_type)


def test_it_should_find_schema_for_valid_media_type():
    finder = PathBasedSchemaFinder(schema_dir='test/test_schemas')
    media_type = MediaType('application/vnd.elife.valid-data+json; version=1')
    assert finder.find_schema_for(media_type) == 'test/test_schemas/valid-data.v1.json'


def test_it_should_find_schema_for_problem_json_error_response():
    content_type = 'application/problem+json'
    media_type = MediaType(content_type)
    schema_dir = 'test/test_schemas'

    finder = PathBasedSchemaFinder(schema_dir=schema_dir)
    assert finder.find_schema_for(media_type) == schema_dir + '/error.v1.json'


def test_it_should_find_the_correct_alternate_version_from_media_type():
    finder = PathBasedSchemaFinder(schema_dir='test/test_schemas')
    media_type = MediaType('application/vnd.elife.valid-data+json; version=2')
    assert finder.find_schema_for(media_type) == 'test/test_schemas/valid-data.v2.json'
