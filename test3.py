import inspect
import asyncio


class Test:
    async def __call__(self, a):
        print(a)

async def main():
    await Test()(a='aaa')

    print(inspect.iscoroutinefunction(Test().__call__))
    print(inspect.iscoroutinefunction(main))

    f_args = inspect.getfullargspec(Test().__call__).args
    print(f_args)

if __name__ == '__main__':
    asyncio.run(main())

