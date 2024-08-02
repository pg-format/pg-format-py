import re
from lark import Lark, Transformer, Discard, v_args

parser = Lark.open("grammar.lark", rel_to=__file__, parser='earley')

escapeCodes = {
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
}


def mergeProperties(ps, props):
    for key, values in ps:
        if key in props:
            props[key] += values
        else:
            props[key] = values
    return props


def parseNumber(n):
    if "." in n or "e" in n or "E" in n:
        n = float(n)
        if n.is_integer():
            n = int(n)
    else:
        n = int(n)
    return n


class ToStatements(Transformer):

    def node(self, data):
        node = {
            "type": "node",
            "id": data[0],
            "labels": data[1],
            "properties": data[2]
        }
        return node

    def edge(self, data):
        edge = {"type": "edge"}
        if len(data) == 6:
            edge["id"] = data.pop(0)
        edge["from"] = data[0]
        edge["to"] = data[2]
        edge["labels"] = data[3]
        edge["properties"] = data[4]
        if data[1].children[0].data.value == "undirected":
            edge["undirected"] = True
        return edge

    def unescaped(self, chars):
        return ''.join(chars)

    @v_args(inline=True)
    def escaped(self, code):
        if len(code) == 4:
            return chr(int(code, 16))
        elif code in escapeCodes:
            return escapeCodes[str(code)]
        else:
            return code

    def empty(self, _):
        return Discard

    def edge_identifier(self, x):
        return x[0]

    def statement(self, x):
        return x[0]

    def statement_separator(self, _):
        return Discard

    def QUOT(self, _):
        return '"'

    def APOS(self, _):
        return "'"

    @v_args(inline=True)
    def label(self, label):
        return label

    def labels(self, L):
        return list(set(L))

    def single_quoted(self, children):
        return children[0]

    def double_quoted(self, children):
        return children[0]

    def UNQUOTED_CHAR(self, children):
        return children[0]

    def UNQUOTED_KCHAR(self, children):
        return children[0]

    def UNQUOTED_VCHAR(self, children):
        return children[0]

    def UNQUOTED_START(self, children):
        return children[0]

    def quoted_id(self, children):
        return ''.join(children)

    def property(self, args):
        return args

    def properties(self, ps):
        return mergeProperties(ps, {})

    def key(self, children):
        return children[0]

    def quoted_key(self, children):
        return children[0]

    def COLON(self, _):
        return ":"

    def unquoted_key(self, children):
        return ''.join(children[:-1])

    def unquoted_key2(self, children):
        return ''.join(children)

    def identifier(self, args):
        return ''.join(args)

    def quoted_string(self, args):
        return ''.join(args)

    def value(self, children):
        return children[0]

    def unquoted_value(self, children):
        v = ''.join(children)
        if v == "true":
            return True
        elif v == "false":
            return False
        elif re.match('^-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?$', v):
            return parseNumber(v)
        else:
            return v

    def DW(self, _):
        return Discard

    def SPACES(self, _):
        return Discard

    def value_list(self, children):
        return children

    def number(self, args):
        return parseNumber(args[0])

    def boolean(self, args):
        return args[0] == "true"

    def start(self, statements):
        return statements


def parseStatements(pg, duplicatedEdgeIds=False, mergeNodes=True, implicitNodes=False):
    tree = parser.parse(pg)
    transformer = ToStatements()
    statements = transformer.transform(tree)

    if not (mergeNodes or implicitNodes):
        return statements

    nodes = [s for s in statements if s["type"] == "node"]
    edges = [s for s in statements if s["type"] == "edge"]

    # TODO: move to parser to get position information
    if not duplicatedEdgeIds:
        edgeId = set()
        for e in edges:
            if "id" in e:
                if e["id"] in edgeId:
                    # TODO: more specific error messag
                    raise Exception("Duplicated edge id!")
                edgeId.add(e["id"])

    if mergeNodes:
        nodeId = {}
        for nd in nodes:
            id = nd["id"]
            if id in nodeId:
                node = nodeId[id]
                node["labels"] = list(set(node["labels"] + nd["labels"]))
                mergeProperties(nd["properties"].items(), node["properties"])
            else:
                nodeId[id] = nd
        nodes = list(nodeId.values())

    else:
        nodeId = set([n["id"] for n in nodes])

    def addNode(id):
        if id not in nodeId:
            node = {"type": "node", "id": id, "labels": [], "properties": {}}
            nodeId[id] = node
            nodes.append(node)

    if implicitNodes:
        for e in edges:
            addNode(e["from"])
            addNode(e["to"])

    return nodes + edges


def parseGraph(pg, sort=True):
    statements = parseStatements(pg, implicitNodes=True)

    if sort:
        for s in statements:
            s["labels"].sort()

    nodes = [s for s in statements if s["type"] == "node"]
    edges = [s for s in statements if s["type"] == "edge"]
    for n in nodes:
        del n["type"]
    for e in edges:
        del e["type"]

    if sort:
        nodes.sort(key=lambda n: n["id"])

    return {
        "nodes": nodes,
        "edges": edges,
    }
