import sys
import json
import argparse
import lark

from .parser import parseStatements, parseGraph
from .serializer import serializeGraph

formats = ["ndjson", "json", "pg"]


def pgformat(args):
    parser = argparse.ArgumentParser(
        prog="pgformat",
        description="Parse and transform property graphs in PG Format."
    )
    parser.add_argument(
        '-t', '--to',
        choices=formats, default="ndjson",
        help="target format",
    )
    parser.add_argument(
        'source', nargs='?', help="input file (default: - for standard input)", default="-")
    args = parser.parse_args(args)

    # TODO: configure node merging and duplicated edge ids

    if args.source == "-":
        input = sys.stdin.read()
    else:
        input = open(args.source).read()

    try:
        if args.to == "ndjson":
            for s in parseStatements(input):
                print(json.dumps(s))
        else:
            graph = parseGraph(input)
            if args.to == "json":
                print(json.dumps(graph, indent=2))
            elif args.to == "pg":
                print(serializeGraph(graph))
    except lark.exceptions.UnexpectedInput as err:
        print(err, file=sys.stderr)
        return 1

    return 0


def cli():
    sys.exit(pgformat(sys.argv[1:]))
