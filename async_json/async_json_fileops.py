from json import loads, dumps

import asyncio
from aiofiles import open


__doc__ = """
Writing to JSON via 'dump' is a syncronous (blocking) action.
Cheap Async fix for this is to generate file pointer via
aiofiles, append new data to current json data
loaded via async load(), then json.dumps the new data.

Downside:
 - Load() to get JSON data is mandatory
 - Cannot directly run write() without having data from in file
 - 2 function calls for write, 1 for load (overall)
"""

# RFB (reason for bit):
#  https://stackoverflow.com/questions/66522303/should-i-use-json-dumps-with-write-function-or-json-dump-in-python#comment119418412_66522414


async def load(filename):
    """Async load from JSON file"""
    async with open(filename, "rb") as f:
        return loads(await f.read())


async def write(filename, data, indent=0):
    """Async write to JSON file"""
    async with open(filename, "w+") as f:
        await f.write(f"{dumps(data, indent=indent)}")


async def bla():
    """Whatever async print to test above"""
    print("bla")


async def main():
    for i in range(10):
        await bla()
        data = await load("test.json")
        print(data, type(data))

        data[len(data.keys()) + 1] = "test"

        await write("test.json", data, 4)

    # With more complex structure
    data = await load("test.json")
    data[len(data.keys()) + 1] = [{"list_dict": "test"}]
    await write("test.json", data, 4)


if __name__ == "__main__":
    asyncio.run(main())
