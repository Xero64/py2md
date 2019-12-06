class MDHeading(object):
    heading = None
    level = None
    def __init__(self, heading: str, level: int):
        self.heading = heading
        self.level = level
    def __str__(self):
        mdstr = ''
        for _ in range(self.level):
            mdstr += '#'
        mdstr += ' '
        mdstr += self.heading
        mdstr += '\n'
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
    def __repr__(self):
        return '<MDHeading>'
