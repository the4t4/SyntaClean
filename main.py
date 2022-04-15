import sys

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel
from plagiarism_checker.checker import naiveCheck, collisionCheck


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("py main.py <inputfile1> <inputfile2>")
        sys.exit(2)
    f1 = open(sys.argv[1])
    f2 = open(sys.argv[2])
    parser = CleanParser(abstractionLevel=AbstractionLevel.SIMPLE)
    tree1 = parser.parse(f1.read())
    tree2 = parser.parse(f2.read())
    result1 = naiveCheck(tree1, tree2)
    result2_1, result2_2 = collisionCheck(tree1, tree2)
    print(result1)
    print(result2_1, result2_2)   
