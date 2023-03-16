from typing import List
from .mdobject import MDObject

class MDReport(MDObject):
    objs: List['MDObject'] = None
    def __init__(self) -> None:
        self.objs = []
    def add_object(self, obj: MDObject) -> 'None':
        if isinstance(obj, MDObject):
            self.objs.append(obj)
        else:
            raise ValueError('Not a valid MDObject.')
    def __str__(self) -> str:
        mdstr = ''
        for obj in self.objs:
            mdstr += obj.__str__()
        return mdstr
    def __repr__(self) -> str:
        return '<py2md.MDReport>'
