from .mdobject import MDObject

class MDString(MDObject):
    string: str = None

    def __init__(self, string: str) -> None:
        self.string = string

    def __str__(self) -> str:
        return self.string
    
    def __repr__(self) -> str:
        return '<py2md.MDString>'
