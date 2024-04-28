from os.path import abspath, split
from re import search
from time import time
from typing import Dict, List

from .jupyter import JupyterKernel
from .output.md import MDWriter


class Py2MD():
    source: str = None
    cells: List[Dict[str, str]] = None
    nocode: bool = None
    nohead: bool = None
    inline: bool = None

    def __init__(self, source: str) -> None:
        self.source = source
        self.read()
        self.nocode = False
        self.nohead = False
        self.inline = False

    def read(self):
        print('Reading {:s}'.format(self.source))
        t0 = time()
        content = ''
        self.cells = []
        with open(self.source, 'rt') as file:
            cell = {}
            linenum = 0
            for line in file:
                line: str = line
                linenum += 1
                if line[0:3] == r'#%%':
                    line = line.replace(r'#%%', '')
                    if len(cell) != 0:
                        cell['content'] = content
                        self.cells.append(cell)
                        content = ''
                    cell = {}
                    if '[markdown]' in line:
                        cell['type'] = 'markdown'
                        line = line.replace('[markdown]', '')
                    else:
                        cell['type'] = 'code'
                        cell['start_line'] = linenum
                    cell['label'] = line.strip()
                else:
                    content += line
        if len(cell) != 0:
            cell['content'] = content
            self.cells.append(cell)
        t1 = time()
        total = t1-t0
        print('Read {:s} in {:g} seconds'.format(self.source, total))

    def print_cells(self) -> None:
        for ind, cell in enumerate(self.cells):
            print('Chunk {:d}'.format(ind))
            if 'type' in cell:
                print('Type: {:s}'.format(cell['type']))
            if 'content' in cell:
                print('Content:\n{:s}'.format(cell['content']))
            if 'results' in cell:
                print('Results:')
                for result in cell['results']:
                    print('{:}'.format(result))
                print()

    def run(self, mplpng: bool=False) -> None:
        kernel = 'python3'
        curdir = split(abspath(self.source))[0]

        jk = JupyterKernel(kernel, curdir)
        jk.start_kernel()
        jk.start_client()

        jk.run_code('%matplotlib inline')
        jk.run_code('from IPython.display import set_matplotlib_formats')
        if mplpng:
            jk.run_code('set_matplotlib_formats("png")')
        else:
            jk.run_code('set_matplotlib_formats("svg")')

        for ind, cell in enumerate(self.cells):
            if cell['type'] == 'code':
                t0 = time()
                cell['results'] = jk.run_cell(cell)
                t1 = time()
                total = t1-t0
                print('Executed code cell {:d} in {:g} seconds'.format(ind, total))
            if cell['type'] == 'markdown':
                t0 = time()
                content = cell['content']
                content = cleanup_markdown(content)
                result = {'output_type': 'display_data', 'data': []}
                result['data'] = {'text/markdown': content}
                cell['results'] = [result]
                t1 = time()
                total = t1-t0
                print(f'Outputting markdown cell {ind:d} in {total:g} seconds')

        jk.stop_client()
        jk.stop_kernel()

    def write_file(self, inline: bool=False,
                   nocode: bool=False,
                   nohead: bool=False) -> None:
        destination = self.source + '.md'
        print('Writing {:s}'.format(destination))
        t0 = time()
        mdwriter = MDWriter(destination)
        mdwriter.open_file()
        for cell in self.cells:
            mdwriter.write_cell(cell, inline, nocode, nohead)
        mdwriter.close_file()
        t1 = time()
        total = t1-t0
        print('Wrote {:s} in {:g} seconds'.format(destination, total))
        
    def __repr__(self) -> str:
        return '<py2md.Py2MD>'

def cleanup_markdown(instr: str) -> str:
    contentsplit = instr.split('\n')
    mdstr = ''
    for line in contentsplit:
        if line.strip() != '':
            mdstr += line[2:] + '\n'
    return mdstr

def replace_outline_latex(instr: str, begstr: str,
                          endstr: str) -> str:
    newstr = instr
    poslst = []
    match = search(r'\$\$', newstr)
    while match is not None:
        poslst.append(match.regs[0])
        newstr = newstr[match.regs[0][1]:]
        match = search(r'\$\$', newstr)
    newposlst = []
    newpos = (0, 0)
    for pos in poslst:
        newpos = (pos[0]+newpos[1], pos[1]+newpos[1])
        newposlst.append(newpos)
    newposlst.reverse()
    beg, end = False, True
    for pos in newposlst:
        if end:
            instr = instr[0:pos[0]]+endstr+instr[pos[1]:]
        if beg:
            instr = instr[0:pos[0]]+begstr+instr[pos[1]:]
        beg, end = end, beg
    return instr
