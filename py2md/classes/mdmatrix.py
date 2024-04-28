from typing import List, Any
from .mdobject import MDObject

class MDMatrix(MDObject):
    label: str = None
    matrix: List[List[Any]] = None
    frmstr: str = None
    
    def __init__(self, label: str, matrix: List[List[Any]],
                 frmstr: str) -> None:
        self.label = label
        self.matrix = matrix
        self.frmstr = frmstr

    def __str__(self) -> str:
        outstr = '\n$$\n'
        outstr += '{:s} = \n'.format(self.label)
        outstr += '\\begin{bmatrix}\n'
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                value = self.matrix[i][j]
                outstr += value.__format__(self.frmstr)
                if j == len(row)-1:
                    outstr += ' \\\\\n'
                else:
                    outstr += ' && '
        outstr += '\\end{bmatrix}\n$$\n'
        return outstr

    def __repr__(self) -> str:
        return f'<py2md.MDMatrix: {self.label:s}>'
