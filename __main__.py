import sys
from .py2md import Py2MD

def main():
    args = sys.argv
    if args[1][-3:] == '.py':
        py2md = Py2MD(args[1])
        py2md.run()
        # py2md.print_cells()
        py2md.write_file()

if __name__ == "__main__":
    main()
