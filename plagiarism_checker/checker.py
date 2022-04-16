from lark.lexer import Token
from hashlib import md5

from plagiarism_checker.fingerprint import Fingerprint
from plagiarism_checker.utils import treeSize, idGenerator

class PlagiarismCheker():
    def __init__(self, hashTable = {}, collisions = {}):
        self.hashTable = hashTable
        self.collisions = collisions
        self.results = []
        self.weights = []
        self.__size = 0

    def check(self, *trees):
        n = len(trees)
        self.__size += n
        collidedWeights = [0] * self.__size
        self.results = []
        self.updateCollisionSize(n)

        for tree in trees:
            id = next(idGenerator)   
            self.hashTree(tree, id)
            self.weights.append(treeSize(tree))

        for key, vals in self.collisions.items():
            maxCollisions = min(len(val) for val in vals)
            for i in range(self.__size):
                if len(vals[i]) != 0:
                    collidedWeight = vals[i][0].weight * maxCollisions
                    collidedWeights[i] += collidedWeight

        for i in range(self.__size):
            self.results.append(collidedWeights[i]/self.weights[i])

        return self.results

    def hashTree(self, tree, id):
        hash = md5(repr(tree).encode('ASCII')).digest()
        fingerprint = Fingerprint(id, treeSize(tree), tree)
        collided = self.addTreeHash(hash, fingerprint)
        if not collided:
            for subtree in tree.children:
                if type(subtree) != Token:
                    self.hashTree(subtree, id)

    def addTreeHash(self, key, value):
        if self.hashTable.get(key) != None:
            self.addCollision(key, value)
            return True
        else:
            self.hashTable.update({key:value})
            return False

    def addCollision(self, key, value):
        id = value.id
        if self.collisions.get(key) != None:
            self.collisions.get(key)[id].append(value)
        else:
            list = [ [] for _ in range(self.__size) ]
            list[self.hashTable.get(key).id].append(self.hashTable.get(key))
            list[id].append(value)
            self.collisions.update({key:list})
    
    def updateCollisionSize(self, n):
        for key, vals in self.collisions.items():
            for _ in range(n):
                vals.append([])

    def reset(self):
        self.hashTable = {}
        self.collisions = {}
        self.results = []
        self.weights = []
        self.__size += 0
