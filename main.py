import sys

from clean_parser.parser import parser, TokenRemover
from plagiarism_checker.checker import naiveCheck

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("py main.py <inputfile1> <inputfile2>")
        sys.exit(2)
    f1 = open(sys.argv[1])
    f2 = open(sys.argv[2])
    tree1 = parser.parse(f1.read())
    tree2 = parser.parse(f2.read())
    result = naiveCheck(tree1, tree2)
    print(result)
