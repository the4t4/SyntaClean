from lark.lexer import Token
from hashlib import md5

from plagiarism_checker.fingerprint import Fingerprint
from plagiarism_checker.utils import treeSize, IDGenerator

class PlagiarismCheker():
    def __init__(self, threshold=0.5):
        self.__size = 0
        self.threshold = threshold
        self.hashTable = {}
        self.baseTreeHash = {}
        self.collisions = {}
        self.results = {}
        self.similarities = []
        self.fingerprints = []
        self.idGenerator = IDGenerator()

    def check(self, trees, files, baseTree=None):
        n = len(trees)
        self.updateSize(n)

        if baseTree is not None:
            self.hashBaseTree(baseTree)

        for i in range(n):
            id = next(self.idGenerator)
            fingerprint = Fingerprint(files[i], id, treeSize(trees[i]), trees[i])
            self.fingerprints.append(fingerprint)
            self.hashFingerprint(fingerprint)

        for fp in self.fingerprints:
            collidedWeights = self.calculateCollidedWeights(fp.node, fp.id)
            similarityList = [0] * self.__size
            for i in range(self.__size):
                similarityList[i] = round(collidedWeights[i]/fp.weight, 2)
            self.similarities[fp.id] = similarityList

        results = self.collectResults()

        return results

    def hashBaseTree(self, baseTree):
        self.baseTreeHash.clear()

        subtrees = baseTree.children[0].children

        for subtree in subtrees:
            hash = self.hashNode(subtree)
            if self.baseTreeHash.get(hash) is None:
                self.baseTreeHash.update({hash:subtree})

    def hashFingerprint(self, fingerprint):
        hash = self.hashNode(fingerprint.node)
        if self.baseTreeHash.get(hash) is not None:
            return
        self.addTreeHash(hash, fingerprint)
        for subtree in fingerprint.node.children:
            if type(subtree) is not Token:
                subfp = Fingerprint(fingerprint.file, fingerprint.id, treeSize(subtree), subtree)
                self.hashFingerprint(subfp)
    
    def hashNode(self, node):
        hash = md5(repr(node).encode('ASCII')).digest()
        return hash

    def addTreeHash(self, key, value):
        if self.hashTable.get(key) is not None:
            self.addCollision(key, value)
        else:
            self.hashTable.update({key:value})

    def addCollision(self, key, value):
        id = value.id
        if self.collisions.get(key) is not None:
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

        if collisions is not None and len(collisions[id]) > 0:
            weight = collisions[id][0].weight
            for i in range(self.__size):
                collidedWeight = min(weight, weight * len(collisions[i]))
                if i != id and collidedWeight != 0:
                    collidedWeights[i] += collidedWeight
                    blockExtraCollides[i] = True
        for subtree in tree.children:
            if type(subtree) is not Token:
                result = self.calculateCollidedWeights(subtree, id)
                for i in range(self.__size):
                    if not blockExtraCollides[i]:
                        collidedWeights[i] += result[i]

        return collidedWeights

    def collectResults(self):
        self.results.clear()
        for row in range(self.__size):
            matches = []
            for col in range(self.__size):
                if self.similarities[row][col] >= self.threshold:
                    matches.append((self.fingerprints[col].file, self.similarities[row][col]))
            if len(matches) > 0:
                self.results.update({self.fingerprints[row].file : matches})
        
        return self.results.copy()
    
    def updateSize(self, n):
        self.__size += n

        for similarity in self.similarities:
            for _ in range(n):
                similarity.append(0.0)

        for _ in range(n):
            self.similarities.append([0.0] * self.__size)

        for key, vals in self.collisions.items():
            for _ in range(n):
                vals.append([])
    
    def prettyReport(self):
        out = "\t" + "\t".join([" " + str(i) for i in range(self.__size)]) + "\n"
        out += "\t" + "\t".join(["----" for _ in range(self.__size)]) + "\n"
        ids = "\n"
        for i in range(self.__size):
            out += str(i).ljust(3) + "   |\t" + "\t".join([str(j) for j in self.similarities[i]]) + "\n"
            ids += str(self.fingerprints[i].id) + " = " + self.fingerprints[i].file + "\n"
        out += ids
        return out

    def reset(self):
        self.__size = 0
        self.hashTable.clear()
        self.baseTreeHash.clear()
        self.collisions.clear()
        self.results.clear()
        self.similarities.clear()
        self.fingerprints.clear()
        self.idGenerator.reset()

    def setThreshold(self, threshold):
        self.threshold = threshold

    def setBaseTree(self, tree):
        self.baseTreeHash.clear()
        self.hashBaseTree(tree)

    def getReport(self):
        return (self.similarities.copy(), self.fingerprints.copy())

    def getResults(self):
        return self.results.copy()
