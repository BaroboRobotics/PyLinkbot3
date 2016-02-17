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

