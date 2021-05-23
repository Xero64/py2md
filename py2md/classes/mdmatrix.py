from typing import List
from .mdobject import MDObject

class MDMatrix(MDObject):
    label = None
    matrix = None
    frmstr = None
    def __init__(self, label: str, matrix: List[List[object]], frmstr: str):
        self.label = label
        self.matrix = matrix
        self.frmstr = frmstr
    def __str__(self):
        mdstr = '\n$$\n'
        mdstr += '{:s} = \n'.format(self.label)
        mdstr += '\\begin{bmatrix}\n'
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                value = self.matrix[i][j]
                mdstr += value.__format__(self.frmstr)
                if j == len(row)-1:
                    mdstr += ' \\\\\n'
                else:
                    mdstr += ' && '
        mdstr += '\\end{bmatrix}\n$$\n'
        return mdstr
    def __repr__(self):
        return f'<MDMatrix: {self.label:s}>'
