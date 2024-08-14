from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AskForSubscribe(_message.Message):
    __slots__ = ("channel", "consumerName")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CONSUMERNAME_FIELD_NUMBER: _ClassVar[int]
    channel: str
    consumerName: str
    def __init__(self, channel: _Optional[str] = ..., consumerName: _Optional[str] = ...) -> None: ...

class AskForSubscribeReplay(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: str
    def __init__(self, ack: _Optional[str] = ...) -> None: ...

class AskForQuees(_message.Message):
    __slots__ = ("ask",)
    ASK_FIELD_NUMBER: _ClassVar[int]
    ask: str
    def __init__(self, ask: _Optional[str] = ...) -> None: ...

class AskForQueesReplay(_message.Message):
    __slots__ = ("listQuees",)
    LISTQUEES_FIELD_NUMBER: _ClassVar[int]
    listQuees: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, listQuees: _Optional[_Iterable[str]] = ...) -> None: ...

class AskForMessage(_message.Message):
    __slots__ = ("channel", "consumerName")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CONSUMERNAME_FIELD_NUMBER: _ClassVar[int]
    channel: str
    consumerName: str
    def __init__(self, channel: _Optional[str] = ..., consumerName: _Optional[str] = ...) -> None: ...

class AskForMessageReplay(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: str
    def __init__(self, ack: _Optional[str] = ...) -> None: ...
