
# airodor-wifi

This repository provides two [poetry](https://python-poetry.org/) packages
1. airodor_wifi_api: this package provides a simple python api to communicate with the limodor/limot airodor wifi module
2. airodor_web_app: this packages provides a simple flas web app as frontend to the airodor_wifi_api. :warning: This module holds a poetry tool dependency to the airodor_wifi_api. This is currently a workaround to have both packages in one repository and will be resolved in the future.

## use the docker container

you can easily use the docker container provided at dockerhub [benniwi/airodor-wifi](https://hub.docker.com/r/benniwi/airodor-wifi)

Start the container with the environment variable **VENTILATION_ADDRESS** to connect it to your airodor wifi module


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



  

