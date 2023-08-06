import logging
import importlib
import pkgutil

logger = logging.getLogger(__name__)

class Shortener(object):
    """Base Factory class to create shoreteners instances

    >>> s = Shortener(**kwargs)
    >>> instance = s.shortener_name
    >>> instance.short('http://www.google.com')
    'http://short.url/'

    Available Shorteners can be seen with:

    >>> s = Shortener()
    >>> print(s.available_shorteners)
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        # validate some required fields
        self.kwargs["debug"] = bool(kwargs.pop("debug", False))
        self.kwargs["timeout"] = int(kwargs.pop("timeout", 2))
        self.kwargs["verify"] = bool(kwargs.pop("verify", True))
        module = importlib.import_module("pydlj.shorteners")
        self.available_shorteners = [
            i.name for i in pkgutil.iter_modules(module.__path__)
        ]
        # print(module)
        # print(module.__path__)
        # print(self.available_shorteners)

    def __getattr__(self, attr):
        if attr not in self.available_shorteners:
            return self.__getattribute__(attr)

        # get instance of shortener class
        short_module = importlib.import_module(
            "{}.{}".format("pydlj.shorteners", attr)
        )
        instance = getattr(short_module, "Shortener")(**self.kwargs)

        return instance

class Dlj(Shortener):
    ... 