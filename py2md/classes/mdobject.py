class MDObject():
    def to_mdfile(self, mdfilepath: str, **kwargs) -> None:
        if 'mode' not in kwargs:
            kwargs['mode'] = 'wt'
        if 'encoding' not in kwargs:
            kwargs['encoding'] = 'UTF-8'
        with open(mdfilepath, **kwargs) as mdfile:
            mdfile.write(self.__str__())
    def _repr_markdown_(self) -> str:
        return self.__str__()
    def __repr__(self) -> str:
        return '<py2md.MDObject>'
