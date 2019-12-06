from sys import argv

def main():
    if len(argv) == 1:
        print('Specify a .py file to run and create a .py.md output file.')
        print('Use --debug to debug py2md process.')
        return
    
    from .py2md import Py2MD
    if argv[1][-3:] == '.py':
        py2md = Py2MD(argv[1])
        py2md.run()
        if len(argv) > 2:
            if argv[2] == '--debug':
                py2md.print_cells()
        py2md.write_file()
