import lark

def naiveCheck(tree1, tree2):
    return tree1 == tree2
     
def treeSize(tree):
    if type(tree) == lark.lexer.Token:
        return 1
    size = 1
    for child in tree.children:
        size += treeSize(child)
    return size
