[![Build Status](https://travis-ci.org/elifesciences/api-validator-python.svg?branch=add_travis_and_coveralls_support)](https://travis-ci.org/elifesciences/api-validator-python) [![Coverage Status](https://coveralls.io/repos/github/elifesciences/api-validator-python/badge.svg?branch=add_travis_and_coveralls_support)](https://coveralls.io/github/elifesciences/api-validator-python?branch=add_travis_and_coveralls_support)

# eLife API Validator for Python

This library provides a validator for the [eLife Sciences API](https://github.com/elifesciences/api-raml).

It validates HTTP responses to make sure that they match the schema specification for that media type.

Dependencies
------------

* Python 3.5 or greater

Installation
------------

`python setup.py install`

Usage
-----

To validate a response:

```python
import requests

from elife_api_validator.validators import JSONResponseValidator

>>> response = requests.get('https://api.elifesciences.org/articles')
>>> JSONResponseValidator.validate(response)

```

The validate method will return `None` if valid, otherwise it will raise a `ValidationError` with the appropriate information.

