#!/usr/bin/env python3

import asyncio
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

class Linkbot(rb.Proxy):
    def __init__(self, serial_id):
        self.__iocore = _IoCore()

        super().__init__(
                os.path.join(_dirname, 'robot_pb2.py'),
                self.__iocore.get_event_loop()
                )

        self.__daemon = _SfpProxy(
                os.path.join(_dirname, 'daemon_pb2.py'),
                self.__iocore.get_event_loop()
                )

        # Connect TCP to daemon
        coro = self.__iocore.get_event_loop().create_connection(
                sfp.asyncio.SfpProtocol,
                'localhost', '42000' )
        fut = asyncio.run_coroutine_threadsafe( 
                coro,
                self.__iocore.get_event_loop() )
        (transport, protocol) = fut.result()
        self.__daemon.set_protocol(protocol)
        protocol.deliver = self.__daemon.rb_deliver
        self.__daemon.rb_connect()
    
        args = self.__daemon.rb_get_args_obj('resolveSerialId')
        args.serialId.value = serial_id
        tcp_endpoint = self.__daemon.resolveSerialId(args).result()
        print(tcp_endpoint)
        # Close the connection to the daemon, start a connection to the robot
        transport.close()
        logging.info('Connecting to robot endpoint...')
        coro = self.__iocore.get_event_loop().create_connection(
                sfp.asyncio.SfpProtocol,
                tcp_endpoint.endpoint.address,
                str(tcp_endpoint.endpoint.port) )
        fut = asyncio.run_coroutine_threadsafe(
                coro, self.__iocore.get_event_loop() )
        (linkbot_transport, linkbot_protocol) = fut.result()
        logging.info('Connected to robot endpoint.')
        self._linkbot_transport = linkbot_transport
        self._linkbot_protocol = linkbot_protocol
        self._linkbot_protocol.deliver = self.rb_deliver
        logging.info('Sending connect request to robot...')
        self.rb_connect()
        logging.info('Done sending connect request to robot.')

    async def rb_emit_to_server(self, bytestring):
        self._linkbot_protocol.write(bytestring)
         



