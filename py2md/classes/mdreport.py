from os.path import join, split
from typing import Any

from .mdfigure import MDFigure
from .mdheading import MDHeading
from .mdlist import MDList
from .mdmatrix import MDMatrix
from .mdobject import MDObject
from .mdparamlist import MDParamList
from .mdparamtable import MDParamTable
from .mdtable import MDTable


class MDReport(MDObject):
    objs: list['MDObject'] = None

    def __init__(self) -> None:
        self.objs = []

    def add_object(self, obj: MDObject) -> 'None':
        if isinstance(obj, MDObject):
            self.objs.append(obj)
        else:
            raise ValueError('Not a valid MDObject.')

    def to_mdfile(self, mdfilepath: str, mode: str = 'wt', **kwargs) -> None:
        if 'encoding' not in kwargs:
            kwargs['encoding'] = 'UTF-8'
        mdfilepathsplit = tuple(split(mdfilepath))
        figname = mdfilepathsplit[-1].replace('.md', '')
        path = join(*mdfilepathsplit[:-1])
        outstr, _ = self.to_mdreport(path, figname)
        with open(mdfilepath, mode, **kwargs) as mdfile:
            mdfile.write(outstr)

    def to_mdreport(self, path: str, mdname: str,
                    figind: int=0) -> str:
        outstr = ''
        for obj in self.objs:
            if isinstance(obj, MDReport):
                repstr, figind = obj.to_mdreport(path, mdname, figind)
                outstr += repstr
            elif isinstance(obj, MDFigure):
                figind += 1
                outstr += obj.to_mdreport(path, mdname, figind)
            else:
                outstr += obj.to_mdreport()
        return outstr, figind

    def add_heading(self, heading: str, level: int) -> MDHeading:
        heading = MDHeading(heading, level)
        self.add_object(heading)

    def add_table(self) -> MDTable:
        table = MDTable()
        self.add_object(table)
        return table

    def add_paramtable(self) -> MDParamTable:
        paramtable = MDParamTable()
        self.add_object(paramtable)
        return paramtable

    def add_paramlist(self, header: str, frmstr: str) -> MDParamList:
        paramlist = MDParamList(header, frmstr)
        self.add_object(paramlist)
        return paramlist

    def add_list(self, header: str, frmstr: str, halign: str='') -> MDList:
        mdlist = MDList(header, frmstr, halign)
        self.add_object(mdlist)
        return mdlist

    def add_figure(self, figpath: str, caption: str) -> MDFigure:
        figure = MDFigure(figpath, caption)
        self.add_object(figure)
        return figure

    def add_report(self) -> 'MDReport':
        report = MDReport()
        self.add_object(report)
        return report

    def add_matrix(self, label: str, data: list[list[Any]],
                   frmstr: str = '') -> MDMatrix:
        mdmatrix = MDMatrix(label, data, frmstr)
        self.add_object(mdmatrix)
        return mdmatrix

    def _repr_markdown_(self) -> str:
        mdstr = ''
        for obj in self.objs:
            mdstr += obj._repr_markdown_()
        return mdstr

    def __str__(self) -> str:
        outstr = ''
        for obj in self.objs:
            outstr += obj.__str__()
        return outstr

    def __repr__(self) -> str:
        return '<py2md.MDReport>'
