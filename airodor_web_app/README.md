
# airodor-web-app
provide a simple web application and api for the airodor wifi module from limot

To run this application:

```bash
poetry run flask run
```

## install poetry

```bash
curl -sSL https://install.python-poetry.org | python3 - --version $(cat ./.poetry-version)
poetry self add poetry-multiproject-plugin
```

### Prepare poetry Environment

```bash
poetry config virtualenvs.in-project true
cd airodor_web_app && poetry install
```

### Debugging the API when using the WebApp
in [pyproject.toml](pyproject.toml): 
1. comment line 

    ```
    airodor_wifi_api = { git = "https://github.com/BenniWi/airodor-wifi.git", subdirectory = "airodor_wifi_api", branch = "main" }
    ```
2. uncomment line 

    ```
    # airodor_wifi_api = {path = "../airodor_wifi_api", develop = true}
    ```


## connect codespace with local network
using the GitHub cli:
```bash
gh net
```

for more details check this https://github.com/github/gh-net#codespaces-network-bridge



  

