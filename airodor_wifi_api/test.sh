#! /usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SRC_DIR=${SCRIPT_DIR}/airodor_wifi_api
TEST_DIR=${SCRIPT_DIR}/tests


echo "isort"
poetry run isort ${SCRIPT_DIR}
echo "black"
poetry run black ${SRC_DIR} ${TEST_DIR}
echo "pytest"
poetry run pytest --cov=airodor_wifi_api --cov-report term:skip-covered --cov-report lcov ${TEST_DIR}
echo "mypy"
poetry run mypy ${SRC_DIR} ${TEST_DIR}
echo "flake8"
poetry run flake8 ${SRC_DIR} ${TEST_DIR}
echo "docstr-coverage"
poetry run docstr-coverage ${SRC_DIR}