import asyncio


async def foo():
    print('foo')


async def main():
    await foo()

if __name__ == '__main__':
    asyncio.run(main())

    