from lark import Lark, tree
from lark.indenter import Indenter

class FooterIndenter(Indenter):
    NL_type = 'T_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

parser = Lark.open("grammars/grammar.lark", rel_to=__file__, parser="lalr", postlex=FooterIndenter())

if __name__ == "__main__":
    f = open("tests/resources/SampleMidterm1_Solutions.icl")
    tree = parser.parse(f.read()) 
    print(tree.pretty())
