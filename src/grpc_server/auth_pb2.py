# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04user\" \n\x0bUserRequest\x12\x11\n\tjwt_token\x18\x01 \x01(\t\"\x1a\n\x0cUserResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x32:\n\x04User\x12\x32\n\x07GetUser\x12\x11.user.UserRequest\x1a\x12.user.UserResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERREQUEST._serialized_start=20
  _USERREQUEST._serialized_end=52
  _USERRESPONSE._serialized_start=54
  _USERRESPONSE._serialized_end=80
  _USER._serialized_start=82
  _USER._serialized_end=140
# @@protoc_insertion_point(module_scope)
