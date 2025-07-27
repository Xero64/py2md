class MDObject():

    def to_mdfile(self, mdfilepath: str, mode: str = 'wt', **kwargs) -> None:
        if 'encoding' not in kwargs:
            kwargs['encoding'] = 'UTF-8'
        with open(mdfilepath, mode, **kwargs) as mdfile:
            mdfile.write(self._repr_markdown_())

    def to_mdreport(self) -> str:
        return self._repr_markdown_()

    def _repr_markdown_(self) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return '<py2md.MDObject>'
