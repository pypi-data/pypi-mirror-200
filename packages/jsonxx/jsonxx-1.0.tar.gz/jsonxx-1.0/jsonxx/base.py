class ExtensionBase:

    classes = {}

    def __init_subclass__(cls):
        for cl in cls.mro():
            if cl not in (cls, ExtensionBase, object):
                ExtensionBase.classes[cls] = cl
                break
        else:
            raise ValueError(
                f"Unable to determine subclassed type for {cls.__name__}")

    def __init__(self, data=None, saver=None):
        super().__init__(data) if data is not None else super().__init__()
        self.saver = saver

    def __getitem__(self, item):
        result = self.get(item)
        klass = self.get_class(result, init=False)
        if isinstance(result, tuple(self.classes.values())):
            klass = klass(result, saver=self.save)
            self.setitem(item, klass, False)
            return klass
        return result

    def __setitem__(self, item, value, save=True):
        super().__setitem__(item, value)
        if save:
            self.save(self)

    def __delitem__(self, item):
        super().__delitem__(item)
        self.save()

    setitem = __setitem__

    def save(self, _=None):
        if self.saver is not None and callable(self.saver):
            return self.saver(self)

    @classmethod
    def get_class(cls, data, *args, init=True, **kwargs):
        for klass, cl in cls.classes.items():
            if isinstance(data, cl):
                return klass(data, *args, **kwargs) if init else klass
        return data
