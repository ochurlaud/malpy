#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The group service provides a mechanism for other services to reference sets of their own objects using a single group reference. These groups are used by the other MC services (such as Action, Alert, Check, Aggregation and Parameter) to reduce the complexity of operations by allowing consumers to reference groups of objects (such as parameters) in operations rather than having to supply large lists of object references.
Where operations of other service mention the use of groups in their operations, any reference to a group object instance identifier implicitly means a GroupIdentity object.
Groups of other groups is supported, however all objects within the group of groups should have the same object type as most operations expect a single type.
The creation of cyclic group of groups should also be avoided.
The group service does not provide any operations directly, but allows consumers to add, remove, and modify groups via the COM archive."""

from enum import IntEnum
from malpy.mo import mal
from malpy.mo import com
from malpy.mo import mc

number = 8
class MALShortForm(IntEnum):
    GROUPDETAILS = 1


class GroupDetails(mal.Composite):
    """The GroupDetails structure holds the object type, domain, and set of object instance identifiers for a set of objects from another service."""

    shortForm = MALShortForm.GROUPDETAILS
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
            self.description = value[mal.Composite._fieldNumber + 0]
            self.objectType = value[mal.Composite._fieldNumber + 1]
            self.domain = value[mal.Composite._fieldNumber + 2]
            self.instanceIds = value[mal.Composite._fieldNumber + 3]

    @property
    def description(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @description.setter
    def description(self, description):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.String(description, canBeNull=False, attribName='description')
        self._isNull = False

    @property
    def objectType(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @objectType.setter
    def objectType(self, objectType):
        self._internal_value[mal.Composite._fieldNumber + 1] = com.ObjectType(objectType, canBeNull=False, attribName='objectType')
        self._isNull = False

    @property
    def domain(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @domain.setter
    def domain(self, domain):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.IdentifierList(domain, canBeNull=False, attribName='domain')
        self._isNull = False

    @property
    def instanceIds(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @instanceIds.setter
    def instanceIds(self, instanceIds):
        self._internal_value[mal.Composite._fieldNumber + 3] = mal.LongList(instanceIds, canBeNull=False, attribName='instanceIds')
        self._isNull = False


class GroupDetailsList(mal.ElementList):
    shortForm = -MALShortForm.GROUPDETAILS

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
                 self._internal_value.append(GroupDetails(v))

