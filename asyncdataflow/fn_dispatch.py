def dispatch(fn):

    registry = dict()
    registry[''] = fn
    
    def register(key_):
        def inner(fn):
            registry[key_] = fn
            return fn  
        return inner
   
    def decorator(*args, _dispatch_key, **kwargs):
        return registry[_dispatch_key](*args, **kwargs)
    
    decorator.register = register
    decorator.registry = registry.keys()

    return decorator







