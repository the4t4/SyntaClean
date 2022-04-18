import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from clean_parser.parser import CleanParser

import unittest
from unittest import TestCase

resourceDir = "resources"

parser = CleanParser()

class TestParser(TestCase):
    def test_parser(self):
        for filename in os.listdir(resourceDir):
            file = os.path.join(resourceDir, filename)
            try:
                f = open(file)
                tree = parser.parse(f.read())
                # parser.make_png(tree, "png/" + filename[:-4] + ".png")
            except Exception as e:
                self.fail("Could not parse " + file + ":\n" + str(e))
            f.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        f = open(sys.argv[1])
        tree = parser.parse(f.read())
        print(tree.pretty())
