class MDObject():
    def to_mdfile(self, mdfilepath: str, **kwargs):
        if 'mode' not in kwargs:
            kwargs['mode'] = 'wt'
        if 'encoding' not in kwargs:
            kwargs['encoding'] = 'UTF-8'
        with open(mdfilepath, **kwargs) as mdfile:
            mdfile.write(self.__str__())
    def _repr_markdown_(self):
        return self.__str__()
