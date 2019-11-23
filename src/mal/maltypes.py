from enum import IntEnum
from abc import ABC

name = "MAL"
number = 1
version = 1

class MALShortForm(IntEnum):
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
    INTERACTIONTYPE = 19
    SESSIONTYPE = 20
    QOSLEVEL = 21
    UPDATETYPE = 22
    SUBSCRIPTION = 23
    ENTITYREQUEST = 24
    ENTITYKEY = 25
    UPDATEHEADER = 26
    IDBOOLEANPAIR = 27
    PAIR = 28
    NAMEDVALUE = 29
    FILE = 30

class InteractionType(IntEnum):
    """InteractionType is an enumeration holding the possible interaction pattern types."""

    shortForm = MALShortForm.INTERACTIONTYPE

    SEND = 1 # Used for Send interactions.
    SUBMIT = 2 # Used for Submit interactions.
    REQUEST = 3 # Used for Request interactions.
    INVOKE = 4 # Used for Invoke interactions.
    PROGRESS = 5 # Used for Progress interactions.
    PUBSUB = 6 # Used for Publish/Subscribe interactions.


class SessionType(IntEnum):
    """SessionType is an enumeration holding the session types."""

    shortForm = MALShortForm.SESSIONTYPE

    LIVE = 1 # Used for Live sessions.
    SIMULATION = 2 # Used for Simulation sessions.
    REPLAY = 3 # Used for Replay sessions.


class QoSLevel(IntEnum):
    """QoSLevel is an enumeration holding the possible QoS levels."""

    shortForm = MALShortForm.QOSLEVEL

    BESTEFFORT = 1 # Used for Best Effort QoS Level.
    ASSURED = 2 # Used for Assured QoS Level.
    QUEUED = 3 # Used for Queued QoS Level.
    TIMELY = 4 # Used for Timely QoS Level.


class UpdateType(IntEnum):
    """UpdateType is an enumeration holding the possible Update types."""

    shortForm = MALShortForm.UPDATETYPE

    CREATION = 1 # Update is notification of the creation of the item.
    UPDATE = 2 # Update is just a periodic update of the item and has not changed its value.
    MODIFICATION = 3 # Update is for a changed value or modification of the item.
    DELETION = 4 # Update is notification of the removal of the item.


class Errors(IntEnum):
    """ All MAL errors."""

    DELIVERY_FAILED = 65536 # Confirmed communication error.
    DELIVERY_TIMEDOUT = 65537 # Unconfirmed communication error.
    DELIVERY_DELAYED = 65538 # Message queued somewhere awaiting contact.
    DESTINATION_UNKNOWN = 65539 # Destination cannot be contacted.
    DESTINATION_TRANSIENT = 65540 # Destination middleware reports destination application does not exist.
    DESTINATION_LOST = 65541 # Destination lost halfway through conversation.
    AUTHENTICATION_FAIL = 65542 # A failure to authenticate the message correctly.
    AUTHORISATION_FAIL = 65543 # A failure in the MAL to authorise the message.
    ENCRYPTION_FAIL = 65544 # A failure in the MAL to encrypt/decrypt the message.
    UNSUPPORTED_AREA = 65545 # The destination does not support the service area.
    UNSUPPORTED_OPERATION = 65546 # The destination does not support the operation.
    UNSUPPORTED_VERSION = 65547 # The destination does not support the service version.
    BAD_ENCODING = 65548 # The destination was unable to decode the message.
    INTERNAL = 65549 # An internal error has occurred.
    UNKNOWN = 65550 # Operation specific.
    INCORRECT_STATE = 65551 # The destination was not in the correct state for the received message.
    TOO_MANY = 65552 # Maximum number of subscriptions or providers of a broker has been exceeded.
    SHUTDOWN = 65553 # The component is being shutdown.


class Element(ABC):
    """Element is the base type of all data constructs. All types that make up the MAL data model are derived from it."""

    shortForm = None


class Attribute(Element):
    """Attribute is the base type of all attributes of the MAL data model. Attributes are contained within Composites and are used to build complex structures that make the data model."""

    shortForm = None

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.value
        elif type(value) == type(self).value_type:
            self._value = value
        else:
            raise TypeError("Expected {}, got {}.".format(type(self).value_type, type(value)))

    @property
    def value(self):
        return self._value

    def copy(self):
        return self.value


class Composite(Element):
    """Composite is the base structure for composite structures that contain a set of elements."""

    shortForm = None

    @property
    def value(self):
        return self._value

    def copy(self):
        value = []
        for v in self.value:
            if type(v) == list:
                value.append([x.copy() for x in v])
            else:
                value.append(v.copy())
        return self.__class__(value)


class Blob(Attribute):
    """The Blob structure is used to store binary object attributes. It is a variable-length, unbounded, octet array. The distinction between this type and a list of Octet attributes is that this type may allow language mappings and encodings to use more efficient or appropriate representations."""

    shortForm = MALShortForm.BLOB
    value_type = bytes


class Boolean(Attribute):
    """The Boolean structure is used to store Boolean attributes. Possible values are 'True' or 'False'."""

    shortForm = MALShortForm.BOOLEAN
    value_type = bool


class Duration(Attribute):
    """The Duration structure is used to store Duration attributes. It represents a length of time in seconds. It may contain a fractional component."""

    shortForm = MALShortForm.DURATION
    value_type = float


class Float(Attribute):
    """The Float structure is used to store floating point attributes using the IEEE 754 32-bit range.
Three special values exist for this type: POSITIVE_INFINITY, NEGATIVE_INFINITY, and NaN (Not A Number)."""

    shortForm = MALShortForm.FLOAT
    value_type = float


class Double(Attribute):
    """The Double structure is used to store floating point attributes using the IEEE 754 64-bit range.
Three special values exist for this type: POSITIVE_INFINITY, NEGATIVE_INFINITY, and NaN (Not A Number)."""

    shortForm = MALShortForm.DOUBLE
    value_type = float


class Identifier(Attribute):
    """The Identifier structure is used to store an identifier and can be used for indexing. It is a variable-length, unbounded, Unicode string."""

    shortForm = MALShortForm.IDENTIFIER
    value_type = str


class Octet(Attribute):
    """The Octet structure is used to store 8-bit signed attributes. The permitted range is -128 to 127."""

    shortForm = MALShortForm.OCTET
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < -128 or value > 127 ):
            raise ValueError("Authorized value is between -128 and 127.")


class UOctet(Attribute):
    """The UOctet structure is used to store 8-bit unsigned attributes. The permitted range is 0 to 255."""

    shortForm = MALShortForm.UOCTET
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < 0 or value > 255 ):
            raise ValueError("Authorized value is between 0 and 255.")


class Short(Attribute):
    """The Short structure is used to store 16-bit signed attributes. The permitted range is -32768 to 32767."""

    shortForm = MALShortForm.SHORT
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < -32768 or value > 32767 ):
            raise ValueError("Authorized value is between -32768 and 32767.")


class UShort(Attribute):
    """The UShort structure is used to store 16-bit unsigned attributes. The permitted range is 0 to 65535."""

    shortForm = MALShortForm.USHORT
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < 0 or value > 65535 ):
            raise ValueError("Authorized value is between 0 and 65535.")


class Integer(Attribute):
    """The Integer structure is used to store 32-bit signed attributes. The permitted range is -2147483648 to 2147483647."""

    shortForm = MALShortForm.INTEGER
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < -2147483648 or value > 21474836487 ):
            raise ValueError("Authorized value is between -2147483648 and 21474836487.")


class UInteger(Attribute):
    """The UInteger structure is used to store 32-bit unsigned attributes. The permitted range is 0 to 4294967295."""

    shortForm = MALShortForm.UINTEGER
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < 0 or value > 4294967295 ):
            raise ValueError("Authorized value is between 0 and 4294967295.")


class Long(Attribute):
    """The Long structure is used to store 64-bit signed attributes. The permitted range is -9223372036854775808 to 9223372036854775807."""

    shortForm = MALShortForm.LONG
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < -9223372036854775808 or value > 9223372036854775807 ):
            raise ValueError("Authorized value is between -9223372036854775808 and 9223372036854775807.")


class ULong(Attribute):
    """The ULong structure is used to store 64-bit unsigned attributes. The permitted range is 0 to 18446744073709551615."""

    shortForm = MALShortForm.ULONG
    value_type = int

    def __init__(self, value):
        super().__init__(value)
        if type(value) == int and ( value < 0 or value > 18446744073709551615 ):
            raise ValueError("Authorized value is between 0 and 18446744073709551615.")


class String(Attribute):
    """The String structure is used to store String attributes. It is a variable-length, unbounded, Unicode string."""

    shortForm = MALShortForm.STRING
    value_type = str


class Time(Attribute):
    """The Time structure is used to store absolute time attributes. It represents an absolute date and time to millisecond resolution."""

    shortForm = MALShortForm.TIME
    value_type = float


class FineTime(Attribute):
    """The FineTime structure is used to store high-resolution absolute time attributes. It represents an absolute date and time to picosecond resolution."""

    shortForm = MALShortForm.FINETIME
    value_type = float


class URI(Attribute):
    """The URI structure is used to store URI addresses. It is a variable-length, unbounded, Unicode string."""

    shortForm = MALShortForm.URI
    value_type = str


class Subscription(Composite):
    """The Subscription structure is used when subscribing for updates using the PUBSUB interaction pattern. It contains a single identifier that identifies the subscription being defined and a set of entities being requested."""

    shortForm = MALShortForm.SUBSCRIPTION

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.subscriptionId = value[0]
            self.entities = value[1]

    @property
    def subscriptionId(self):
        return self._value[0]

    @subscriptionId.setter
    def subscriptionId(self, subscriptionId):
        self._value[0] = EntityRequest(subscriptionId)

    @property
    def entities(self):
        return self._value[1]

    @entities.setter
    def entities(self, entities):
        self._value[1] = [EntityRequest(x) for x in entities]


class EntityRequest(Composite):
    """The EntityRequest structure is used when subscribing for updates using the PUBSUB interaction pattern."""

    shortForm = MALShortForm.ENTITYREQUEST

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.subDomain = value[0]
            self.allAreas = value[1]
            self.allServices = value[2]
            self.allOperations = value[3]
            self.onlyOnChange = value[4]
            self.entityKeys = value[5]

    @property
    def subDomain(self):
        return self._value[0]

    @subDomain.setter
    def subDomain(self, subDomain):
        self._value[0] = [EntityKey(x) for x in subDomain]

    @property
    def allAreas(self):
        return self._value[1]

    @allAreas.setter
    def allAreas(self, allAreas):
        self._value[1] = EntityKey(allAreas)

    @property
    def allServices(self):
        return self._value[2]

    @allServices.setter
    def allServices(self, allServices):
        self._value[2] = EntityKey(allServices)

    @property
    def allOperations(self):
        return self._value[3]

    @allOperations.setter
    def allOperations(self, allOperations):
        self._value[3] = EntityKey(allOperations)

    @property
    def onlyOnChange(self):
        return self._value[4]

    @onlyOnChange.setter
    def onlyOnChange(self, onlyOnChange):
        self._value[4] = EntityKey(onlyOnChange)

    @property
    def entityKeys(self):
        return self._value[5]

    @entityKeys.setter
    def entityKeys(self, entityKeys):
        self._value[5] = [EntityKey(x) for x in entityKeys]


class EntityKey(Composite):
    """The EntityKey structure is used to identify an entity in the PUBSUB interaction pattern."""

    shortForm = MALShortForm.ENTITYKEY

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.firstSubKey = value[0]
            self.secondSubKey = value[1]
            self.thirdSubKey = value[2]
            self.fourthSubKey = value[3]

    @property
    def firstSubKey(self):
        return self._value[0]

    @firstSubKey.setter
    def firstSubKey(self, firstSubKey):
        self._value[0] = Long(firstSubKey)

    @property
    def secondSubKey(self):
        return self._value[1]

    @secondSubKey.setter
    def secondSubKey(self, secondSubKey):
        self._value[1] = Long(secondSubKey)

    @property
    def thirdSubKey(self):
        return self._value[2]

    @thirdSubKey.setter
    def thirdSubKey(self, thirdSubKey):
        self._value[2] = Long(thirdSubKey)

    @property
    def fourthSubKey(self):
        return self._value[3]

    @fourthSubKey.setter
    def fourthSubKey(self, fourthSubKey):
        self._value[3] = Long(fourthSubKey)


class UpdateHeader(Composite):
    """The UpdateHeader structure is used by updates using the PUBSUB interaction pattern. It holds information that identifies a single update."""

    shortForm = MALShortForm.UPDATEHEADER

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.timestamp = value[0]
            self.sourceURI = value[1]
            self.updateType = value[2]
            self.key = value[3]

    @property
    def timestamp(self):
        return self._value[0]

    @timestamp.setter
    def timestamp(self, timestamp):
        self._value[0] = EntityKey(timestamp)

    @property
    def sourceURI(self):
        return self._value[1]

    @sourceURI.setter
    def sourceURI(self, sourceURI):
        self._value[1] = EntityKey(sourceURI)

    @property
    def updateType(self):
        return self._value[2]

    @updateType.setter
    def updateType(self, updateType):
        self._value[2] = EntityKey(updateType)

    @property
    def key(self):
        return self._value[3]

    @key.setter
    def key(self, key):
        self._value[3] = EntityKey(key)


class IdBooleanPair(Composite):
    """IdBooleanPair is a simple pair type of an identifier and Boolean value."""

    shortForm = MALShortForm.IDBOOLEANPAIR

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.id = value[0]
            self.value = value[1]

    @property
    def id(self):
        return self._value[0]

    @id.setter
    def id(self, id):
        self._value[0] = Boolean(id)

    @property
    def value(self):
        return self._value[1]

    @value.setter
    def value(self, value):
        self._value[1] = Boolean(value)


class Pair(Composite):
    """Pair is a simple composite structure for holding pairs. The pairs can be user-defined attributes."""

    shortForm = MALShortForm.PAIR

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.first = value[0]
            self.second = value[1]

    @property
    def first(self):
        return self._value[0]

    @first.setter
    def first(self, first):
        self._value[0] = Attribute(first)

    @property
    def second(self):
        return self._value[1]

    @second.setter
    def second(self, second):
        self._value[1] = Attribute(second)


class NamedValue(Composite):
    """The NamedValue structure represents a simple pair type of an identifier and abstract attribute value."""

    shortForm = MALShortForm.NAMEDVALUE

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.name = value[0]
            self.value = value[1]

    @property
    def name(self):
        return self._value[0]

    @name.setter
    def name(self, name):
        self._value[0] = Attribute(name)

    @property
    def value(self):
        return self._value[1]

    @value.setter
    def value(self, value):
        self._value[1] = Attribute(value)


class File(Composite):
    """The File structure represents a File and holds details about a File. It can also, optionally, hold a BLOB of the file data. The file type is denoted using the internet MIME media types, the list of official MIME types is held at http://www.iana.org/assignments/media-types/index.html."""

    shortForm = MALShortForm.FILE

    def __init__(self, value):
        if type(value) == type(self):
            self._value = value.copy()
        else:
            self.name = value[0]
            self.mimeType = value[1]
            self.creationDate = value[2]
            self.modificationDate = value[3]
            self.size = value[4]
            self.content = value[5]
            self.metaData = value[6]

    @property
    def name(self):
        return self._value[0]

    @name.setter
    def name(self, name):
        self._value[0] = NamedValue(name)

    @property
    def mimeType(self):
        return self._value[1]

    @mimeType.setter
    def mimeType(self, mimeType):
        self._value[1] = NamedValue(mimeType)

    @property
    def creationDate(self):
        return self._value[2]

    @creationDate.setter
    def creationDate(self, creationDate):
        self._value[2] = NamedValue(creationDate)

    @property
    def modificationDate(self):
        return self._value[3]

    @modificationDate.setter
    def modificationDate(self, modificationDate):
        self._value[3] = NamedValue(modificationDate)

    @property
    def size(self):
        return self._value[4]

    @size.setter
    def size(self, size):
        self._value[4] = NamedValue(size)

    @property
    def content(self):
        return self._value[5]

    @content.setter
    def content(self, content):
        self._value[5] = NamedValue(content)

    @property
    def metaData(self):
        return self._value[6]

    @metaData.setter
    def metaData(self, metaData):
        self._value[6] = [NamedValue(x) for x in metaData]


