#!/usr/bin/env bash
set -e

. mkvenv.sh

source venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

coverage run -m pytest --junitxml=build/pytest.xml

COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-api-validator) coveralls
