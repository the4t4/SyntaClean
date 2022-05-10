from email.policy import default
import sys, os, re
import argparse

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel, strToAbstr
from plagiarism_checker.checker import PlagiarismCheker

parser = CleanParser(abstractionLevel=AbstractionLevel.NONE)
checker = PlagiarismCheker(threshold=0.3, granularity=1)
argparser = argparse.ArgumentParser(description="Plagiarism checker for Clean")

argparser.add_argument("files", help="Files or folders where Clean source code (.icl) reside", action='store', type=str, nargs='+')
argparser.add_argument("-b", "--basefile", help="Base File containing template code", action='store', type=str, nargs='?')
argparser.add_argument("-t", "--threshold", help="Similarity threshold for plagiarism", type=int, default=30)
argparser.add_argument("-g", "--granularity", help="Match granularity", type=int, default=1)
argparser.add_argument("-a", "--abstraction", help="Abstraction level of ASTs", type=str, choices=["none", "simple", "complete"], default="none")
argparser.add_argument("-c", "--create", help="Create graphical ASTs in PNG format", action=argparse.BooleanOptionalAction)
argparser.add_argument("-p", "--pretty", help="Pretty print the results of the execution", action=argparse.BooleanOptionalAction)

def normalize_path(path):
    return os.path.normpath(os.sep.join(re.split(r'\\|/', path)))

def parseFile(file, createPng=False):
    filename = file[:-4]
    extension = file[-4:]
    if extension == ".icl":
        try:
            f = open(file)
            tree = parser.parse(f.read())
            if createPng:
                parser.make_png(tree, filename + ".png")
            return tree
        except Exception as e:
            print("Could not parse " + file + ":\n" + str(e))
        f.close()
    return None

def parseFolder(folder, createPng=False):
    trees = []
    files = []
    for file in os.listdir(folder):
        fileFullPath = os.path.join(folder, file)
        tree = parseFile(fileFullPath, createPng)
        if tree is not None:
            trees.append(tree)
            files.append(fileFullPath)

    return (trees, files)

def setBaseFile(baseFile):
    tree = parseFile(baseFile)
    checker.setBaseTree(tree)

def main(args):
    allTrees = []
    allFiles = []

    parsedArgs = argparser.parse_args(args)

    if parsedArgs.basefile is not None:
        normPathFile = normalize_path(parsedArgs.basefile)
        tree = parseFile(normPathFile)
        if tree is None:
            print("Base file could not be parsed, so it was ignored")
        else:
            checker.setBaseTree(tree)
    
    if parsedArgs.threshold < 0 or parsedArgs.threshold > 100:
        raise argparse.ArgumentTypeError("Threshold must be a value between 0 and 100, inclusive")
    else:
        checker.setThreshold(parsedArgs.threshold / 100)
    
    if parsedArgs.granularity < 1 or parsedArgs.granularity > 10:
        raise argparse.ArgumentTypeError("Granularity must be a value between 1 and 10, inclusive")
    else:
        checker.setGranularity(parsedArgs.granularity)
    
    abstractionLevel = strToAbstr(parsedArgs.abstraction)
    parser.setAbstractionLevel(abstractionLevel)

    for file in parsedArgs.files:
        normpath = normalize_path(file)
        if os.path.isdir(file):
            trees, files = parseFolder(normpath, parsedArgs.create)
            allTrees += trees
            allFiles += files
        else:
            tree = parseFile(normpath, parsedArgs.create)
            allTrees.append(tree)
            allFiles.append(normpath)
    
    results = checker.check(allTrees, allFiles)
    similarities, fingerprints = checker.getReport()
    
    if parsedArgs.pretty:
        print(checker.prettyReport())
    return (results, similarities, fingerprints)

if __name__ == "__main__":
    main(sys.argv[1:])
