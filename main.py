import sys

from clean_parser.parser import parser, TokenRemover
from plagiarism_checker.checker import naiveCheck

if __name__ == "__main__":
    try:
        f1 = open(sys.argv[1])
        f2 = open(sys.argv[2])
    except IndexError:
        print("py main.py <inputfile1> <inputfile2>")
        sys.exit(2)
    tree1 = parser.parse(f1.read())
    tree2 = parser.parse(f2.read())
    TokenRemover().transform(tree1)
    TokenRemover().transform(tree2)    
    result = naiveCheck(tree1, tree2)
    print(result)
