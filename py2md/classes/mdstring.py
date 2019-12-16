class MDString(object):
    string = None
    def __init__(self, string: str):
        self.string = string
    def __str__(self):
        return self.string
    def _repr_markdown_(self):
        return self.__str__()
    def __repr__(self):
        return '<MDString>'
