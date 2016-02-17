import asyncio
import functools

class Accelerometer():
    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        self._event_callback = None
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

    async def set_event_handler(self, callback=None, granularity=0.05):
        '''
        Set a callback function to be executed when the accelerometer
        values on the robot change.

        :param callback: async func(x, y, z, timestamp) -> None
        :param granularity: float . The callback will only be called when any
            axis of the accelerometer changes by this many G's of acceleration.
        '''
        self._event_callback = callback
        if not callback:
            # Remove the event
            try:
                fut = await self._proxy.enableAccelerometerEvent(
                        enable=False,
                        granularity=granularity)
                await fut
                self._proxy.rb_remove_broadcast_handler('accelerometerEvent')
                return fut
            except KeyError:
                # Don't worry if the bcast handler is not there.
                pass

        else:
            self._proxy.rb_add_broadcast_handler( 'accelerometerEvent', 
                                                  self.__event_handler )
            return await self._proxy.enableAccelerometerEvent(
                    enable=True,
                    granularity=granularity )

    async def __event_handler(self, payload):
        await self._event_callback( payload.x, 
                                    payload.y, 
                                    payload.z, 
                                    payload.timestamp)

class Button():
    PWR = 0
    A = 1
    B = 2

    UP = 0
    DOWN = 1

    @classmethod
    async def create(cls, proxy):
        self = cls()
        self._proxy = proxy
        self._event_callback = None
        return self

    async def values(self):
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__values,
                    user_fut
                    )
                )
        return user_fut

    def __values(self, user_fut, fut):
        pwr = fut.result().mask & 0x01
        a = (fut.result().mask>>1) & 0x01
        b = (fut.result().mask>>2) & 0x01
        user_fut.set_result( (pwr, a, b) )

    async def pwr(self):
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__button_values,
                    0,
                    user_fut
                    )
                )
        return user_fut

    async def a(self):
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__button_values,
                    1,
                    user_fut
                    )
                )
        return user_fut

    async def b(self):
        fut = await self._proxy.getButtonState()
        user_fut = asyncio.Future()
        fut.add_done_callback(
                functools.partial(
                    self.__button_values,
                    2,
                    user_fut
                    )
                )
        return user_fut

    def __button_values(self, index, user_fut, fut):
        user_fut.set_result((fut.result().mask>>index) & 0x01)

    async def set_event_handler(self, callback=None):
        '''
        Set a callback function to be executed when there is a button press or
        release.

        :param callback: func(buttonNo(int), buttonDown(bool), timestamp) -> None
        '''
        self._event_callback = callback
        if not callback:
            # Remove the event
            try:
                fut = await self._proxy.enableButtonEvent(
                        enable=False)
                await fut
                self._proxy.rb_remove_broadcast_handler('buttonEvent')
                return fut
            except KeyError:
                # Don't worry if the bcast handler is  not there.
                pass

        else:
            self._proxy.rb_add_broadcast_handler( 'buttonEvent', 
                                                  self.__event_handler )
            return await self._proxy.enableButtonEvent(
                    enable=True)

    async def __event_handler(self, payload):
        await self._event_callback( payload.button, 
                                    payload.state, 
                                    payload.timestamp)

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
