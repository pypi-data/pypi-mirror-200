# OpenPySQL

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![Python package](https://github.com/joumaico/openpysql/actions/workflows/python-package.yml/badge.svg)](https://github.com/joumaico/openpysql/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joumaico/openpysql/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joumaico/openpysql/actions/workflows/python-publish.yml)

## Installation

```console
$ pip install openpysql
```

## Usage

OpenPySQL: A Python module for connecting to SQLite and MySQL databases and executing SQL queries.

This module provides a class OpenPySQL with methods for connecting to SQLite and MySQL databases and executing SQL queries. It also includes methods for hashing and checking passwords using the bcrypt library.

Example usage:

```python
from openpysql import OpenPySQL

# Connect to SQLite database
db = OpenPySQL.sqlite('example.db')

# Execute an INSERT query
db.query = 'INSERT INTO users (name, age) VALUES (?, ?);'
db.value = ('Alice', 25)
db.execute()

# Execute a SELECT query
db.query = 'SELECT * FROM users WHERE age > ?;'
db.value = 18
results = db.fetch()

# Hash a password
hashed_password = OpenPySQL.hash_password('password')

# Check a password
is_valid = OpenPySQL.check_password('password', hashed_password)

# Close connection
db.close()
```

## Links
* PyPI Releases: https://pypi.org/project/openpysql
* Source Code: https://github.com/joumaico/openpysql
