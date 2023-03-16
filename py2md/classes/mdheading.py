from .mdobject import MDObject

class MDHeading(MDObject):
    heading: str = None
    level: int = None
    def __init__(self, heading: str, level: int) -> None:
        self.heading = heading
        self.level = level
    def __str__(self) -> str:
        mdstr = '\n'
        for _ in range(self.level):
            mdstr += '#'
        mdstr += ' '
        mdstr += self.heading
        mdstr += '\n'
        return mdstr
    def __repr__(self) -> str:
        return f'<py2md.MDHeading: {self.heading:s}>'
