import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("  strong param[0] != 'null'",
                    "  weak param[1] != 'null'",
                    "  strong result != 'null'",
                    "  strong 'The bucket is reset' == true",
                    "  strong 'The bucket must not be shared' == true",
                    "  strong 'parsing is not supported' == false",
                    "  strong 'the text to parse is invalid' == false")
        raw_tokens = ("root",
                      "strong", "!=", "param[0]", "'null'",
                      "weak", "!=", "param[1]", "'null'",
                      "strong", "!=", "result", "'null'",
                      "strong", "==", "'The bucket is reset'", "true",
                      "strong", "==", "'The bucket must not be shared'", "true",
                      "strong", "==", "'parsing is not supported'", "false",
                      "strong", "==", "'the text to parse is invalid'", "false")
        raw_tree = "root(" \
                   "strong(!=(param[0],'null'))," \
                   "weak(!=(param[1],'null'))," \
                   "strong(!=(result,'null'))," \
                   "strong(==('The bucket is reset',true))," \
                   "strong(==('The bucket must not be shared',true))," \
                   "strong(==('parsing is not supported',false))," \
                   "strong(==('the text to parse is invalid',false)))"
        tree = Parser.parse("\n".join(raw_code))
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        assert len(tokens) == len(raw_tokens)
        assert all(raw_token == token.name for token, raw_token in zip(tokens, raw_tokens))
        assert str(tree) == raw_tree
        yet_another_tree = Decompiler.dfs(Decompiler.typing(raw_tokens))
        Validator().accept(yet_another_tree)
        assert str(yet_another_tree) == str(tree)
        assert yet_another_tree == tree
