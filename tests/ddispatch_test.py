# @ddispatch
# async def foo(*args, _dispatch_key, **kwargs):
#     pass

# @foo.register('a')
# async def foo1(a, b):
#     await asyncio.sleep(1.100)
#     print(f'async: {a} {b}')

# @foo.register('b')
# def foo2(a):
#     print(f'sync {a}')   

# async def main():
#     print(f'inside main')
#     tasks = list()

#     print(inspect.isfunction(foo))
#     print(inspect.iscoroutinefunction(foo))
#     print(inspect.isroutine(foo))

#     print(inspect.getfullargspec(foo))

#     tasks.append(asyncio.create_task(foo(_dispatch_key='a', a=1, b=2)))
#     tasks.append(asyncio.create_task(foo(3, _dispatch_key='b')))

#     for task in tasks:
#         await task

# if __name__ == '__main__':
#     asyncio.run(main())

