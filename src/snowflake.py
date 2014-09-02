# -*- coding: utf-8 -*-


"""
========================
Snowflake Design Pattern
========================

:Authors:
    Moritz Emanuel Beber
:Date:
    2013-03-20
:Copyright:
    Copyright |c| 2013, Moritz Emanuel Beber, all rights reserved.
:File:
    snowflake.py

.. |c| unicode:: U+A9
"""


__all__ = ["Snowflake"]
__version__ = "0.1.0"


class MetaFlake(type):
    """
    Metaclass for Snowflake.

    This metaclass is one of two possible solutions to having a per-class
    dictionary that stores existing instances of that class. The per-class
    aspect is tricky because ``_memory`` is a mutable object. It would normally be
    shared among ``Snowflake`` and all its subclasses.

    Shared state of the ``_memory`` variable is avoided with this metaclass by
    creating each class with a different empty dict.

    Overriding the ``__call__`` method ensures that existing instances (identified
    by ``unique_id``) are not re-initialised with different arguments.
    """
    def __new__(mcls, cls_name, cls_bases, cls_dct):
        """
        Adds a unique `dict` to each class.
        """
        cls_dct["_memory"] = dict()
        return super(MetaFlake, mcls).__new__(mcls, cls_name, cls_bases, cls_dct)

    def __call__(cls, unique_id="", namespace="default", **kw_args):
        """
        Returns an existing instance identified by ``unique_id`` or instantiates
        a new one.
        """
        memory = cls._memory.setdefault(namespace, dict())
        if unique_id in memory:
            return memory[unique_id]
        else:
            cls._counter += 1
            return super(type(cls), cls).__call__(unique_id=unique_id,
                    namespace=namespace, **kw_args)

    def __getitem__(cls, item):
        if isinstance(item, tuple):
            return cls._memory[item[1]][item[0]]
        else:
            return cls._memory["default"][item]

    def __setitem__(cls, item):
        if isinstance(item, tuple):
            return cls._memory[item[1]][item[0]]
        else:
            return cls._memory[item._namespace][item]

    def __delitem__(cls, item):
        if isinstance(item, tuple):
            del cls._memory[item[1]][item[0]]
        else:
            del cls._memory[item._namespace][item]

    def __contains__(cls, item):
        return item in cls._memory[item._namespace]

    def get(cls, unique_id, default=None, namespace="default"):
        return cls._memory[namespace].get(unique_id, default)

    def clear(cls, namespace="default"):
        cls._memory[namespace].clear()

    def has_key(cls, unique_id, namespace="default"):
        return unique_id in cls._memory[namespace]


class Snowflake(object):
    """
    Base class for all objects that should be unique based on an identifier.

    Notes
    -----
    Each instance of this class or its subclasses is uniquely identified and
    stored by its identifier.  Instantiating the same class with the same
    identifier will simply yield the original instance.

    The class attribute ``_counter`` is immutable and thus the state is not shared
    among subclasses but could be modified by the metaclass in the same way as
    ``_memory`` otherwise.

    Warning
    -------
    Subclasses of ``Snowflake`` must not override ``__call__`` unless you know
    exactly what you're doing.
    """

    # metaclass adds mutable subclass-specific attribute
    __metaclass__ = MetaFlake
    # immutable class attribute is subclass-specific automatically
    _counter = 0

    def __init__(self, unique_id="", namespace="default", **kw_args):
        """
        Parameters
        ----------
        unique_id: str (optional)
            A string uniquely identifying one component among its class.
            Actually, any hashable object that can serve as a dictionary key can
            serve as the ID.
        """
        super(Snowflake, self).__init__(**kw_args)
        self._index = self.__class__._counter
        if unique_id:
            self.unique_id = unique_id
        else:
            self.unique_id = u"{0}_{1:d}".format(self.__class__.__name__,
                    self._index)
        self._namespace = namespace
        self._skip_setstate = False
        self.__class__._memory[namespace][self.unique_id] = self

    def __reduce__(self):
        """
        Take full control of pickling this class.

        The basic dilemma is that ``__getnewargs__`` is called only by pickle
        protocol version >= 2 but we require it to be called every time so
        that we can unpickle the correct objects no matter the pickle version
        used.
        """
        return (_unpickle_call, self.__getnewargs__(), self.__getstate__())

    def __getnewargs__(self):
        """
        Returns a tuple that is supplied to a call of ``self.__class__`` when
        unpickling this object.

        The ``unique_id`` is all we need for persistent state. It allows us to
        retrieve an existing object with that ID or generate it accordingly.
        """
        return (self.__class__, self.unique_id, self._namespace)

    def __getstate__(self):
        """
        We could be unpickling this instance in a new process or namespace and
        there ``__setstate__`` should definitely be run. So we remove the skip
        flag.
        """
        self._skip_setstate = False
        return self.__dict__

    def __setstate__(self, state):
        """
        Take control of how to unpickle an instance of this class.

        Update the instance's ``__dict__`` with the state. We only update attributes
        that evaluate to false because otherwise we might replace existing
        attributes with the unpickled ones (kind of a workaround, can't decide
        when an object was newly created upon unpickling).
        """
        if self._skip_setstate:
            return
        self.__dict__.update(state)

    def __str__(self):
        return str(self.unique_id)

    def __unicode__(self):
        return unicode(self.unique_id)

    def __repr__(self):
        return u"<{0}.{1} {2:d}>".format(self.__module__, self.__class__.__name__, id(self))


def _unpickle_call(cls, unique_id, namespace):
    """
    Prevents setting of state iff the object existed before.
    """
    memory = cls._memory.setdefault(namespace, dict())
    skip = unique_id in memory # test before instantiation
    obj = cls(unique_id=unique_id, namespace=namespace)
    obj._skip_setstate = skip
    return obj

