class MDHeading(object):
    heading = None
    level = None
    def __init__(self, heading: str, level: int):
        self.heading = heading
        self.level = level
    def _repr_markdown_(self):
        mdstr = ''
        for _ in range(self.level):
            mdstr += '#'
        mdstr += ' '
        mdstr += self.heading
        mdstr += '\n'
        return mdstr
