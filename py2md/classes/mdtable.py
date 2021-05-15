from typing import List
from .mdobject import MDObject
from .mdlist import MDList

class MDTable(MDObject):
    columns: List[MDList] = None
    numrows: int = None
    def __init__(self):
        self.columns = []
        self.numrows = 0
    def add_column(self, header: str, frmstr: str, halign: str='', data: list=[]):
        from .mdlist import MDList
        mdlist = MDList(header, frmstr, halign)
        for di in data:
            mdlist.add_value(di)
        if len(self.columns) == 0:
            self.numrows = mdlist.numval
            self.columns.append(mdlist)
        elif mdlist.numval == self.numrows:
            self.columns.append(mdlist)
    def add_row(self, data):
        if len(data) != len(self.columns):
            raise IndexError
        else:
            self.numrows += 1
            for i, column in enumerate(self.columns):
                column.add_value(data[i])
    def __str__(self):
        mdstr = '\n|'
        for column in self.columns:
            mdstr += ' ' + column.header_string() + ' |'
        mdstr += '\n'
        mdstr += '|'
        for column in self.columns:
            mdstr += ' ' + column.align_string() + ' |'
        mdstr += '\n'
        for i in range(self.numrows):
            mdstr += '|'
            for column in self.columns:
                mdstr += ' ' + column.value_string(i) + ' |'
            mdstr += '\n'
        return mdstr
    def __repr__(self):
        return '<MDTable>'
