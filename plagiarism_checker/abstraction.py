from enum import Enum

from lark import Token
from lark.visitors import Transformer, Discard

class AbstractionLevel(Enum):
    SIMPLE = 1
    COMPLETE = 2

class TokenRemover(Transformer):
    def __default_token__(self, token):
        return Discard

class TokenAbstractor(Transformer):
    def __default_token__(self, token):
        return Token(token.type, 'ABSTRACTED')

def applyAbstr(tree, abstractionLevel):
    if abstractionLevel == AbstractionLevel.SIMPLE:
        return TokenAbstractor().transform(tree)
    elif abstractionLevel == AbstractionLevel.COMPLETE:
        return TokenRemover().transform(tree)
    else:
        return tree
