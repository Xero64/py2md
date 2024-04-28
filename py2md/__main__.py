from sys import argv
from .py2md import Py2MD

def main() -> None:

    if len(argv) == 1:
        print('Specify a .py file to run and create a .py.md output file.')
        print('Use -debug to debug py2md process.')
        print('Use -nocode to omit code blocks from output.')
        print('Use -nohead to omit cell headers from output.')
        print('Use -inline to make images internal to the output.')
        print('Use -mplpng to make create png rather than svg images.')

    elif argv[1][-3:] == '.py':
        py2md = Py2MD(argv[1])
        nocode, nohead, inline, debug, mplpng = False, False, False, False, False
        for arg in argv[2:]:
            if arg == '-nocode':
                nocode = True
            elif arg == '-nohead':
                nohead = True
            elif arg == '-inline':
                inline = True
            elif arg == '-debug':
                debug = True
            elif arg == '-mplpng':
                mplpng = True
        py2md.run(mplpng)
        if len(argv) > 2:
            if argv[2] == '-debug':
                py2md.print_cells()
        if debug:
            py2md.print_cells()
        py2md.write_file(inline, nocode, nohead)
        
    else:
        print('A python .py file needs to be supplied as the first argument.')
