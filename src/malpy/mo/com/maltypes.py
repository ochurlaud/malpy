#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""This section details the Common Object Model area; the structures used by the service are detailed in section 4. The area and structures are defined in terms of the MO Message Abstraction Layer (MAL), so it is possible to deploy them over any supported protocol and message transport."""

from enum import IntEnum
from malpy.mo import mal

name = "COM"
number = 2
version = 1

class MALShortForm(IntEnum):
    OBJECTTYPE = 1
    OBJECTKEY = 2
    OBJECTID = 3
    OBJECTDETAILS = 4
    INSTANCEBOOLEANPAIR = 5


class ObjectType(mal.Composite):
    """The ObjectType structure uniquely identifies the type of an object. It is the combination of the area number, service number, area version, and service object type number. The combined parts are able to fit inside a MAL::Long (for implementations that prefer to index on a single numeric field rather than a structure)."""

    shortForm = MALShortForm.OBJECTTYPE
    _fieldNumber = mal.Composite._fieldNumber + 4

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*4
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            self.area = value[mal.Composite._fieldNumber + 0]
            self.service = value[mal.Composite._fieldNumber + 1]
            self.version = value[mal.Composite._fieldNumber + 2]
            self.number = value[mal.Composite._fieldNumber + 3]

    @property
    def area(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @area.setter
    def area(self, area):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.UShort(area, canBeNull=False, attribName='area')
        self._isNull = False

    @property
    def service(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @service.setter
    def service(self, service):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.UShort(service, canBeNull=False, attribName='service')
        self._isNull = False

    @property
    def version(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @version.setter
    def version(self, version):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.UOctet(version, canBeNull=False, attribName='version')
        self._isNull = False

    @property
    def number(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @number.setter
    def number(self, number):
        self._internal_value[mal.Composite._fieldNumber + 3] = mal.UShort(number, canBeNull=False, attribName='number')
        self._isNull = False


class ObjectTypeList(mal.ElementList):
    shortForm = -MALShortForm.OBJECTTYPE

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value = []
        if type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._internal_value.append(ObjectType(v))


class ObjectKey(mal.Composite):
    """The ObjectKey structure combines a domain and an object instance identifier such that it identifies the instance of an object for a specific domain."""

    shortForm = MALShortForm.OBJECTKEY
    _fieldNumber = mal.Composite._fieldNumber + 2

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*2
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            self.domain = value[mal.Composite._fieldNumber + 0]
            self.instId = value[mal.Composite._fieldNumber + 1]

    @property
    def domain(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @domain.setter
    def domain(self, domain):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.IdentifierList(domain, canBeNull=False, attribName='domain')
        self._isNull = False

    @property
    def instId(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @instId.setter
    def instId(self, instId):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Long(instId, canBeNull=False, attribName='instId')
        self._isNull = False


class ObjectKeyList(mal.ElementList):
    shortForm = -MALShortForm.OBJECTKEY

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value = []
        if type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._internal_value.append(ObjectKey(v))


class ObjectId(mal.Composite):
    """The ObjectId structure combines an object type and an object key such that it identifies the instance and type of an object for a specific domain."""

    shortForm = MALShortForm.OBJECTID
    _fieldNumber = mal.Composite._fieldNumber + 2

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*2
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            self.type = value[mal.Composite._fieldNumber + 0]
            self.key = value[mal.Composite._fieldNumber + 1]

    @property
    def type(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @type.setter
    def type(self, type):
        self._internal_value[mal.Composite._fieldNumber + 0] = ObjectType(type, canBeNull=False, attribName='type')
        self._isNull = False

    @property
    def key(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @key.setter
    def key(self, key):
        self._internal_value[mal.Composite._fieldNumber + 1] = ObjectKey(key, canBeNull=False, attribName='key')
        self._isNull = False


class ObjectIdList(mal.ElementList):
    shortForm = -MALShortForm.OBJECTID

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value = []
        if type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._internal_value.append(ObjectId(v))


class ObjectDetails(mal.Composite):
    """The ObjectDetails type is used to hold the extra information associated with an object instance, namely the related and source links."""

    shortForm = MALShortForm.OBJECTDETAILS
    _fieldNumber = mal.Composite._fieldNumber + 2

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*2
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            self.related = value[mal.Composite._fieldNumber + 0]
            self.source = value[mal.Composite._fieldNumber + 1]

    @property
    def related(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @related.setter
    def related(self, related):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Long(related, canBeNull=True, attribName='related')
        self._isNull = False

    @property
    def source(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @source.setter
    def source(self, source):
        self._internal_value[mal.Composite._fieldNumber + 1] = ObjectId(source, canBeNull=True, attribName='source')
        self._isNull = False


class ObjectDetailsList(mal.ElementList):
    shortForm = -MALShortForm.OBJECTDETAILS

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value = []
        if type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._internal_value.append(ObjectDetails(v))


class InstanceBooleanPair(mal.Composite):
    """Simple pair of an object instance identifier and a Boolean value."""

    shortForm = MALShortForm.INSTANCEBOOLEANPAIR
    _fieldNumber = mal.Composite._fieldNumber + 2

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*2
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            self.id = value[mal.Composite._fieldNumber + 0]
            self.value = value[mal.Composite._fieldNumber + 1]

    @property
    def id(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @id.setter
    def id(self, id):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Long(id, canBeNull=False, attribName='id')
        self._isNull = False

    @property
    def value(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @value.setter
    def value(self, value):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Boolean(value, canBeNull=False, attribName='value')
        self._isNull = False


class InstanceBooleanPairList(mal.ElementList):
    shortForm = -MALShortForm.INSTANCEBOOLEANPAIR

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value = []
        if type(value) == type(self):
            if value.internal_value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._internal_value = value.copy().internal_value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._internal_value.append(InstanceBooleanPair(v))


class Errors(IntEnum):
    """All MAL errors."""

    INVALID = 70000  # Operation specific
    DUPLICATE = 70001  # Operation specific