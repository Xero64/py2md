from .mdlist import MDList
from .mdobject import MDObject
from .mdparamlist import MDParamList


class MDParamTable(MDObject):
    labels: MDList = None
    values: MDParamList = None
    units: MDList = None
    numrows: int = None

    def __init__(self) -> None:
        self.labels = MDList('Parameter', 's')
        self.values = MDParamList('Value')
        self.units = MDList('Unit', 's')
        self.numrows = 0

    def add_param(self, label: str, value: str, valfrm: str, unit: str) -> None:
        self.numrows += 1
        self.labels.add_value(label)
        self.values.add_value(value, valfrm)
        self.units.add_value(unit)

    def _repr_markdown_(self) -> str:
        mdstr = '\n|'
        mdstr += ' ' + self.labels.header_string() + ' |'
        mdstr += ' ' + self.values.header_string() + ' |'
        mdstr += ' ' + self.units.header_string() + ' |'
        mdstr += '\n|'
        mdstr += ' ' + self.labels.align_string() + ' |'
        mdstr += ' ' + self.values.align_string() + ' |'
        mdstr += ' ' + self.units.align_string() + ' |'
        mdstr += '\n'
        for i in range(self.numrows):
            mdstr += '|'
            mdstr += ' ' + self.labels.value_string(i) + ' |'
            mdstr += ' ' + self.values.value_string(i) + ' |'
            mdstr += ' ' + self.units.value_string(i) + ' |'
            mdstr += '\n'
        mdstr += '\n<br/>\n'
        return mdstr

    def __str__(self) -> str:
        outstr = '\n|'
        outstr += ' ' + self.labels.header_string() + ' |'
        outstr += ' ' + self.values.header_string() + ' |'
        outstr += ' ' + self.units.header_string() + ' |'
        outstr += '\n|'
        outstr += ' ' + self.labels.align_string() + ' |'
        outstr += ' ' + self.values.align_string() + ' |'
        outstr += ' ' + self.units.align_string() + ' |'
        outstr += '\n'
        for i in range(self.numrows):
            outstr += '|'
            outstr += ' ' + self.labels.value_string(i) + ' |'
            outstr += ' ' + self.values.value_string(i) + ' |'
            outstr += ' ' + self.units.value_string(i) + ' |'
            outstr += '\n'
        return outstr

    def __repr__(self) -> str:
        return '<py2md.MDParamTable>'
