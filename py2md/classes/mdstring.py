from .mdobject import MDObject

class MDString(MDObject):
    string: str = None
    def __init__(self, string: str):
        self.string = string
    def __str__(self):
        return self.string
    def __repr__(self):
        return '<MDString>'
