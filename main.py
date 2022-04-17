import sys

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel
from plagiarism_checker.checker import PlagiarismCheker


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("py main.py <inputfile1> <inputfile2>")
        sys.exit(2)
    f1 = open(sys.argv[1])
    f2 = open(sys.argv[2])
    parser = CleanParser(abstractionLevel=AbstractionLevel.SIMPLE)
    checker = PlagiarismCheker()
    tree1 = parser.parse(f1.read())
    tree2 = parser.parse(f2.read())
    checker.check(tree1, tree2, tree2, tree1)
    print(checker.prettyResults())
