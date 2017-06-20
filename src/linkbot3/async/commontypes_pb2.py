# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: commontypes.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import nanopb_pb2 as nanopb__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='commontypes.proto',
  package='linkbot',
  syntax='proto2',
  serialized_pb=_b('\n\x11\x63ommontypes.proto\x12\x07linkbot\x1a\x0cnanopb.proto\" \n\x08SerialId\x12\x14\n\x05value\x18\x01 \x02(\tB\x05\x92?\x02\x08\x05*\'\n\tRadioPort\x12\x1a\n\x16LINKBOT_RADIO_PROTOCOL\x10\x05')
  ,
  dependencies=[nanopb__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_RADIOPORT = _descriptor.EnumDescriptor(
  name='RadioPort',
  full_name='linkbot.RadioPort',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LINKBOT_RADIO_PROTOCOL', index=0, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=78,
  serialized_end=117,
)
_sym_db.RegisterEnumDescriptor(_RADIOPORT)

RadioPort = enum_type_wrapper.EnumTypeWrapper(_RADIOPORT)
LINKBOT_RADIO_PROTOCOL = 5



_SERIALID = _descriptor.Descriptor(
  name='SerialId',
  full_name='linkbot.SerialId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='linkbot.SerialId.value', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\010\005'))),
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
  serialized_start=44,
  serialized_end=76,
)

DESCRIPTOR.message_types_by_name['SerialId'] = _SERIALID
DESCRIPTOR.enum_types_by_name['RadioPort'] = _RADIOPORT

SerialId = _reflection.GeneratedProtocolMessageType('SerialId', (_message.Message,), dict(
  DESCRIPTOR = _SERIALID,
  __module__ = 'commontypes_pb2'
  # @@protoc_insertion_point(class_scope:linkbot.SerialId)
  ))
_sym_db.RegisterMessage(SerialId)


_SERIALID.fields_by_name['value'].has_options = True
_SERIALID.fields_by_name['value']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\010\005'))
# @@protoc_insertion_point(module_scope)
