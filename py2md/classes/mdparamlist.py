from typing import Any, List

from .mdobject import MDObject


class MDParamList(MDObject):
    header: str = None
    halign: str = None
    values: List[Any] = None
    valfrm: List[str] = None
    length: int = None
    numval: int = None

    def __init__(self, header: str, halign: str='') -> None:
        self.header = header
        self.halign = halign
        self.values = []
        self.valfrm = []
        self.numval = 0
        self.length = max(len(self.header), 3)

    def add_value(self, value: Any, valfrm: str) -> None:
        self.values.append(value)
        self.valfrm.append(valfrm)
        self.numval = len(self.values)
        try:
            string = value.__format__(valfrm)
        except TypeError:
            err = f'Value {value} cannot be formatted with {valfrm}.'
            raise TypeError(err)
        strlen = len(string)
        if strlen > self.length:
            self.length = strlen

    def __getitem__(self, ind: int) -> Any:
        if ind < len(self.values):
            return self.values[ind]
        else:
            raise IndexError

    def header_string(self) -> str:
        frmstr = '{:' + self.halign + str(self.length) + 's}'
        return frmstr.format(self.header)

    def align_string(self) -> str:
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
            frmstr = ':{:' + str(self.length-2) + 's}:'
            char = ''
        else:
            frmstr = '{:' + self.halign + str(self.length) + 's}'
            char = ':'
        return frmstr.format(char).replace(' ', '-')

    def value_string(self, ind: int) -> str:
        if ind < len(self.values):
            frmstr = '{:' + self.halign + str(self.length) + self.valfrm[ind] + '}'
            return frmstr.format(self.values[ind])
        else:
            raise IndexError

    def _repr_markdown_(self) -> str:
        mdstr = '\n'
        mdstr += '| ' + self.header_string() + ' |\n'
        mdstr += '| ' + self.align_string() + ' |\n'
        for i in range(self.numval):
            mdstr += '| ' + self.value_string(i) + ' |\n'
        mdstr += '\n<br/>\n'
        return mdstr

    def __str__(self) -> str:
        outstr = '\n'
        outstr += '| ' + self.header_string() + ' |\n'
        outstr += '| ' + self.align_string() + ' |\n'
        for i in range(self.numval):
            outstr += '| ' + self.value_string(i) + ' |\n'
        return outstr

    def __repr__(self) -> str:
        return f'<py2md.MDParamList: {self.header:s}>'
