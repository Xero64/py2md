from .mdobject import MDObject

class MDHeading(MDObject):
    heading = None
    level = None
    def __init__(self, heading: str, level: int):
        self.heading = heading
        self.level = level
    def __str__(self):
        mdstr = '\n'
        for _ in range(self.level):
            mdstr += '#'
        mdstr += ' '
        mdstr += self.heading
        mdstr += '\n'
        return mdstr
    def __repr__(self):
        return f'<MDHeading: {self.heading:s}>'
