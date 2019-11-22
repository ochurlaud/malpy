from enum import IntEnum

class MAL_ATTRIBUTE_FLAGS(IntEnum):
    BLOB = 1
    BOOLEAN = 2
    DURATION = 3
    FLOAT = 4
    DOUBLE = 5
    IDENTIFIER = 6
    OCTET = 7
    UOCTET = 8
    SHORT = 9
    USHORT = 10
    INTEGER = 11
    UINTEGER = 12
    LONG = 13
    ULONG = 14
    STRING = 15
    TIME = 16
    FINETIME = 17
    URI = 18


class MAL_IP_TYPES(IntEnum):
    SEND = 1
    SUBMIT = 2
    REQUEST = 3
    INVOKE = 4
    PROGRESS = 5
    PUBSUB = 6


class MAL_IP_STAGES(IntEnum):
    SEND = 0
    SUBMIT = 1
    SUBMIT_ACK = 2
    REQUEST = 3
    REQUEST_RESPONSE = 4
    INVOKE = 5
    INVOKE_ACK = 6
    INVOKE_RESPONSE = 7
    PROGRESS = 8
    PROGRESS_ACK = 9
    PROGRESS_UPDATE = 10
    PROGRESS_RESPONSE = 11
    PUBSUB_REGISTER = 12
    PUBSUB_REGISTER_ACK = 13
    PUBSUB_PUBLISH_REGISTER = 14
    PUBSUB_PUBLISH_REGISTER_ACK = 15
    PUBSUB_PUBLISH = 16
    PUBSUB_NOTIFY = 17
    PUBSUB_DEREGISTER = 18
    PUBSUB_DEREGISTER_ACK = 19
    PUBSUB_PUBLISH_DEREGISTER = 20
    PUBSUB_PUBLISH_DEREGISTER_ACK = 21


class MAL_IP_ERRORS(IntEnum):
    SUBMIT_ERROR = 2
    REQUEST_ERROR = 4
    INVOKE_ACK_ERROR = 6
    INVOKE_RESPONSE_ERROR = 7
    PROGRESS_ACK_ERROR = 9
    PROGRESS_UPDATE_ERROR = 10
    PROGRESS_RESPONSE_ERROR = 11
    PUBSUB_REGISTER_ACK_ERROR = 13
    PUBSUB_PUBLISH_REGISTER_ERROR = 14
    PUBSUB_PUBLISH_ERROR = 16
    PUBSUB_NOTIFY_ERROR = 17


class SESSION_TYPES(IntEnum):
    LIVE = 1
    SIMULATION = 2
    REPLAY = 3


class QOSLEVELS(IntEnum):
    BESTEFFORT = 1
    ASSURED = 2
    QUEUED = 3
    TIMELY = 4

