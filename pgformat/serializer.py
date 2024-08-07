import re
import json

plainId = re.compile(
    r'^[^\u0000-\u0020<>\'"{}|^`\\#:([-][^\u0000-\u0020<>"{}|^`\\]*$')
specialValue = re.compile(r'^(-?[0-9]+(\.[0-9]+)?|true|false|)$')
reserved = re.compile(r'.*[ \u0009<>"{}|^`\\#:([,-]')


def quoteId(id):
    return id if plainId.match(id) and not re.match('--', id) else json.dumps(id)


def quoteValue(s):
    print(reserved.match(" b"))
    return s if isinstance(s, str) and not (specialValue.match(s) or reserved.match(s)) else json.dumps(s)


def serializeLabelsOf(elem):
    if "labels" in elem:
        return " ".join([":" + quoteId(s) for s in elem["labels"]])
    else:
        return ""


def serializeValues(values):
    return ",".join([quoteValue(v) for v in values])


def serializeProperty(key, values):
    return quoteId(key) + (": " if ":" in key else ":") + serializeValues(values)


def serializePropertiesOf(elem):
    if "properties" in elem:
        return " ".join([serializeProperty(k, v) for (k, v) in elem["properties"].items()])
    else:
        return ""


def serializeNode(node):
    parts = [
        quoteId(node["id"]),
        serializeLabelsOf(node),
        serializePropertiesOf(node)
    ]
    return " ".join([p for p in parts if p != ""])


def serializeEdge(edge):
    undirected = "undirected" in edge and edge["undirected"]
    parts = [
        quoteId(edge["from"]),
        ("--" if undirected else "->"),
        quoteId(edge["to"]),
        serializeLabelsOf(edge),
        serializePropertiesOf(edge)
    ]
    if "id" in edge and edge["id"]:
        parts.insert(0, edge["id"] + ":")
    return " ".join([p for p in parts if p != ""])


def serializeGraph(graph: dict) -> str:
    nodes = [serializeNode(n)
             for n in graph["nodes"]] if "nodes" in graph else []
    edges = [serializeEdge(n)
             for n in graph["edges"]] if "edges" in graph else []
    return "\n".join([*nodes, *edges])
