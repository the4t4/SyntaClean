from lark.lexer import Token
from hashlib import md5

from plagiarism_checker.fingerprint import Fingerprint, idGenerator

def naiveCheck(tree1, tree2):
    return tree1 == tree2

def collisionCheck(tree1, tree2):
    hashTable = {}
    collisions = {}
    hashTree(tree1, next(idGenerator), hashTable, collisions)
    hashTree(tree2, next(idGenerator), hashTable, collisions)
    size1 = treeSize(tree1)
    size2 = treeSize(tree2)
    collidedSize1 = 0
    collidedSize2 = 0
    for key, vals in collisions.items():
        if len(vals[0]) != 0 and len(vals[1]) != 0:
            collidedSize1 += sum(a.weight for a in vals[0])
            collidedSize2 += sum(a.weight for a in vals[1])
    return (collidedSize1/size1, collidedSize2/size2)

def hashTree(tree, id, hashTable, collisions):
    hash = md5(repr(tree).encode('ASCII')).digest()
    fingerprint = Fingerprint(id, treeSize(tree), tree)
    if hashTable.get(hash) != None:
        if collisions.get(hash) != None:
            collisions.get(hash)[id].append(fingerprint)
        else:
            list = [ [] for _ in range(2) ]
            list[hashTable.get(hash).id].append(hashTable.get(hash))
            list[id].append(fingerprint)
            collisions.update({hash:list})
    else:
        hashTable.update({hash:fingerprint})
        for subtree in tree.children:
            if type(subtree) != Token:
                hashTree(subtree, id, hashTable, collisions)

def treeSize(tree):
    iter = tree.iter_subtrees()
    sum = 0
    for subtree in iter:
        sum += 1
        for child in subtree.children:
            if type(child) == Token:
                sum += 1
    return sum
