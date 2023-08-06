# Models

## Code Style

```bash
sudo apt update
sudo apt install python3-venv python3-pip
cd models
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

```bash
isort .
black .
pycodestyle v1 v3 utils
pylint v1 v3 utils
```

```bash
pytest v1/tests v3/tests utils/tests --maxfail=1
```
