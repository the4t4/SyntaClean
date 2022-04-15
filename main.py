import sys

from clean_parser.parser import parser, WhitespaceRemover
from plagiarism_checker.checker import naiveCheck
from plagiarism_checker.abstraction import AbstractionLevel, applyAbstr


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("py main.py <inputfile1> <inputfile2>")
        sys.exit(2)
    f1 = open(sys.argv[1])
    f2 = open(sys.argv[2])
    tree1 = parser.parse(f1.read())
    tree2 = parser.parse(f2.read())
    WhitespaceRemover().transform(tree1)
    WhitespaceRemover().transform(tree2)
    tree1 = applyAbstr(tree1, AbstractionLevel.COMPLETE)
    tree2 = applyAbstr(tree2, AbstractionLevel.COMPLETE)
    result = naiveCheck(tree1, tree2)
    print(result)
