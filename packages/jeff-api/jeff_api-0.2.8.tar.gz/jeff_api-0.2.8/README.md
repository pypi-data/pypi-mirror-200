# jeff-api

Python library for Jeff interaction. Supports both `jeff-qt` and `jeff-core`.

## Installing from PyPi.org

```bash
pip install jeff-api
```

## Usage

```python
from jeff_api import server, client

srv = server.Server(None, ext_port)
cli = client.Client('localhost', jeff_port)

data = srv.listen()
cli.send_msg(data)
```

```python
from jeff_api import client, server, scenario

srv = server.Server(None, ext_port)
cli = client.Client('localhost', jeff_port)
scn = scenario.Scenario(cli, srv, "Example scenario")
```

## Building

```bash
cd jeff-api
python -m pip install --upgrade build
python -m build
```
