import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser.Parser import parse, parse_tree
from contracts.visitors.AstCompiler import AstCompiler
from contracts.visitors.AstEqualReducer import AstEqualReducer


class TestCase(unittest.TestCase):
    def test(self):
        raw_tree = ("strong", " true")
        forest = parse("(false != true) == true")
        assert len(forest) == 1
        ast = forest[0]
        assert ast.consistent()
        reducer = AstDfsGuide(AstEqualReducer())
        reducer.accept(ast)
        assert str(ast) == "\n".join(raw_tree)
        compiler = AstDfsGuide(AstCompiler())
        args = compiler.accept(ast)
        ast = parse_tree(*args, collapse_type="dfs")
        assert ast.consistent()
        ast = parse_tree(*args, collapse_type="bfs")
        assert ast.consistent()
