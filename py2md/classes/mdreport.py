from typing import List
from .mdobject import MDObject

class MDReport(MDObject):
    objs: List[MDObject] = None
    def __init__(self):
        self.objs = []
    def add_object(self, obj: MDObject):
        if isinstance(obj, MDObject):
            self.objs.append(obj)
        else:
            return ValueError('Not a valid MDObject.')
    def __str__(self):
        mdstr = ''
        for obj in self.objs:
            mdstr += obj.__str__()
        return mdstr
    def __repr__(self):
        return '<MDReport>'
