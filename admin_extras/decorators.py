from . import conf


def cache_result(first_is_self=False, cache_attr_name=None):
    def wrapped_decorator(func):
        def wrapped_func(*args, **kwargs):
            obj = args[0] if first_is_self else func
            cache_attr = cache_attr_name or '_%s' % func.__name__
            if not hasattr(obj, cache_attr):
                setattr(obj, cache_attr, func(*args, **kwargs))
            return getattr(obj, cache_attr)

        wrapped_func.__dict__ = func.__dict__
        wrapped_func.__doc__ = func.__doc__
        wrapped_func.__name__ = func.__name__

        return wrapped_func
    return wrapped_decorator


def add_readonly_to_builtin_permissions(func):
    def wrapped_func(opts):
        if conf.READONLY_CODENAME not in opts.default_permissions:
            opts.default_permissions = list(opts.default_permissions)
            opts.default_permissions.append(conf.READONLY_CODENAME)
            perms = func(opts)
            try:
                opts.default_permissions.remove(conf.READONLY_CODENAME)
            except ValueError:
                pass
            return perms
        return func(opts)

    wrapped_func.__dict__ = func.__dict__
    wrapped_func.__doc__ = func.__doc__
    wrapped_func.__name__ = func.__name__

    return wrapped_func
