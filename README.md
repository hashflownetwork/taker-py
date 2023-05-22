Python Hashflow Taker API
=========================

Uses the `aiohttp` python library.

Setup
-----
```sh
pip install -r requirements.txt
```

Running basic test
------------------

```sh
python -m hashflow.api
```

Running unit tests
------------------
```sh
pytest
```

Building Instructions
---------------------

```sh
python3 -m pip install --upgrade build
python3 -m build
```

Publishing Instructions
-----------------------

```sh
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*

```
