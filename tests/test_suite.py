import unittest
import json
import re
from pathlib import Path

from pgformat import parseGraph

SUITE_DIR = Path(__file__).parent.resolve() / "pg-test-suite"

# TODO: test parseStatements


class TestSuite(unittest.TestCase):

    def test_valid_test_cases(self):
        valid = json.load(open(SUITE_DIR / "pg-format-valid.json"))
        for t in valid:
            # print(t["about"] if "about" in t else t["pg"])
            graph = parseGraph(t["pg"], sort=True)
            if "graph" in t:
                self.assertEqual(graph, t["graph"])
            else:
                self.assertTrue(graph)

    def test_invalid_test_cases(self):
        invalid = json.load(open(SUITE_DIR / "pg-format-invalid.json"))
        for pg in invalid:
            with self.assertRaises(Exception):  # TODO: more specific error class
                parseGraph(pg)

    def test_examples(self):
        for f in Path(SUITE_DIR / "examples").glob('*.pg'):
            graph = parseGraph(open(f).read(), sort=True)
            jsonFile = re.sub('\\.pg$', '.json', str(f))
            print(f)
            if Path(jsonFile).is_file():
                expect = json.load(open(jsonFile))
                self.assertEqual(graph, expect)
            else:
                self.assertTrue(graph)


if __name__ == '__main__':
    unittest.main()
