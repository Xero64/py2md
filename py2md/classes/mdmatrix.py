from numpy.matlib import matrix

class MDMatrix(object):
    label = None
    matrix = None
    frmstr = None
    def __init__(self, label: str, matrix: matrix, frmstr: str):
        self.label = label
        self.matrix = matrix
        self.frmstr = frmstr
    def __str__(self):
        mdstr = '$$\n'
        mdstr += '{:s} = \n'.format(self.label)
        mdstr += '\\begin{bmatrix}\n'
        shp = self.matrix.shape
        for i in range(shp[0]):
            for j in range(shp[1]):
                value = self.matrix[i, j]
                mdstr += value.__format__(self.frmstr)
                if j == shp[1]-1:
                    mdstr += ' \\\\\n'
                else:
                    mdstr += ' && '
        mdstr += '\\end{bmatrix}\n$$\n'
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
    def __repr__(self):
        return '<MDMatrix>'
