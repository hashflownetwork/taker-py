Python Hashflow Taker API
=========================

Uses the `requests` python library.

Running basic test
------------------

```sh
python -m hashflow.api
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