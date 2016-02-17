import asyncio
import functools

class Accelerometer():
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        return self

    async def values(self):
        fut = await self._proxy.getAccelerometerData()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__values,
                    user_fut )
                )
        return user_fut

    def __values(self, user_fut, fut):
        user_fut.set_result(
                ( fut.result().x, fut.result().y, fut.result().z )
                )

    async def x(self):
        fut = await self.values()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__get_index,
                    0,
                    user_fut )
                )
        return user_fut

    async def y(self):
        fut = await self.values()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__get_index,
                    1,
                    user_fut )
                )
        return user_fut

    async def z(self):
        fut = await self.values()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__get_index,
                    2,
                    user_fut )
                )
        return user_fut

    def __get_index(self, index, user_fut, fut):
        user_fut.set_result( fut.result()[index] )

class Led():
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        return self

    async def color(self):
        fut = await self._proxy.getLedColor()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__color,
                    user_fut
                    )
                )
        return user_fut
        
    def __color(self, user_fut, fut):
        word = fut.result().value
        r = (word&0xff0000) >> 16
        g = (word&0x00ff00) >> 8
        b = word&0x0000ff
        user_fut.set_result( (r,g,b) )

    async def set_color(self, r, g, b):
        word = b | (g<<8) | (r<<16)
        fut = await self._proxy.setLedColor(value=word)
        return fut
