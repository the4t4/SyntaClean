from distutils.log import debug
import sys
import logging

from lark import Lark, logger
from lark.indenter import Indenter
from lark.visitors import Transformer_InPlace, Discard

logger.setLevel(logging.DEBUG)

class FooterIndenter(Indenter):
    NL_type = 'T_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

class TokenRemover(Transformer_InPlace):
    def T_NEWLINE(self, token):
        return Discard
    def indents(self, token):
        return Discard

parser = Lark.open("resources/clean.lark", rel_to=__file__, parser="lalr", debug=False, postlex=FooterIndenter())

if __name__ == "__main__":
    try:
        f = open(sys.argv[1])
    except IndexError:
        print("py main.py <inputfile>")
        sys.exit(2)
    except FileNotFoundError:
        print("File could not be found")
        sys.exit(2)
    tree = parser.parse(f.read())
    TokenRemover().transform(tree)
    print(tree.pretty())
