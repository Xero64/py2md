from typing import List
from .mdobject import MDObject

class MDList(object):
    header: str = None
    frmstr: str = None
    halign: str = None
    values: List[object] = None
    length: int = None
    numval: int = None
    def __init__(self, header: str, frmstr: str, halign: str=''):
        self.header = header
        self.frmstr = frmstr
        self.halign = halign
        self.values = []
        self.numval = 0
        self.length = len(self.header)
    def add_value(self, value):
        self.values.append(value)
        self.numval = len(self.values)
        string = value.__format__(self.frmstr)
        strlen = len(string)
        if strlen > self.length:
            self.length = strlen
    def __getitem__(self, ind: int):
        if ind < len(self.values):
            return self.values[ind]
        else:
            raise IndexError
    def header_string(self):
        frmstr = '{:'+self.halign+str(self.length)+'s}'
        return frmstr.format(self.header)
    def align_string(self):
        if self.length == 1:
            return ':'
        elif self.length == 2:
            if self.halign == '<':
                return ':-'
            elif self.halign == '>':
                return '-:'
            else:
                return '::'
        elif self.halign == '':
            frmstr = ':{:'+str(self.length-2)+'s}:'
            char = ''
        else:
            frmstr = '{:'+self.halign+str(self.length)+'s}'
            char = ':'
        return frmstr.format(char).replace(' ', '-')
    def value_string(self, ind: int):
        if ind < len(self.values):
            frmstr = '{:'+self.halign+str(self.length)+self.frmstr+'}'
            return frmstr.format(self.values[ind])
        else:
            raise IndexError
    def __str__(self):
        mdstr = '\n'
        mdstr += '| ' + self.header_string() + ' |\n'
        mdstr += '| ' + self.align_string() + ' |\n'
        for i in range(self.numval):
            mdstr += '| ' + self.value_string(i) + ' |\n'
        return mdstr
    def __repr__(self):
        return f'<MDList: {self.header:s}>'
