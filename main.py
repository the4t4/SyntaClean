import sys

from hashlib import md5

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel
from plagiarism_checker.checker import naiveCheck


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("py main.py <inputfile1> <inputfile2>")
        sys.exit(2)
    f1 = open(sys.argv[1])
    f2 = open(sys.argv[2])
    parser = CleanParser(abstractionLevel=AbstractionLevel.SIMPLE)
    tree1 = parser.parse(f1.read())
    tree2 = parser.parse(f2.read())
    print(md5(repr(tree1).encode('ASCII')).digest())
    print(md5(repr(tree2).encode('ASCII')).digest())
    result = naiveCheck(tree1, tree2)
    print(result)
