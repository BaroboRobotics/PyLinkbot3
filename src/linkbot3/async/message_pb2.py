# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\rmessage.proto\"\x89\x01\n\x0bPrexMessage\x12&\n\x04type\x18\x01 \x01(\x0e\x32\x18.PrexMessage.MessageType\x12\x0f\n\x07payload\x18\x02 \x01(\x0c\"A\n\x0bMessageType\x12\x10\n\x0cLOAD_PROGRAM\x10\x00\x12\x06\n\x02IO\x10\x01\x12\t\n\x05IMAGE\x10\x02\x12\r\n\tTERMINATE\x10\x03\";\n\x0bLoadProgram\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0c\n\x04\x61rgv\x18\x03 \x03(\t\"Q\n\x02Io\x12\x14\n\x04type\x18\x01 \x01(\x0e\x32\x06.Io.FD\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\'\n\x02\x46\x44\x12\t\n\x05STDIN\x10\x00\x12\n\n\x06STDOUT\x10\x01\x12\n\n\x06STDERR\x10\x02\"\x18\n\x05Image\x12\x0f\n\x07payload\x18\x01 \x01(\x0c\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_PREXMESSAGE_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='PrexMessage.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LOAD_PROGRAM', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IO', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IMAGE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TERMINATE', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=90,
  serialized_end=155,
)
_sym_db.RegisterEnumDescriptor(_PREXMESSAGE_MESSAGETYPE)

_IO_FD = _descriptor.EnumDescriptor(
  name='FD',
  full_name='Io.FD',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STDIN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STDOUT', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STDERR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=260,
  serialized_end=299,
)
_sym_db.RegisterEnumDescriptor(_IO_FD)


_PREXMESSAGE = _descriptor.Descriptor(
  name='PrexMessage',
  full_name='PrexMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='PrexMessage.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payload', full_name='PrexMessage.payload', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PREXMESSAGE_MESSAGETYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=155,
)


_LOADPROGRAM = _descriptor.Descriptor(
  name='LoadProgram',
  full_name='LoadProgram',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='LoadProgram.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='LoadProgram.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='argv', full_name='LoadProgram.argv', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=157,
  serialized_end=216,
)


_IO = _descriptor.Descriptor(
  name='Io',
  full_name='Io',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Io.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='Io.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _IO_FD,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=218,
  serialized_end=299,
)


_IMAGE = _descriptor.Descriptor(
  name='Image',
  full_name='Image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='Image.payload', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=325,
)

_PREXMESSAGE.fields_by_name['type'].enum_type = _PREXMESSAGE_MESSAGETYPE
_PREXMESSAGE_MESSAGETYPE.containing_type = _PREXMESSAGE
_IO.fields_by_name['type'].enum_type = _IO_FD
_IO_FD.containing_type = _IO
DESCRIPTOR.message_types_by_name['PrexMessage'] = _PREXMESSAGE
DESCRIPTOR.message_types_by_name['LoadProgram'] = _LOADPROGRAM
DESCRIPTOR.message_types_by_name['Io'] = _IO
DESCRIPTOR.message_types_by_name['Image'] = _IMAGE

PrexMessage = _reflection.GeneratedProtocolMessageType('PrexMessage', (_message.Message,), dict(
  DESCRIPTOR = _PREXMESSAGE,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:PrexMessage)
  ))
_sym_db.RegisterMessage(PrexMessage)

LoadProgram = _reflection.GeneratedProtocolMessageType('LoadProgram', (_message.Message,), dict(
  DESCRIPTOR = _LOADPROGRAM,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:LoadProgram)
  ))
_sym_db.RegisterMessage(LoadProgram)

Io = _reflection.GeneratedProtocolMessageType('Io', (_message.Message,), dict(
  DESCRIPTOR = _IO,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:Io)
  ))
_sym_db.RegisterMessage(Io)

Image = _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), dict(
  DESCRIPTOR = _IMAGE,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:Image)
  ))
_sym_db.RegisterMessage(Image)


# @@protoc_insertion_point(module_scope)
