class Singleton(object):
    INSTANCE = None
    def __new__(cls, *args, **kwargs):
        if not cls.INSTANCE:
            cls.INSTANCE = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.INSTANCE
