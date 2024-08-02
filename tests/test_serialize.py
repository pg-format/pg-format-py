import unittest
import json
import re
from pathlib import Path

from pgformat import parseGraph, serializeGraph

SUITE_DIR = Path(__file__).parent.resolve() / "pg-test-suite"


class TestSuite(unittest.TestCase):

    def test_valid_test_cases(self):
        valid = json.load(open(SUITE_DIR / "pg-format-valid.json"))
        for t in valid:
            graph = parseGraph(t["pg"], sort=True)
            pg = serializeGraph(graph)
            self.assertEqual(graph, parseGraph(pg, sort=True))

    def test_examples(self):
        for f in Path(SUITE_DIR / "examples").glob('*.pg'):
            graph = parseGraph(open(f).read(), sort=True)
            pg = serializeGraph(graph)
            self.assertEqual(graph, parseGraph(pg, sort=True))


if __name__ == '__main__':
    unittest.main()
