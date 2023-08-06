class Entity:
    def __init__(self, **kwargs) -> None:
        self._init_args = kwargs

    def __repr__(self) -> str:
        attrs = {a:self.__dict__[a] for a in self.__dict__ if not a.startswith('__') and not a.startswith('_')}
        return str(attrs)
