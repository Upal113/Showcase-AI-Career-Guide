import asyncio

async def async_func():
    print('Velotio ...')
    await asyncio.sleep(1)
    print('... Blog!')

async def main():
    tasks = [asyncio.create_task(async_func()) for _ in range(3)]
    await asyncio.gather(*tasks)

asyncio.run(main())
