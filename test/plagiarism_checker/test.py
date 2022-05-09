import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from clean_parser.parser import CleanParser
from plagiarism_checker.checker import PlagiarismCheker

import unittest
from unittest import TestCase

resourceDir = "resources"

parser = CleanParser()
checker = PlagiarismCheker()

class TestChecker(TestCase):
    def test_parser(self):
        numOfFiles = len(os.listdir(resourceDir))
        for filename in os.listdir(resourceDir):
            file = os.path.join(resourceDir, filename)
            try:
                f = open(file)
                tree = parser.parse(f.read())
                checker.check([tree], [file])
            except Exception as e:
                self.fail("Could not check " + file + ":\n" + str(e))
            f.close()

        assert(len(checker.similarities) == numOfFiles)
        assert(len(checker.similarities[0]) == numOfFiles)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        for i in range(1, len(sys.argv)):
            f = open(sys.argv[i])
            tree = parser.parse(f.read())
            checker.check(tree)
            print(checker.prettyResults())
