#!/usr/bin/env bash
set -e

if [ ! -e "venv/bin/python3.5" ]; then
    echo "could not find venv/bin/python3.5, recreating venv"
    rm -rf venv
    virtualenv --python=python3.5 venv
fi

source venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m proofreader elife_api_validator/ test/
coverage run -m pytest --junitxml=build/pytest.xml

COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-api-validator) coveralls
