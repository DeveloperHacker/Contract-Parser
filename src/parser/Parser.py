from typing import Iterable, Generator

from parser.Tree import Tree


class Parser:
    @staticmethod
    def tokenize(source: str) -> Generator[str]:
        delimiters = ("(", ")", ",", ":", " ", "\"", "\n")
        token = []
        for ch in source:
            if ch in delimiters:
                token = "".join(token).strip()
                if len(token) > 0:
                    yield token
                if ch != " ":
                    yield ch
                token = []
            else:
                token.append(ch)
        token = "".join(token).strip()
        if len(token) > 0:
            yield token

    @staticmethod
    def parse(source: str) -> Iterable[Tree]:
        for token in Parser.tokenize(source):
            print(token)
