from dataclasses import field
import sys, os

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel
from plagiarism_checker.checker import PlagiarismCheker

parser = CleanParser(abstractionLevel=AbstractionLevel.NONE)
checker = PlagiarismCheker(threshold=0.3)

def parseFile(file, generatePng=False):
    extension = file[-4:]
    if extension == ".icl":
        try:
            f = open(file)
            tree = parser.parse(f.read())
            if generatePng:
                parser.make_png(tree, extension + ".png")
            return tree
        except Exception as e:
            print("Could not parse " + file + ":\n" + str(e))
        f.close()

def parseFolder(folder, generatePng=False):
    trees = []
    files = []
    for filename in os.listdir(folder):
        file = os.path.join(folder, filename)
        tree = parseFile(file, generatePng)
        trees.append(tree)
        files.append(file)

    return (trees, files)

def setBaseFile(baseFile):
    tree = parseFile(baseFile)
    checker.setBaseTree(tree)

def main(argv, pretty=False):
    allTrees = []
    allFiles = []

    for arg in argv:
        if os.path.isdir(arg):
            trees, files = parseFolder(arg)
            allTrees += trees
            allFiles += files
        else:
            tree = parseFile(arg)
            allTrees.append(tree)
            allFiles.append(arg)
    
    results = checker.check(allTrees, allFiles)
    similarities, fingerprints = checker.getReport()
    if pretty:
        print(checker.prettyReport())
    return (results, similarities, fingerprints)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("py main.py <file1/dir1> ... <fileN/dirN>")
        sys.exit(2)
    main(sys.argv[1:], True)