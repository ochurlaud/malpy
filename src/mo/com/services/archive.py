#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The Archive service provides a basic interface to a standard archiving function. It follows the basic CRUD principles and allows simple querying of the archive. It provides operations to add new objects to an archive, delete objects from an archive, update existing objects in an archive, and also query the content of the archive.
The query operation provides a basic querying ability, allowing a consumer to filter on fields from the object headers (such as domain etc) and also filter on the body of the object if it uses the MAL data type specification.
The query operation is extensible but the extensions would be outside this standard.
Finally, a consumer of the archive can monitor it for changes by subscribing for archive events from the event service. Any change to the archive is published using the event service if it is supported by an implementation."""

from enum import IntEnum
from mo import mal
from mo.com import *

number = 2

# CapabilitySet 1
class Retrieve(mal.InvokeProviderHandler):
    pass

class Query(mal.ProgressProviderHandler):
    pass

class Count(mal.InvokeProviderHandler):
    pass


# CapabilitySet 2
class Store(mal.RequestProviderHandler):
    pass


# CapabilitySet 3
class Update(mal.SubmitProviderHandler):
    pass


# CapabilitySet 4
class Delete(mal.RequestProviderHandler):
    pass

class MALShortForm(IntEnum):
    EXPRESSIONOPERATOR = 5
    ARCHIVEDETAILS = 1
    ARCHIVEQUERY = 2
    COMPOSITEFILTER = 3
    COMPOSITEFILTERSET = 4


class ExpressionOperator(IntEnum):
    """The ExpressionOperator enumeration holds a set of possible expression operators."""

    shortForm = MALShortForm.EXPRESSIONOPERATOR

    EQUAL = 1 # Checks for equality.
    DIFFER = 2 # Checks for difference (not equal).
    GREATER = 3 # Checks for greater than.
    GREATER_OR_EQUAL = 4 # Checks for greater than or equal to.
    LESS = 5 # Checks for less than.
    LESS_OR_EQUAL = 6 # Checks for less than or equal to.
    CONTAINS = 7 # Case sensitive containment test (String types only)
    ICONTAINS = 8 # Case insensitive containment test (String types only).


class QueryFilter(mal.Composite):
    """The base structure for archive filters."""

    shortForm = None

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            self._value = [None]*0


class QueryFilterList(mal.ElementList):
    shortForm = -MALShortForm.QUERYFILTER

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._value = []
        if type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else: 
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._value.append(QueryFilter(v))


class ArchiveDetails(mal.Composite):
    """The ArchiveDetails structure is used to hold information about a single entry in an Archive."""

    shortForm = MALShortForm.ARCHIVEDETAILS

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            self._value = [None]*5
            self.instId = value[0]
            self.details = value[1]
            self.network = value[2]
            self.timestamp = value[3]
            self.provider = value[4]

    @property
    def instId(self):
        return self._value[0]

    @instId.setter
    def instId(self, instId):
        self._value[0] = mal.Long(instId, canBeNull=False, attribName='instId')

    @property
    def details(self):
        return self._value[1]

    @details.setter
    def details(self, details):
        self._value[1] = ObjectDetails(details, canBeNull=False, attribName='details')

    @property
    def network(self):
        return self._value[2]

    @network.setter
    def network(self, network):
        self._value[2] = mal.Identifier(network, canBeNull=True, attribName='network')

    @property
    def timestamp(self):
        return self._value[3]

    @timestamp.setter
    def timestamp(self, timestamp):
        self._value[3] = mal.FineTime(timestamp, canBeNull=True, attribName='timestamp')

    @property
    def provider(self):
        return self._value[4]

    @provider.setter
    def provider(self, provider):
        self._value[4] = mal.URI(provider, canBeNull=True, attribName='provider')


class ArchiveDetailsList(mal.ElementList):
    shortForm = -MALShortForm.ARCHIVEDETAILS

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._value = []
        if type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else: 
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._value.append(ArchiveDetails(v))


class ArchiveQuery(mal.Composite):
    """The ArchiveQuery structure is used to specify filters on the common parts of an object in an archive."""

    shortForm = MALShortForm.ARCHIVEQUERY

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            self._value = [None]*9
            self.domain = value[0]
            self.network = value[1]
            self.provider = value[2]
            self.related = value[3]
            self.source = value[4]
            self.startTime = value[5]
            self.endTime = value[6]
            self.sortOrder = value[7]
            self.sortFieldName = value[8]

    @property
    def domain(self):
        return self._value[0]

    @domain.setter
    def domain(self, domain):
        self._value[0] = mal.IdentifierList(domain, canBeNull=True, attribName='domain')

    @property
    def network(self):
        return self._value[1]

    @network.setter
    def network(self, network):
        self._value[1] = mal.Identifier(network, canBeNull=True, attribName='network')

    @property
    def provider(self):
        return self._value[2]

    @provider.setter
    def provider(self, provider):
        self._value[2] = mal.URI(provider, canBeNull=True, attribName='provider')

    @property
    def related(self):
        return self._value[3]

    @related.setter
    def related(self, related):
        self._value[3] = mal.Long(related, canBeNull=False, attribName='related')

    @property
    def source(self):
        return self._value[4]

    @source.setter
    def source(self, source):
        self._value[4] = ObjectId(source, canBeNull=True, attribName='source')

    @property
    def startTime(self):
        return self._value[5]

    @startTime.setter
    def startTime(self, startTime):
        self._value[5] = mal.FineTime(startTime, canBeNull=True, attribName='startTime')

    @property
    def endTime(self):
        return self._value[6]

    @endTime.setter
    def endTime(self, endTime):
        self._value[6] = mal.FineTime(endTime, canBeNull=True, attribName='endTime')

    @property
    def sortOrder(self):
        return self._value[7]

    @sortOrder.setter
    def sortOrder(self, sortOrder):
        self._value[7] = mal.Boolean(sortOrder, canBeNull=True, attribName='sortOrder')

    @property
    def sortFieldName(self):
        return self._value[8]

    @sortFieldName.setter
    def sortFieldName(self, sortFieldName):
        self._value[8] = mal.String(sortFieldName, canBeNull=True, attribName='sortFieldName')


class ArchiveQueryList(mal.ElementList):
    shortForm = -MALShortForm.ARCHIVEQUERY

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._value = []
        if type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else: 
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._value.append(ArchiveQuery(v))


class CompositeFilter(mal.Composite):
    """The CompositeFilter allows an archive query to specify a filter based on the content of the body of an object if that body is specified using the MAL data type specification."""

    shortForm = MALShortForm.COMPOSITEFILTER

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            self._value = [None]*3
            self.fieldName = value[0]
            self.type = value[1]
            self.fieldValue = value[2]

    @property
    def fieldName(self):
        return self._value[0]

    @fieldName.setter
    def fieldName(self, fieldName):
        self._value[0] = mal.String(fieldName, canBeNull=False, attribName='fieldName')

    @property
    def type(self):
        return self._value[1]

    @type.setter
    def type(self, type):
        self._value[1] = ExpressionOperator(type, canBeNull=False, attribName='type')

    @property
    def fieldValue(self):
        return self._value[2]

    @fieldValue.setter
    def fieldValue(self, fieldValue):
        self._value[2] = mal.Attribute(fieldValue, canBeNull=True, attribName='fieldValue')


class CompositeFilterList(mal.ElementList):
    shortForm = -MALShortForm.COMPOSITEFILTER

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._value = []
        if type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else: 
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._value.append(CompositeFilter(v))


class CompositeFilterSet(QueryFilter):
    """Contains a list of CompositeFilters that are AND'd together to form a more complex filter."""

    shortForm = MALShortForm.COMPOSITEFILTERSET

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        if value is None and self._canBeNull:
            self._isNull = True
        elif type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else:
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            self._value = [None]*1
            self.filters = value[0]

    @property
    def filters(self):
        return self._value[0]

    @filters.setter
    def filters(self, filters):
        self._value[0] = CompositeFilterList(filters, canBeNull=False, attribName='filters')


class CompositeFilterSetList(mal.ElementList):
    shortForm = -MALShortForm.COMPOSITEFILTERSET

    def __init__(self, value, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._value = []
        if type(value) == type(self):
            if value.value is None:
                if self._canBeNull:
                    self._isNull = True
                else: 
                    raise ValueError("This {} cannot be Null".format(type(self)))
            else:
                self._value = value.copy().value
        else:
            listvalue = value if type(value) == list else [value]
            for v in listvalue:
                 self._value.append(CompositeFilterSet(v))


