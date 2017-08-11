import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler
from contracts.DfsGuide import DfsGuide
from contracts.Node import Node
from contracts.TreeVisitor import TreeVisitor
from contracts.Validator import Validator


def apply_filters(string: str) -> str:
    # noinspection SqlNoDataSourceInspection
    return "begin {} end".format(string)


class StringFiltrator(TreeVisitor):
    def __init__(self):
        super().__init__(DfsGuide())

    def visit_string(self, depth: int, node: Node, parent: Node):
        quote = node.token.name[0]
        string = "begin %s end" % node.token.name[1:-1]
        node.token.name = quote + string + quote


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("  strong param[0] != 'null'",
                    "  weak param[1] != 'null'",
                    "  strong result != 'null'",
                    "  strong 'The bucket is reset' == true",
                    "  strong 'The bucket must not be shared' == true",
                    "  strong 'parsing is not supported' == false",
                    "  strong 'the text to parse is invalid' == false")
        raw_tree = "root(" \
                   "strong(!=(param[0],'begin null end'))," \
                   "weak(!=(param[1],'begin null end'))," \
                   "strong(!=(result,'begin null end'))," \
                   "strong(==('begin The bucket is reset end',true))," \
                   "strong(==('begin The bucket must not be shared end',true))," \
                   "strong(==('begin parsing is not supported end',false))," \
                   "strong(==('begin the text to parse is invalid end',false)))"
        tree = Parser.parse("\n".join(raw_code))
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        tree = Decompiler.dfs(tokens)
        Validator().accept(tree)
        filtrator = StringFiltrator()
        filtrator.accept(tree)
        Validator().accept(tree)
        assert str(tree) == raw_tree
