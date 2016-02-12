#!/usr/bin/env python3

import asyncio
import functools
import logging
import os
import ribbonbridge as rb
import sfp.asyncio
import threading

_dirname = os.path.dirname(os.path.realpath(__file__))

class _Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(_Singleton, cls).__call__(*args, **kw)
        return cls.instance

class _IoCore():
    __metaclass__ = _Singleton

    def __init__(self):
        self._initializing = True
        self._initializing_sig = threading.Condition()
        self.loop = None
        self._thread = threading.Thread(target=self._work)
        self._thread.start()

        self._initializing_sig.acquire()
        while self._initializing:
            self._initializing_sig.wait(timeout=1)
        self._initializing_sig.release()

    def get_event_loop(self):
        return self.loop

    def _work(self):
        self.loop = asyncio.new_event_loop()
        self._initializing_sig.acquire()
        self._initializing = False
        self._initializing_sig.notify_all()
        self._initializing_sig.release()
        logging.info('Starting event loop.')
        self.loop.run_forever()

class _SfpProxy(rb.Proxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_protocol(self, protocol):
        self._protocol = protocol

    async def rb_emit_to_server(self, bytestring):
        self._protocol.write(bytestring)

class _AsyncLinkbot(rb.Proxy):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    @classmethod
    async def create(cls, serial_id):
        logging.info('Creating async Linkbot handle to ID:{}'.format(serial_id))
        self = cls( os.path.join(_dirname, 'robot_pb2.py'))
        self.__daemon = _SfpProxy(
                os.path.join(_dirname, 'daemon_pb2.py'))

        loop = asyncio.get_event_loop()
        logging.info('Creating tcp connection to daemon...')
        (transport, protocol) = await loop.create_connection(
                functools.partial(
                    sfp.asyncio.SfpProtocol,
                    self.__daemon.rb_deliver,
                    loop),
                'localhost', '42000' )
        logging.info('Daemon TCP connection established.')

        logging.info('Setting daemon protocol...')
        self.__daemon.set_protocol(protocol)
        logging.info('Initiating daemon handshake...')
        await asyncio.sleep(0.5)
        await self.__daemon.rb_connect()
        logging.info('Daemon handshake finished.')

        logging.info('Resolving serial id...')
        args = self.__daemon.rb_get_args_obj('resolveSerialId')
        args.serialId.value = serial_id
        result_fut = await self.__daemon.resolveSerialId(args)
        tcp_endpoint = await result_fut
        logging.info('Connecting to robot endpoint...')
        (linkbot_transport, linkbot_protocol) = \
            await loop.create_connection(
                    functools.partial(
                        sfp.asyncio.SfpProtocol,
                        self.rb_deliver,
                        loop),
                    tcp_endpoint.endpoint.address,
                    str(tcp_endpoint.endpoint.port) )
        logging.info('Connected to robot endpoint.')
        self._linkbot_transport = linkbot_transport
        self._linkbot_protocol = linkbot_protocol
        logging.info('Sending connect request to robot...')
        await asyncio.sleep(0.5)
        await self.rb_connect()
        logging.info('Done sending connect request to robot.')
        return self

    def close(self):
        self._linkbot_transport.close()

    async def rb_emit_to_server(self, bytestring):
        logging.info('Emitting bytestring to protocol layer...')
        self._linkbot_protocol.write(bytestring)

class _Linkbot():
    def __init__(self, serial_id):
        self.__iocore = _IoCore()

        self._proxy = asyncio.run_coroutine_threadsafe(
                AsyncLinkbot.create(serial_id),
                self.__iocore.get_event_loop()
                )

    def __getattr__(self, name):
        if name not in self._proxy.rb_procedures():
            raise AttributeError('{} is not a Linkbot member function.'
                    .format(name) )
        return functools.partial(
                self._handle_rpc, name
                )

    def _handle_rpc(self, name, args_obj=None, **kw):
        if not args_obj:
            args_obj = self._proxy.rb_get_args_obj()
            for k,v in kw.items():
                setattr(args_obj, k, v)
        fut = asyncio.run_coroutine_threadsafe(
                getattr(self._proxy, name)(args_obj),
                self.__iocore.get_event_loop()
                )
        return fut


