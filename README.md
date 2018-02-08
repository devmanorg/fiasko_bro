# Fiasko Bro

> When flake8 is not enought.

[![Build Status](https://travis-ci.org/devmanorg/fiasko_bro.svg?branch=master)](https://travis-ci.org/devmanorg/fiasko_bro)
[![codecov](https://codecov.io/gh/devmanorg/fiasko_bro/branch/master/graph/badge.svg)](https://codecov.io/gh/devmanorg/fiasko_bro)
[![Documentation Status](https://readthedocs.org/projects/fiasko-bro/badge/?version=latest)](http://fiasko-bro.readthedocs.io/en/latest/?badge=latest)

Fiasko is a static analysis tool for python code that catches common style errors.

![](http://melevir.com/static/fiasko.jpg)

### Example

```python
>>> import fiasko_bro
>>> fiasko_bro.validate_repo('/path/to/repo/')
[('camel_case_vars', 'переименуй, например, WorkBook.')]
```
The `validate_repo` method returns list of tuples which consist of an error slug and an error message.


### Installation

With pip:
```bash
pip install git+https://github.com/devmanorg/fiasko_bro.git
```

Or just clone the project and install the requirements:
```bash
$ git clone https://github.com/devmanorg/fiasko_bro.git
$ cd fiasko_bro
$ pip install -r requirements.txt
```

### Docs
[fiasko-bro.readthedocs.io](http://fiasko-bro.readthedocs.io/)


### Contributing
Read more about it [in the docs](http://fiasko-bro.readthedocs.io/en/latest/contributing.html)


### Launch tests
`python -m pytest`


### Versioning
We follow [semantic versioning](https://github.com/dbrock/semver-howto/blob/master/README.md).
