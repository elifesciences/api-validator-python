import os

import elife_api_validator.schemas as schemas

__version__ = '0.0.1'


SCHEMA_DIRECTORY = os.path.dirname(schemas.__file__)


__all__ = [SCHEMA_DIRECTORY]
