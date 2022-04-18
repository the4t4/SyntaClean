import sys, os

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel
from plagiarism_checker.checker import PlagiarismCheker


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("py main.py <file1/dir1> ... <fileN/dirN>")
        sys.exit(2)

    parser = CleanParser(abstractionLevel=AbstractionLevel.NONE)
    checker = PlagiarismCheker()
    trees = []
    files = []

    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for filename in os.listdir(arg):
                file = os.path.join(arg, filename)
                try:
                    f = open(file)
                    tree = parser.parse(f.read())
                    trees.append(tree)
                    files.append(file)
                    # parser.make_png(tree, "png/" + filename[:-4] + ".png")
                except Exception as e:
                    print("Could not parse " + file + ":\n" + str(e))
                f.close()
        else:
            try:
                f = open(arg)
                tree = parser.parse(f.read())
                trees.append(tree)
                files.append(arg)
                # parser.make_png(tree, "png/" + filename[:-4] + ".png")
            except Exception as e:
                print("Could not parse " + arg + ":\n" + str(e))
            f.close()
    
    checker.check(trees, files)

    print(checker.prettyResults())
