class _filter:
    def __init__(self, val, groupBy=True):
        self.value = val
        self.group_by = groupBy

    def m(self):
        if self.__class__ == _filter:
            raise NotImplementedError()
        return f'{self.__class__.__name__}({self.value})'


class literal_or(_filter):
    pass


class iliteral_or(_filter):
    pass


class wildcard(_filter):
    pass


class regexp(_filter):
    pass


class not_key(_filter):
    def __init__(self):
        super().__init__("", True)
