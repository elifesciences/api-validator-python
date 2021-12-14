#!/usr/bin/env bash
set -e
. install.sh
coverage run -m pytest --junitxml=build/pytest.xml
