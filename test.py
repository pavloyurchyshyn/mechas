import asyncio

RUN = True


async def say(what, when):
    i = 0
    while RUN:
        await asyncio.sleep(when)
        print(what, i)
        i += 1


async def loop_end(timeout, loop):
    print('end of the loop start')
    await asyncio.sleep(timeout)
    global RUN
    RUN = False
    print('end of the loop')


async def main(loop):
    await asyncio.wait(
        [
            loop.create_task(loop_end(5, loop)),
            loop.create_task(say('hello world', 1)),
        ]
    )


# a = 100, 1000, 100, 000
# print(a)
# loop = asyncio.new_event_loop()
# loop.run_until_complete(main(loop))
#
# loop.close()
#
# try:
#     print('aa', '1' == 1)
#     if '1' != 1:
#         raise Exception
#     else:
#         print("someError has not occured")
# except Exception:
#     print("someError has occured")

f = None

for i in range(5):
    with open("data.txt", "w") as f:
        if (i > 2):
            break

print(f.closed)