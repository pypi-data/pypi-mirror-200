from typing import Union

__version__ = "0.4.0"


RODICT_ENABLED_ATTRS: set = {
    "__class__",
    "__contains__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getitem__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__iter__",
    "__le__",
    "__len__",
    "__lt__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "copy",
    "fromkeys",
    "get",
    "items",
    "keys",
    "values",
}

ROLIST_ENABLED_ATTRS: set = {
    "__class__",
    "__contains__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getitem__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__iter__",
    "__le__",
    "__len__",
    "__lt__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "copy",
    "count",
    "index",
}

ROSET_ENABLED_ATTRS: set = {
    "__and__",
    "__class__",
    "__contains__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__iter__",
    "__le__",
    "__len__",
    "__lt__",
    "__ne__",
    "__new__",
    "__or__",
    "__rand__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__ror__",
    "__rsub__",
    "__rxor__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "__xor__",
    "copy",
    "difference",
    "intersection",
    "isdisjoint",
    "issubset",
    "issuperset",
    "symmetric_difference",
    "union",
}


def roview(
    obj,
    enabled_attrs: Union[set, tuple, list] = None,
    disabled_attrs: Union[set, tuple, list] = None,
    nested: bool = False,
):
    if enabled_attrs is not None and disabled_attrs is not None:
        raise ValueError("Only one of ('enabled_attrs', 'disabled_attrs') are allowed, not both")
    if not enabled_attrs and not disabled_attrs:
        raise ValueError("'enabled_attrs' or 'disabled_attrs' should be not empty")

    class Meta(type):
        @classmethod
        def __prepare__(cls, name: str, bases):
            dct: dict = {}

            def make_proxy(attr: str):
                def proxy_method(cls_or_self, *args, **kwds):
                    if hasattr(cls_or_self, "__original__"):
                        o = getattr(cls_or_self.__original__, attr)(*args, **kwds)
                        if nested:
                            if isinstance(o, list):
                                return rolist(o, nested=True)
                            if isinstance(o, dict):
                                return rodict(o, nested=True)
                            if isinstance(o, set):
                                return roset(o, nested=True)
                        return o
                    else:
                        return getattr(cls_or_self, attr)(*args, **kwds)

                proxy_method.__qualname__ = getattr(obj, attr).__qualname__
                return proxy_method

            def make_attribute_error(attr: str):
                def attribute_error(cls_or_self, *args, **kwds):
                    raise AttributeError("Attribute '%s' is not enabled" % attr)

                attribute_error.__qualname__ = getattr(obj, attr).__qualname__
                return attribute_error

            for attr in dir(obj):
                if attr in {
                    "__getattribute__",
                    "__class__",
                    "__init__",
                    "__init_subclass__",
                    "__new__",
                }:
                    continue
                if not callable(getattr(obj, attr)):
                    continue
                if enabled_attrs is not None:
                    if attr in enabled_attrs:
                        dct[attr] = make_proxy(attr)
                    else:
                        dct[attr] = make_attribute_error(attr)
                elif disabled_attrs is not None:
                    if attr in disabled_attrs:
                        dct[attr] = make_attribute_error(attr)
                    else:
                        dct[attr] = make_proxy(attr)

            return dct

    class ROView(obj.__class__, metaclass=Meta):
        __slots__ = ("__original__",)

        def __init__(self, *args, **kwds):
            object.__setattr__(self, "__original__", obj.__class__(*args, **kwds))

        def __getattr__(self, attr):
            return getattr(obj, attr)

        def __eq__(self, other):
            if hasattr(other, "__original__"):
                return self.__original__ == other.__original__
            return self.__original__ == other

        def __ne__(self, other):
            if hasattr(other, "__original__"):
                return self.__original__ != other.__original__
            return self.__original__ != other

    proxy = type(
        f"{obj.__class__.__name__}ROView",
        (ROView,),
        {} if hasattr(obj, "__dict__") else {"__slots__": ("__original__",)},
    )()
    if hasattr(obj, "__dict__"):
        object.__setattr__(proxy, "__dict__", rodict(obj.__dict__))
    object.__setattr__(proxy, "__original__", obj)
    return proxy


def rodict(obj, nested: bool = False):
    return roview(obj, enabled_attrs=RODICT_ENABLED_ATTRS, nested=nested)


def rolist(obj, nested: bool = False):
    return roview(obj, enabled_attrs=ROLIST_ENABLED_ATTRS, nested=nested)


def roset(obj, nested: bool = False):
    return roview(obj, enabled_attrs=ROSET_ENABLED_ATTRS, nested=nested)
