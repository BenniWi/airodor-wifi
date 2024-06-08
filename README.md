
# airodor-wifi

This repository provides two [poetry](https://python-poetry.org/) packages
1. airodor_wifi_api: this package provides a simple python api to communicate with the limodor/limot airodor wifi module
2. airodor_web_app: this packages provides a simple flas web app as frontend to the airodor_wifi_api. :warning: This module holds a poetry tool dependency to the airodor_wifi_api. This is currently a workaround to have both packages in one repository and will be resolved in the future.

## use the docker container

you can easily use the docker container provided at dockerhub [benniwi/airodor-wifi](https://hub.docker.com/r/benniwi/airodor-wifi)

Start the container with the environment variable **VENTILATION_ADDRESS** to connect it to your airodor wifi module
Give the server a custom name with the environment variable **SERVER_NAME**
Enable the testing mode with the environment variable


## install poetry

```bash
curl -sSL https://install.python-poetry.org | python3
```

### create local venv with poetry

```bash
poetry config virtualenvs.in-project true
```

## connect codespace with local network
using the GitHub cli:
```bash
gh net
```

for more details check this https://github.com/github/gh-net#codespaces-network-bridge

## testing the container

### build the container
```bash
docker build -t benniwi/airodor-wifi:latest --file ./container/Dockerfile .
```
### run the container 
```bash
docker run --env TEST_MODE=1 --env VENTILATION_ADDRESS="1.1.1.1" --env SERVER_NAME="My Custom Server Name"  --expose=80 --rm -ti benniwi/airodor-wifi
```