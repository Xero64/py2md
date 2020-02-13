from sys import argv

def main():
    if len(argv) == 1:
        print('Specify a .py file to run and create a .py.md output file.')
        print('Use --debug to debug py2md process.')
        return
    
    from .py2md import Py2MD
    if argv[1][-3:] == '.py':
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
