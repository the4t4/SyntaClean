from itertools import count
from lark.lexer import Token

def treeSize(tree):
    iter = tree.iter_subtrees()
    sum = 0
    for subtree in iter:
        sum += 1
        for child in subtree.children:
            if type(child) == Token:
                sum += 1
    return sum

class IDGenerator():
    idGenerator = count(start=0, step=1)

    def reset(self):
        self.idGenerator = count(start=0, step=1)

    def __next__(self):
        return next(self.idGenerator)

