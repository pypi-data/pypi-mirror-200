from _thread import RLock

_NOT_FOUND = object()


# Most of the code comes from the standard library (cached_property decorator)
# Warning: the dependent properties that get listed must be hashable!

def dependent_cached_prop(on=[]):
    def decorator(func):
        return _cached_property(func, on)

    return decorator


class _cached_property:
    def __init__(self, func, attr_for_caches=None):
        if attr_for_caches is None:
            attr_for_caches = []
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.attr_for_caches = attr_for_caches
        self.lock = RLock()

    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
        elif name != self.attrname:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.attrname!r} and {name!r})."
            )

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it.")
        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        val = cache.get(self.attrname + '__cached', _NOT_FOUND)
        surrogate_key = hash(tuple(getattr(instance, attr) for attr in self.attr_for_caches))
        surrogate_key_from_cache = cache.get(f"{self.attrname}_surrogate_key", _NOT_FOUND)
        if surrogate_key_from_cache is _NOT_FOUND or surrogate_key != surrogate_key_from_cache:
            cache[f"{self.attrname}_surrogate_key"] = surrogate_key
        if val is _NOT_FOUND or surrogate_key != surrogate_key_from_cache:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname + '__cached', _NOT_FOUND)
                if val is _NOT_FOUND or surrogate_key != surrogate_key_from_cache:
                    val = self.func(instance)
                    try:
                        cache[self.attrname + '__cached'] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
        return val


class MyClass:
    def __init__(self):
        self.salary = 100
        self.title = 'noob'

    @dependent_cached_prop(on=["salary", "title"])
    def bigsalary(self):
        print("bigsalary called")
        if self.title == 'senior':
            return '999999'
        return self.salary * 10


m = MyClass()
print(m.bigsalary)
print(m.bigsalary)
m.salary = 200
print(m.bigsalary)
print(m.bigsalary)
m.title = 'senior'
print(m.bigsalary)
print(m.bigsalary)
