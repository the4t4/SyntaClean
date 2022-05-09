from distutils.log import debug
import logging

from lark import Lark, tree, logger
from lark.indenter import Indenter
from lark.visitors import Transformer_InPlace, Discard

from clean_parser.abstraction import AbstractionLevel, applyAbstr

logger.setLevel(logging.DEBUG)

class CleanIndenter(Indenter):
    NL_type = 'T_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

class WhitespaceRemover(Transformer_InPlace):
    def T_NEWLINE(self, token):
        return Discard
    def indents(self, token):
        return Discard

class CleanParser():
    def __init__(self, parser = "lalr", abstractionLevel = AbstractionLevel.NONE, propagate_positions = True, debug = False, logLevel = logging.DEBUG):
        self.parser = Lark.open(
            grammar_filename = "grammars/clean.lark",
            rel_to = __file__,
            parser = parser,
            postlex = CleanIndenter(),
            propagate_positions = propagate_positions,
            debug = debug
        )
        self.abstractionLevel = abstractionLevel
        logger.setLevel(logLevel)

    def parse(self, text):
        tree = self.parser.parse(text)
        WhitespaceRemover().transform(tree)
        applyAbstr(tree, self.abstractionLevel)
        return tree

    def setAbstractionLevel(self, level):
        self.abstractionLevel = level

    def make_png(self, parsedTree, file):
        tree.pydot__tree_to_png(parsedTree, file)

    def make_dot(self, parsedTree, file):
        tree.pydot__tree_to_dot(parsedTree, file)
