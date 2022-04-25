import sys, os

from clean_parser.parser import CleanParser
from clean_parser.abstraction import AbstractionLevel
from plagiarism_checker.checker import PlagiarismCheker

parser = CleanParser(abstractionLevel=AbstractionLevel.NONE)
checker = PlagiarismCheker(threshold=0.3)

def main(argv):
    trees = []
    files = []

    for arg in argv:
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
                # parser.make_png(tree, arg[:-4] + ".png")
            except Exception as e:
                print("Could not parse " + arg + ":\n" + str(e))
            f.close()
    
    results = checker.check(trees, files)
    similarities, fingerprints = checker.getReport()
    return (results, similarities, fingerprints)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("py main.py <file1/dir1> ... <fileN/dirN>")
        sys.exit(2)
    main(sys.argv[1:])