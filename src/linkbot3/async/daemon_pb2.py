# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: daemon.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import nanopb_pb2 as nanopb__pb2
import commontypes_pb2 as commontypes__pb2
import rpc_pb2 as rpc__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='daemon.proto',
  package='barobo.Daemon',
  syntax='proto2',
  serialized_pb=_b('\n\x0c\x64\x61\x65mon.proto\x12\rbarobo.Daemon\x1a\x0cnanopb.proto\x1a\x11\x63ommontypes.proto\x1a\trpc.proto\"3\n\x0bTcpEndpoint\x12\x16\n\x07\x61\x64\x64ress\x18\x01 \x02(\tB\x05\x92?\x02\x08@\x12\x0c\n\x04port\x18\x02 \x02(\r\"\x93\x01\n\x0fresolveSerialId\x1a(\n\x02In\x12\"\n\x08serialId\x18\x01 \x02(\x0b\x32\x10.barobo.SerialId\x1aV\n\x06Result\x12\x1e\n\x06status\x18\x01 \x02(\x0e\x32\x0e.barobo.Status\x12,\n\x08\x65ndpoint\x18\x02 \x02(\x0b\x32\x1a.barobo.Daemon.TcpEndpoint\".\n\x0b\x63ycleDongle\x1a\x15\n\x02In\x12\x0f\n\x07seconds\x18\x01 \x02(\r\x1a\x08\n\x06Result\"n\n\rsendRobotPing\x1a\x33\n\x02In\x12-\n\x0c\x64\x65stinations\x18\x01 \x03(\x0b\x32\x10.barobo.SerialIdB\x05\x92?\x02\x10\x08\x1a(\n\x06Result\x12\x1e\n\x06status\x18\x01 \x02(\x0e\x32\x0e.barobo.Status\"b\n\x0b\x64ongleEvent\x12\x1e\n\x06status\x18\x01 \x02(\x0e\x32\x0e.barobo.Status\x12\x33\n\x0f\x66irmwareVersion\x18\x02 \x02(\x0b\x32\x1a.barobo.rpc.VersionTriplet\"\xcb\x01\n\nrobotEvent\x12\"\n\x08serialId\x18\x01 \x02(\x0b\x32\x10.barobo.SerialId\x12\x33\n\x0f\x66irmwareVersion\x18\x02 \x02(\x0b\x32\x1a.barobo.rpc.VersionTriplet\x12.\n\nrpcVersion\x18\x03 \x02(\x0b\x32\x1a.barobo.rpc.VersionTriplet\x12\x34\n\x10interfaceVersion\x18\x04 \x02(\x0b\x32\x1a.barobo.rpc.VersionTriplet')
  ,
  dependencies=[nanopb__pb2.DESCRIPTOR,commontypes__pb2.DESCRIPTOR,rpc__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TCPENDPOINT = _descriptor.Descriptor(
  name='TcpEndpoint',
  full_name='barobo.Daemon.TcpEndpoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='barobo.Daemon.TcpEndpoint.address', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\010@'))),
    _descriptor.FieldDescriptor(
      name='port', full_name='barobo.Daemon.TcpEndpoint.port', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=126,
)


_RESOLVESERIALID_IN = _descriptor.Descriptor(
  name='In',
  full_name='barobo.Daemon.resolveSerialId.In',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serialId', full_name='barobo.Daemon.resolveSerialId.In.serialId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=148,
  serialized_end=188,
)

_RESOLVESERIALID_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='barobo.Daemon.resolveSerialId.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='barobo.Daemon.resolveSerialId.Result.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endpoint', full_name='barobo.Daemon.resolveSerialId.Result.endpoint', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=276,
)

_RESOLVESERIALID = _descriptor.Descriptor(
  name='resolveSerialId',
  full_name='barobo.Daemon.resolveSerialId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_RESOLVESERIALID_IN, _RESOLVESERIALID_RESULT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=276,
)


_CYCLEDONGLE_IN = _descriptor.Descriptor(
  name='In',
  full_name='barobo.Daemon.cycleDongle.In',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seconds', full_name='barobo.Daemon.cycleDongle.In.seconds', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=293,
  serialized_end=314,
)

_CYCLEDONGLE_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='barobo.Daemon.cycleDongle.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=198,
)

_CYCLEDONGLE = _descriptor.Descriptor(
  name='cycleDongle',
  full_name='barobo.Daemon.cycleDongle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_CYCLEDONGLE_IN, _CYCLEDONGLE_RESULT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=278,
  serialized_end=324,
)


_SENDROBOTPING_IN = _descriptor.Descriptor(
  name='In',
  full_name='barobo.Daemon.sendRobotPing.In',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='destinations', full_name='barobo.Daemon.sendRobotPing.In.destinations', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\020\010'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=343,
  serialized_end=394,
)

_SENDROBOTPING_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='barobo.Daemon.sendRobotPing.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='barobo.Daemon.sendRobotPing.Result.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=230,
)

_SENDROBOTPING = _descriptor.Descriptor(
  name='sendRobotPing',
  full_name='barobo.Daemon.sendRobotPing',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_SENDROBOTPING_IN, _SENDROBOTPING_RESULT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=326,
  serialized_end=436,
)


_DONGLEEVENT = _descriptor.Descriptor(
  name='dongleEvent',
  full_name='barobo.Daemon.dongleEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='barobo.Daemon.dongleEvent.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='firmwareVersion', full_name='barobo.Daemon.dongleEvent.firmwareVersion', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=438,
  serialized_end=536,
)


_ROBOTEVENT = _descriptor.Descriptor(
  name='robotEvent',
  full_name='barobo.Daemon.robotEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serialId', full_name='barobo.Daemon.robotEvent.serialId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='firmwareVersion', full_name='barobo.Daemon.robotEvent.firmwareVersion', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rpcVersion', full_name='barobo.Daemon.robotEvent.rpcVersion', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='interfaceVersion', full_name='barobo.Daemon.robotEvent.interfaceVersion', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=539,
  serialized_end=742,
)

_RESOLVESERIALID_IN.fields_by_name['serialId'].message_type = commontypes__pb2._SERIALID
_RESOLVESERIALID_IN.containing_type = _RESOLVESERIALID
_RESOLVESERIALID_RESULT.fields_by_name['status'].enum_type = commontypes__pb2._STATUS
_RESOLVESERIALID_RESULT.fields_by_name['endpoint'].message_type = _TCPENDPOINT
_RESOLVESERIALID_RESULT.containing_type = _RESOLVESERIALID
_CYCLEDONGLE_IN.containing_type = _CYCLEDONGLE
_CYCLEDONGLE_RESULT.containing_type = _CYCLEDONGLE
_SENDROBOTPING_IN.fields_by_name['destinations'].message_type = commontypes__pb2._SERIALID
_SENDROBOTPING_IN.containing_type = _SENDROBOTPING
_SENDROBOTPING_RESULT.fields_by_name['status'].enum_type = commontypes__pb2._STATUS
_SENDROBOTPING_RESULT.containing_type = _SENDROBOTPING
_DONGLEEVENT.fields_by_name['status'].enum_type = commontypes__pb2._STATUS
_DONGLEEVENT.fields_by_name['firmwareVersion'].message_type = rpc__pb2._VERSIONTRIPLET
_ROBOTEVENT.fields_by_name['serialId'].message_type = commontypes__pb2._SERIALID
_ROBOTEVENT.fields_by_name['firmwareVersion'].message_type = rpc__pb2._VERSIONTRIPLET
_ROBOTEVENT.fields_by_name['rpcVersion'].message_type = rpc__pb2._VERSIONTRIPLET
_ROBOTEVENT.fields_by_name['interfaceVersion'].message_type = rpc__pb2._VERSIONTRIPLET
DESCRIPTOR.message_types_by_name['TcpEndpoint'] = _TCPENDPOINT
DESCRIPTOR.message_types_by_name['resolveSerialId'] = _RESOLVESERIALID
DESCRIPTOR.message_types_by_name['cycleDongle'] = _CYCLEDONGLE
DESCRIPTOR.message_types_by_name['sendRobotPing'] = _SENDROBOTPING
DESCRIPTOR.message_types_by_name['dongleEvent'] = _DONGLEEVENT
DESCRIPTOR.message_types_by_name['robotEvent'] = _ROBOTEVENT

TcpEndpoint = _reflection.GeneratedProtocolMessageType('TcpEndpoint', (_message.Message,), dict(
  DESCRIPTOR = _TCPENDPOINT,
  __module__ = 'daemon_pb2'
  # @@protoc_insertion_point(class_scope:barobo.Daemon.TcpEndpoint)
  ))
_sym_db.RegisterMessage(TcpEndpoint)

resolveSerialId = _reflection.GeneratedProtocolMessageType('resolveSerialId', (_message.Message,), dict(

  In = _reflection.GeneratedProtocolMessageType('In', (_message.Message,), dict(
    DESCRIPTOR = _RESOLVESERIALID_IN,
    __module__ = 'daemon_pb2'
    # @@protoc_insertion_point(class_scope:barobo.Daemon.resolveSerialId.In)
    ))
  ,

  Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
    DESCRIPTOR = _RESOLVESERIALID_RESULT,
    __module__ = 'daemon_pb2'
    # @@protoc_insertion_point(class_scope:barobo.Daemon.resolveSerialId.Result)
    ))
  ,
  DESCRIPTOR = _RESOLVESERIALID,
  __module__ = 'daemon_pb2'
  # @@protoc_insertion_point(class_scope:barobo.Daemon.resolveSerialId)
  ))
_sym_db.RegisterMessage(resolveSerialId)
_sym_db.RegisterMessage(resolveSerialId.In)
_sym_db.RegisterMessage(resolveSerialId.Result)

cycleDongle = _reflection.GeneratedProtocolMessageType('cycleDongle', (_message.Message,), dict(

  In = _reflection.GeneratedProtocolMessageType('In', (_message.Message,), dict(
    DESCRIPTOR = _CYCLEDONGLE_IN,
    __module__ = 'daemon_pb2'
    # @@protoc_insertion_point(class_scope:barobo.Daemon.cycleDongle.In)
    ))
  ,

  Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
    DESCRIPTOR = _CYCLEDONGLE_RESULT,
    __module__ = 'daemon_pb2'
    # @@protoc_insertion_point(class_scope:barobo.Daemon.cycleDongle.Result)
    ))
  ,
  DESCRIPTOR = _CYCLEDONGLE,
  __module__ = 'daemon_pb2'
  # @@protoc_insertion_point(class_scope:barobo.Daemon.cycleDongle)
  ))
_sym_db.RegisterMessage(cycleDongle)
_sym_db.RegisterMessage(cycleDongle.In)
_sym_db.RegisterMessage(cycleDongle.Result)

sendRobotPing = _reflection.GeneratedProtocolMessageType('sendRobotPing', (_message.Message,), dict(

  In = _reflection.GeneratedProtocolMessageType('In', (_message.Message,), dict(
    DESCRIPTOR = _SENDROBOTPING_IN,
    __module__ = 'daemon_pb2'
    # @@protoc_insertion_point(class_scope:barobo.Daemon.sendRobotPing.In)
    ))
  ,

  Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
    DESCRIPTOR = _SENDROBOTPING_RESULT,
    __module__ = 'daemon_pb2'
    # @@protoc_insertion_point(class_scope:barobo.Daemon.sendRobotPing.Result)
    ))
  ,
  DESCRIPTOR = _SENDROBOTPING,
  __module__ = 'daemon_pb2'
  # @@protoc_insertion_point(class_scope:barobo.Daemon.sendRobotPing)
  ))
_sym_db.RegisterMessage(sendRobotPing)
_sym_db.RegisterMessage(sendRobotPing.In)
_sym_db.RegisterMessage(sendRobotPing.Result)

dongleEvent = _reflection.GeneratedProtocolMessageType('dongleEvent', (_message.Message,), dict(
  DESCRIPTOR = _DONGLEEVENT,
  __module__ = 'daemon_pb2'
  # @@protoc_insertion_point(class_scope:barobo.Daemon.dongleEvent)
  ))
_sym_db.RegisterMessage(dongleEvent)

robotEvent = _reflection.GeneratedProtocolMessageType('robotEvent', (_message.Message,), dict(
  DESCRIPTOR = _ROBOTEVENT,
  __module__ = 'daemon_pb2'
  # @@protoc_insertion_point(class_scope:barobo.Daemon.robotEvent)
  ))
_sym_db.RegisterMessage(robotEvent)


_TCPENDPOINT.fields_by_name['address'].has_options = True
_TCPENDPOINT.fields_by_name['address']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\010@'))
_SENDROBOTPING_IN.fields_by_name['destinations'].has_options = True
_SENDROBOTPING_IN.fields_by_name['destinations']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\020\010'))
# @@protoc_insertion_point(module_scope)
