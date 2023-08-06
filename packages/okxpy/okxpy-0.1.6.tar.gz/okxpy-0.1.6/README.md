# okxpy

[![Downloads](https://pepy.tech/badge/okxpy)](https://pepy.tech/project/okxpy)

# Description

Okxpy is a Python package that provides a convenient wrapper for making API requests to the OKX exchange. With this package, users can easily access the various services offered by the OKX exchange, such as trading, account management, and market data retrieval.

Using Okxpy, developers can quickly integrate OKX functionality into their Python applications, without the need for manual HTTP requests and parsing JSON responses. The package abstracts away the details of HTTP communication and handles error responses gracefully, so users can focus on their application logic.

The package includes a variety of modules that correspond to the different services provided by the OKX API. These modules include methods for making requests to the OKX API endpoints, as well as for parsing and processing the responses. The package also includes a variety of utility functions for common tasks, such as generating authentication headers.

To use Okxpy, users simply need to install the package using pip and provide their OKX API credentials. The package supports both public and private API calls, with authentication handled automatically for private calls.

Overall, Okxpy provides a simple, convenient, and reliable way to access the OKX exchange API from Python.


## Source code

https://github.com/EnkhAmar/okxpy


## Reference

[OKX API Documentation](https://www.okx.com/docs-v5/en/)

[How to upload package to pypi?](https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/)


## Push update to pypi

```shell
python -m build
twine upload --skip-existing dist/*  
```