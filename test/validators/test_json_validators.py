import pytest
from jsonschema import ValidationError
import requests
import requests_mock

from elife_api_validator.exceptions import (
    MissingContentType,
    InvalidContentType,
    JSONDataNotFound
)
from elife_api_validator.schema_finder import PathBasedSchemaFinder
from elife_api_validator.validators.json_validators import JSONResponseValidator


def test_it_will_return_the_correct_repr():
    v = JSONResponseValidator()
    assert repr(v) == 'JSONResponseValidator({!r})'.format(v.schema_finder)


def test_it_should_have_a_default_schema_finder_if_not_provided():
    validator = JSONResponseValidator()
    assert validator.schema_finder
    assert type(validator.schema_finder) == PathBasedSchemaFinder


def test_it_should_have_a_custom_schema_finder_if_provided():
    dir_path = '/some/custom/path'
    finder = PathBasedSchemaFinder(dir_path)
    validator = JSONResponseValidator(schema_finder=finder)
    assert validator.schema_finder
    assert validator.schema_finder.schema_dir == dir_path


def test_it_should_validate_a_valid_json_response():
    data = {'name': {'preferred': 'some_user'}}
    headers = {'Content-Type': 'application/vnd.elife.valid-data+json; version=1'}
    url = 'http://localhost:1242/valid-data'

    finder = PathBasedSchemaFinder('test/test_schemas')
    validator = JSONResponseValidator(schema_finder=finder)

    with requests_mock.Mocker() as mock:
        mock.get(url, headers=headers, json=data)
        response = requests.get(url)

    assert response.headers['Content-Type']
    assert not validator.validate(response)


def test_it_will_validate_an_error_response():
    data = {
        "title": "No route found for \"GET /invalid\": Method Not Allowed (Allow: OPTIONS)",
        "type": "about:blank"
    }
    headers = {'Content-Type': 'application/problem+json'}
    url = 'http://localhost:1242/invalid'

    finder = PathBasedSchemaFinder('test/test_schemas')
    validator = JSONResponseValidator(schema_finder=finder)

    with requests_mock.Mocker() as mock:
        mock.get(url, headers=headers, json=data)
        response = requests.get(url)

    assert response.headers['Content-Type']
    assert not validator.validate(response)


def test_it_will_raise_error_with_no_content_type_header_in_response():
    data = {'name': {'preferred': 'some_user'}}
    url = 'http://localhost:1242/valid-data'
    headers = {}

    finder = PathBasedSchemaFinder('test/test_schemas')
    validator = JSONResponseValidator(schema_finder=finder)

    with requests_mock.Mocker() as mock:
        mock.get(url, headers=headers, json=data)
        response = requests.get(url)

    with pytest.raises(MissingContentType):
        validator.validate(response)


def test_it_will_raise_error_with_invalid_content_type_header():
    data = {'name': {'preferred': 'some_user'}}
    url = 'http://localhost:1242/valid-data'
    headers = {'Content-Type': 'some_invalid_type'}

    finder = PathBasedSchemaFinder('test/test_schemas')
    validator = JSONResponseValidator(schema_finder=finder)

    with requests_mock.Mocker() as mock:
        mock.get(url, headers=headers, json=data)
        response = requests.get(url)

    with pytest.raises(InvalidContentType):
        validator.validate(response)


def test_it_should_not_validate_with_invalid_json():
    data = {'invalid': 'data'}
    url = 'http://localhost:1242/valid-data'
    headers = {'Content-Type': 'application/vnd.elife.valid-data+json; version=1'}

    finder = PathBasedSchemaFinder('test/test_schemas')
    validator = JSONResponseValidator(schema_finder=finder)

    with requests_mock.Mocker() as mock:
        mock.get(url, headers=headers, json=data)
        response = requests.get(url)

    with pytest.raises(ValidationError):
        validator.validate(response)


def test_it_should_raise_error_if_there_is_no_json_in_response():
    url = 'http://localhost:1242/valid-data'
    headers = {'Content-Type': 'application/vnd.elife.valid-data+json; version=1'}

    finder = PathBasedSchemaFinder('test/test_schemas')
    validator = JSONResponseValidator(schema_finder=finder)

    with requests_mock.Mocker() as mock:
        mock.get(url, headers=headers)
        response = requests.get(url)

    with pytest.raises(JSONDataNotFound):
        validator.validate(response)
