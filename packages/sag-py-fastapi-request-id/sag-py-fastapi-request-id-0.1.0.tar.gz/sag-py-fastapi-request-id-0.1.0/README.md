# sag_py_fastapi_request_id

[![Maintainability][codeclimate-image]][codeclimate-url]
[![Coverage Status][coveralls-image]][coveralls-url]
[![Known Vulnerabilities](https://snyk.io/test/github/SamhammerAG/sag_py_fastapi_request_id/badge.svg)](https://snyk.io/test/github/SamhammerAG/sag_py_fastapi_request_id)

[coveralls-image]:https://coveralls.io/repos/github/SamhammerAG/sag_py_fastapi_request_id/badge.svg?branch=master
[coveralls-url]:https://coveralls.io/github/SamhammerAG/sag_py_fastapi_request_id?branch=master
[codeclimate-image]:https://api.codeclimate.com/v1/badges/1d0606922774a8ac4a7d/maintainability
[codeclimate-url]:https://codeclimate.com/github/SamhammerAG/sag_py_fastapi_request_id/maintainability

This library provides a way to identify all log entries that belong to a single request.

## What it does
* Provides a middleware to generate a random request id for every request
* Contains a logging filter that adds the request id as field to every log entry

## How to use

### Installation

pip install sag_py_fastapi_request_id

### Add the middleware

Add this middleware so that the request ids are generated:
```python
from sag_py_fastapi_request_id.request_context_middleware import RequestContextMiddleware
from fastapi import FastAPI

app = FastAPI(...)
app.add_middleware(RequestContextMiddleware)
```

### Get the request id

The request id can be accessed over the context
```python
from sag_py_fastapi_request_id.request_context import get_request_id as get_request_id_from_context
request_id = get_request_id_from_context()
```

This works in async calls but not in sub threads (without additional changes).

See:
* https://docs.python.org/3/library/contextvars.html
* https://kobybass.medium.com/python-contextvars-and-multithreading-faa33dbe953d

### Add request id field to logging

It is possible to log the request id by adding a filter.

```python
import logging
from sag_py_fastapi_request_id.request_context_logging_filter import RequestContextLoggingFilter

console_handler = logging.StreamHandler(sys.stdout)
console_handler.addFilter(RequestContextLoggingFilter())

```

The filter adds the field request_id if it has a value in the context.

## How to publish

* Update the version in setup.py and commit your change
* Create a tag with the same version number
* Let github do the rest
