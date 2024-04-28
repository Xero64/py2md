from .mdobject import MDObject

class MDHeading(MDObject):
    heading: str = None
    level: int = None

    def __init__(self, heading: str, level: int) -> None:
        self.heading = heading
        self.level = level

    def __str__(self) -> str:
        outstr = '\n'
        for _ in range(self.level):
            outstr += '#'
        outstr += ' '
        outstr += self.heading
        outstr += '\n'
        return outstr

    def __repr__(self) -> str:
        return f'<py2md.MDHeading: {self.heading:s}>'
