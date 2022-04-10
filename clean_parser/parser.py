from distutils.log import debug
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

parser = Lark.open("grammars/clean.lark", rel_to=__file__, parser="lalr", postlex=FooterIndenter(), debug=False)
