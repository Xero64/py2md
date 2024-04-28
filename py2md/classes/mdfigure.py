from base64 import b64encode
from io import StringIO, BytesIO
from os import makedirs
from os.path import join, relpath
from typing import TYPE_CHECKING

from matplotlib.pyplot import close

from .mdobject import MDObject

if TYPE_CHECKING:
    from matplotlib.figure import Figure

class MDFigure(MDObject):
    fig: 'Figure' = None
    frm: str = None
    figstr: str = None
    figbyt: bytes = None

    def __init__(self, fig: 'Figure', frm: str='svg') -> None:
        self.fig = fig
        self.frm = frm
        self.store_and_close()

    def store_and_close(self) -> None:
        if self.frm == 'svg':
            strio = StringIO()
            self.fig.savefig(strio, format=self.frm)
            figstr = strio.getvalue()
            strio.close()
            ind = figstr.index('<svg ')
            figstr = figstr[ind:]
            self.figstr = '\n' + figstr + '\n'
        elif self.frm == 'png':
            bytio = BytesIO()
            self.fig.savefig(bytio, format=self.frm)
            figbyt = bytio.getvalue()
            bytio.close()
            self.figbyt = figbyt
        close(self.fig)

    def to_mdreport(self, path: str, mdname: str, figind: int) -> str:
        figpath = join(path, mdname)
        makedirs(figpath, exist_ok=True)
        figname = f'{mdname:s}.{figind:d}'
        figfilename = f'{figname:s}.{self.frm:s}'
        figfilepath = join(figpath, figfilename)
        figrelpath = relpath(figfilepath, path)
        if self.frm == 'svg':
            with open(figfilepath, 'wt') as figfile:
                      figfile.write(self.figstr)
        elif self.frm == 'png':
            with open(figfilepath, 'wb') as imgfile:
                      imgfile.write(self.figbyt)
        figrelpath = relpath(figfilepath, path)
        return f'\n![]({figrelpath:s})\n'

    def _repr_markdown_(self) -> str:
        if self.frm == 'svg':
            return self.figstr
        else:
            pngbyt64 = b64encode(self.figbyt)
            outtext = '\n<img alt="" src="data:image/png;base64,'
            outtext += pngbyt64.decode() + '" />\n'
            return outtext

    def __str__(self) -> str:
        return 'py2md.MDFigure'
    
    def __repr__(self) -> str:
        return '<py2md.MDFigure>'
