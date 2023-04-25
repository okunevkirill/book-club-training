import asyncio
from asyncio import AbstractEventLoop
from threading import Thread
from step016 import LoadTester


class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


_loop = asyncio.new_event_loop()
asyncio_thread = ThreadedEventLoop(_loop)
asyncio_thread.start()

app = LoadTester(_loop)
app.mainloop()
