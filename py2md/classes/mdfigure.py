from io import StringIO

class MDFigure(object):
    fig = None
    frm = None
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
    def _repr_markdown_(self):
        return self.__str__()
