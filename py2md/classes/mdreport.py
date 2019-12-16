class MDReport(object):
    objs = None
    def __init__(self):
        self.objs = []
    def add_object(self, obj):
        if hasattr(obj, '_repr_markdown_'):
            self.objs.append(obj)
    def __str__(self):
        mdstr = ''
        for obj in self.objs:
            mdstr += obj._repr_markdown_()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
    def __repr__(self):
        return '<MDReport>'
