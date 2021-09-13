import asyncio
import inspect

def coro_dispatch(fn):
    print(f'inside dispatch {fn.__name__}')
    registry = dict()
    registry[''] = fn
    
    def register(key_):
        print(f'inside register {key_}')
        def inner(fn):
            print(f'inside inner {fn.__name__}')
            registry[key_] = fn
            #return fn  
        return inner
   
    async def decorator(*args, _dispatch_key, **kwargs):
        print(f'inside decorator {_dispatch_key}')
        fn = registry[_dispatch_key]

        print('-------------------------')
        print(inspect.getfullargspec(fn).args)

        if inspect.iscoroutinefunction(fn):
            result = await fn(*args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, fn, *args)
        return result
    
    decorator.register = register
    decorator.registry = registry.keys()

    return decorator

@coro_dispatch
async def foo(*args, _dispatch_key, **kwargs):
    pass

@foo.register('a')
async def foo1(a, b):
    await asyncio.sleep(1.100)
    print(f'async: {a} {b}')

@foo.register('b')
def foo2(a):
    print(f'sync {a}')   

async def main():
    print(f'inside main')
    tasks = list()

    print(inspect.isfunction(foo))
    print(inspect.iscoroutinefunction(foo))
    print(inspect.isroutine(foo))

    print(inspect.getfullargspec(foo))

    tasks.append(asyncio.create_task(foo(_dispatch_key='a', a=1, b=2)))
    tasks.append(asyncio.create_task(foo(3, _dispatch_key='b')))

    for task in tasks:
        await task

if __name__ == '__main__':
    asyncio.run(main())









