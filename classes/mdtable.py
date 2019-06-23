class MDTable(object):
    columns = None
    numrows = None
    def __init__(self):
        self.columns = []
        self.initialise()
    def initialise(self):
        self.numrows = 0
    def add_column(self, header: str, frmstr: str, halign: str=''):
        from .mdlist import MDList
        mdlist = MDList(header, frmstr, halign)
        self.columns.append(mdlist)
    def add_row(self, data):
        if len(data) != len(self.columns):
            raise IndexError
        else:
            self.numrows += 1
            for i, column in enumerate(self.columns):
                column.add_value(data[i])
    def _repr_markdown_(self):
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
