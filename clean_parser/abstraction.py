from enum import Enum

from lark import Token
from lark.visitors import Transformer_InPlace, Discard

class AbstractionLevel(Enum):
    NONE = 0
    SIMPLE = 1
    COMPLETE = 2

class TokenRemover(Transformer_InPlace):
    def __default_token__(self, token):
        return Discard

class TokenAbstractor(Transformer_InPlace):
    def __default_token__(self, token):
        return Token(token.type, 'ABSTRACTED')

def applyAbstr(tree, abstractionLevel):
    if abstractionLevel == AbstractionLevel.NONE:
        return
    elif abstractionLevel == AbstractionLevel.SIMPLE:
        TokenAbstractor().transform(tree)
    elif abstractionLevel == AbstractionLevel.COMPLETE:
        TokenRemover().transform(tree)
