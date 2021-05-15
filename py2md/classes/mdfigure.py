from .mdobject import MDObject
from io import StringIO

class MDFigure(MDObject):
    fig = None
    frm: str = None
    def __init__(self, fig, frm: str='svg'):
        self.fig = fig
        self.frm = frm
    def __str__(self):
        strio = StringIO()
        self.fig.savefig(strio, format=self.frm)
        data = strio.getvalue()
        ind = data.index('<svg ')
        data = data[ind:]
        strio.close()
        return data
