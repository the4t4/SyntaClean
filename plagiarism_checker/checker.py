from lark.lexer import Token
from hashlib import md5

from plagiarism_checker.fingerprint import Fingerprint
from plagiarism_checker.utils import treeSize, idGenerator

class PlagiarismCheker():
    def __init__(self, hashTable = {}, collisions = {}):
        self.hashTable = hashTable
        self.collisions = collisions
        self.results = []
        self.fingerprints = []
        self.__size = 0

    def check(self, *trees):
        n = len(trees)
        self.updateSize(n)

        for tree in trees:
            id = next(idGenerator)
            fingerprint = Fingerprint(id, treeSize(tree), tree)
            self.fingerprints.append(fingerprint)
            self.hashTree(fingerprint)

        for fp in self.fingerprints:
            collidedWeights = self.calculateCollidedWeights(fp.node, fp.id)
            similarityList = [0] * self.__size
            for i in range(self.__size):
                similarityList[i] = round(collidedWeights[i]/fp.weight, 2)
            self.results[fp.id] = similarityList

        return self.results

    def hashTree(self, fingerprint):
        hash = self.hashNode(fingerprint.node)
        self.addTreeHash(hash, fingerprint)
        for subtree in fingerprint.node.children:
            if type(subtree) != Token:
                subfp = Fingerprint(fingerprint.id, treeSize(subtree), subtree)
                self.hashTree(subfp)
    
    def hashNode(self, node):
        hash = md5(repr(node).encode('ASCII')).digest()
        return hash

    def addTreeHash(self, key, value):
        if self.hashTable.get(key) != None:
            self.addCollision(key, value)
        else:
            self.hashTable.update({key:value})

    def addCollision(self, key, value):
        id = value.id
        if self.collisions.get(key) != None:
            self.collisions.get(key)[id].append(value)
        else:
            list = [ [] for _ in range(self.__size) ]
            list[self.hashTable.get(key).id].append(self.hashTable.get(key))
            list[id].append(value)
            self.collisions.update({key:list})

    def calculateCollidedWeights(self, tree, id):
        hash = self.hashNode(tree)
        collisions = self.collisions.get(hash)
        collidedWeights = [0] * self.__size
        blockExtraCollides = [False] * self.__size

        if collisions != None:
            weight = collisions[id][0].weight
            for i in range(self.__size):
                collidedWeight = min(weight, weight * len(collisions[i]))
                if i != id and collidedWeight != 0:
                    collidedWeights[i] += collidedWeight
                    blockExtraCollides[i] = True
        for subtree in tree.children:
            if type(subtree) != Token:
                result = self.calculateCollidedWeights(subtree, id)
                for i in range(self.__size):
                    if not blockExtraCollides[i]:
                        collidedWeights[i] += result[i]

        return collidedWeights
    
    def updateSize(self, n):
        self.__size += n

        for result in self.results:
            for _ in range(n):
                result.append(0.0)

        for _ in range(n):
            self.results.append([0.0] * self.__size)

        for key, vals in self.collisions.items():
            for _ in range(n):
                vals.append([])
    
    def prettyResults(self):
        out = "\t" + "\t".join([" " + str(i) for i in range(self.__size)]) + "\n"
        out += "\t" + "\t".join(["----" for _ in range(self.__size)]) + "\n"
        for i in range(self.__size):
            out += str(i) + "   |\t" + "\t".join([str(j) for j in self.results[i]]) + "\n"
        return out

    def reset(self):
        self.hashTable = {}
        self.collisions = {}
        self.results = []
        self.fingerprints = []
        self.__size = 0
