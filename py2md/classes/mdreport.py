from typing import List
from os.path import split, join

from .mdfigure import MDFigure
from .mdobject import MDObject
from .mdheading import MDHeading
from .mdtable import MDTable


class MDReport(MDObject):
    objs: List['MDObject'] = None

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
