![tests](https://github.com/levsh/roview/workflows/tests/badge.svg)

```python
In [1]: from roview import rolist

In [2]: l = [5, 0, 10]

In [3]: ro_l = rolist(l)

In [4]: ro_l
Out[4]: [5, 0, 10]

In [5]: type(ro_l)
Out[5]: roview.listROView

In [6]: isinstance(ro_l, list)
Out[6]: True

In [7]: ro_l.__class__
Out[7]: roview.listROView

In [8]: ro_l.__dict__
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-10-010dbe493c26> in <module>
----> 1 ro_l.__dict__

~/workspace/dev/roview/roview.py in __getattr__(self, attr)
    179 
    180         def __getattr__(self, attr):
--> 181             return getattr(obj, attr)
    182 
    183     proxy = type(

AttributeError: 'list' object has no attribute '__dict__'

In [9]: ro_l.append(555)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-11-98107de6aec9> in <module>
----> 1 ro_l.append(555)

~/workspace/dev/roview/roview.py in attribute_error(cls_or_self, *args, **kwds)
    143             def make_attribute_error(attr: str):
    144                 def attribute_error(cls_or_self, *args, **kwds):
--> 145                     raise AttributeError("Attribute '%s' is not enabled" % attr)
    146 
    147                 attribute_error.__qualname__ = getattr(obj, attr).__qualname__

AttributeError: Attribute 'append' is not enabled

In [10]: ro_l.__original__
Out[10]: [5, 0, 10]

In [11]: l.append(555)

In [12]: ro_l
Out[12]: [5, 0, 10, 555]

In [13]: l = [[]]

In [14]: l_ro = rolist(l, nested=True)

In [15]: l_ro[0].append(1)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-30-128d12d96898> in <module>
----> 1 l_ro[0].append(1)

~/workspace/dev/roview/roview.py in attribute_error(cls_or_self, *args, **kwds)
    143             def make_attribute_error(attr: str):
    144                 def attribute_error(cls_or_self, *args, **kwds):
--> 145                     raise AttributeError("Attribute '%s' is not enabled" % attr)
    146 
    147                 attribute_error.__qualname__ = getattr(obj, attr).__qualname__

AttributeError: Attribute 'append' is not enabled
```

```python
In [1]: from roview import roview

In [2]: class O:
   ...:     def __init__(self):
   ...:         self.x = 0
   ...:

In [3]: o = O()

In [4]: ro_o = roview(o, enabled_attrs=["__str__", "__getattr__"])

In [5]: ro_o.x
Out[5]: 0

In [6]: ro_o.x = 1
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-22-8598cf01a30a> in <module>
----> 1 ro_o.x = 1

~/workspace/dev/roview/roview.py in attribute_error(cls_or_self, *args, **kwds)
    143             def make_attribute_error(attr: str):
    144                 def attribute_error(cls_or_self, *args, **kwds):
--> 145                     raise AttributeError("Attribute '%s' is not enabled" % attr)
    146 
    147                 attribute_error.__qualname__ = getattr(obj, attr).__qualname__

AttributeError: Attribute '__setattr__' is not enabled

In [7]: ro_o.__dict__
Out[7]: {'x': 0}

In [8]: ro_o.__dict__["x"] = 1
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-24-e98ada46ce51> in <module>
----> 1 ro_o.__dict__["x"] = 1

~/workspace/dev/roview/roview.py in attribute_error(cls_or_self, *args, **kwds)
    143             def make_attribute_error(attr: str):
    144                 def attribute_error(cls_or_self, *args, **kwds):
--> 145                     raise AttributeError("Attribute '%s' is not enabled" % attr)
    146 
    147                 attribute_error.__qualname__ = getattr(obj, attr).__qualname__

AttributeError: Attribute '__setitem__' is not enabled

In [8]: o.x = 1

In [9]: ro_o.x
Out[9]: 1
```
