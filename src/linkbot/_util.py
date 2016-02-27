import asyncio
import functools
import math
import threading

DEFAULT_TIMEOUT=10

def rad2deg(rad):
    return rad*180/math.pi

def deg2rad(deg):
    return deg*math.pi/180

def chain_futures(fut1, fut2, conv=lambda x: x):
    def done(fut2, conv, fut1):
        if fut1.cancelled():
            fut2.cancel()
        else:
            fut2.set_result( conv(fut1.result()) )

    fut1.add_done_callback(
            functools.partial(
                done,
                fut2,
                conv)
            )

def run_linkbot_coroutine(coro, loop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    fut2 = fut.result(timeout=DEFAULT_TIMEOUT)
    result = asyncio.run_coroutine_threadsafe(
            asyncio.wait_for(fut2, timeout=DEFAULT_TIMEOUT), loop)
    return result.result()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class IoCore(metaclass=Singleton):
    def __init__(self):
        self._initializing = True
        self._initializing_sig = threading.Condition()
        self.loop = None
        self._thread = threading.Thread(target=self._work)
        self._thread.daemon = True
        self.start_work()

    def start_work(self):
        if self._thread.is_alive():
            return
        self._thread.start()

        self._initializing_sig.acquire()
        while self._initializing:
            self._initializing_sig.wait(timeout=1)
        self._initializing_sig.release()

    def stop_work(self):
        self.loop.stop()

    def get_event_loop(self):
        return self.loop

    def _work(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._initializing_sig.acquire()
        self._initializing = False
        self._initializing_sig.notify_all()
        self._initializing_sig.release()
        self.loop.run_forever()

