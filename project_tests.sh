#!/usr/bin/env bash
set -e

if [ ! -e "venv/bin/python3.5" ]; then
    echo "could not find venv/bin/python3.5, recreating venv"
    rm -rf venv
    virtualenv --python=python3.5 venv
fi

source venv/bin/activate

pip install --requirement requirements.txt

pylint --reports=n elife_api_validator
flake8 elife_api_validator/ test/
python -m pytest --junitxml=build/pytest.xml
