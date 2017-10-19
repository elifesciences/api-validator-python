import os

import elife_api_validator


def test_it_has_schema_directory_constant():
    raw_schema_dir = os.path.dirname(elife_api_validator.schemas.__file__)
    assert elife_api_validator.SCHEMA_DIRECTORY == raw_schema_dir


def test_schema_module_contains_schema_files():
    schema_dir = elife_api_validator.SCHEMA_DIRECTORY
    assert len(os.listdir(schema_dir)) > 1
