class Unit(list):
    """object mapping to each no-empty line of corpus"""
    def __init__(self, *args, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)
        self.id = kwargs.get('id')

    def __repr__(self):
        return "{cls}({list}, id={id})".format(
            cls=self.__class__,
            list=super(Unit, self).__repr__(),
            id=self.id
        )
