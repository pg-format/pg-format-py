# pgformat

[![Test](https://github.com/pg-format/pgformat/actions/workflows/test.yml/badge.svg)](https://github.com/pg-format/pgformat/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/pgformat?label=pypi%20package)](https://pypi.org/project/pgformat/)

> Property Graph Exchange Format (PG) parser and serializer

This package implements parsers and serializers to for labeled property graphs in [Property Graph Exchange Format](https://pg-format.github.io/).

[PG Format]: https://pg-format.github.io/specification/#pg-format
[PG JSONL]: https://pg-format.github.io/specification/#pg-jsonl

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [API](#api)

## Install

Requires Python 3.

~~~sh
pip install pgformat
~~~

<!-- TODO: install with conda -->

## Usage

The package comes with a simple command line client to convert between serialization forms of Property Graph Exchange format and an [API](#api) to be used in python code. The command line client by default reads [PG Format] and emits [PG JSONL].

~~~sh
usage: pgformat [-h] [-t {ndjson,json,pg}] [source]

Parse and transform property graphs in PG Format.

positional arguments:
  source                input file (default: - for standard input)

options:
  -h, --help            show this help message and exit
  -t {ndjson,json,pg}, --to {ndjson,json,pg}
                        target format
~~~

The functionality is a subset of the [pgraph](https://github.com/pg-format/pgraphs) command line tool written in NodeJS.

## API

The package exports two functions: `parseGraph` and `parseStatements`:

~~~python
from pgformat import parseGraph, parseStatements

graph = parseGraph("a -> b")
statements = parseStatements("x\na -> b")
~~~

The return format consists of plain lists and arrays for direct conversion to JSON.

## License

Licensed under the MIT License.

