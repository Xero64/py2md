from typing import TYPE_CHECKING

from .mdobject import MDObject
from io import StringIO

if TYPE_CHECKING:
    from matplotlib.figure import Figure

class MDFigure(MDObject):
    fig: 'Figure' = None
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
    def __repr__(self) -> str:
        return '<py2md.MDFigure>'
