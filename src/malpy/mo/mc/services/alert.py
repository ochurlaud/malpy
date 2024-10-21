#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The alert service defines the structures and patterns for the publishing and monitoring of alerts. The alert service uses COM event service to monitor and publish alert events.
The generation of alerts can be controlled using the enableGeneration operation, which supports the use of groups. Groups must reference either other groups or alerts only.
Alert definitions are maintained using the operations defined in this service but storage of definitions is delegated to the COM archive."""

from enum import IntEnum
from malpy.mo import mal
from malpy.mo import mc

number = 3

# CapabilitySet 1
class EnableGenerationProviderHandler(mal.RequestProviderHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 1


class EnableGenerationConsumerHandler(mal.RequestConsumerHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 1



# CapabilitySet 2
class ListDefinitionProviderHandler(mal.RequestProviderHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 2


class ListDefinitionConsumerHandler(mal.RequestConsumerHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 2



# CapabilitySet 3
class AddAlertProviderHandler(mal.RequestProviderHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 3


class AddAlertConsumerHandler(mal.RequestConsumerHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 3


class UpdateDefinitionProviderHandler(mal.RequestProviderHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 4


class UpdateDefinitionConsumerHandler(mal.RequestConsumerHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 4


class RemoveAlertProviderHandler(mal.SubmitProviderHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 5


class RemoveAlertConsumerHandler(mal.SubmitConsumerHandler):
    AREA = 4
    AREA_VERSION = 1
    SERVICE = 3
    OPERATION = 5


class MALShortForm(IntEnum):
    ALERTDEFINITIONDETAILS = 1
    ALERTEVENTDETAILS = 2
    ALERTCREATIONREQUEST = 3


class AlertDefinitionDetails(mal.Composite):
    """The AlertDefinitionDetails provides the definition of an alert including any argument definitions."""

    shortForm = MALShortForm.ALERTDEFINITIONDETAILS
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
            self.severity = value[mal.Composite._fieldNumber + 1]
            self.generationEnabled = value[mal.Composite._fieldNumber + 2]
            self.arguments = value[mal.Composite._fieldNumber + 3]

    @property
    def description(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @description.setter
    def description(self, description):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.String(description, canBeNull=False, attribName='description')
        self._isNull = False

    @property
    def severity(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @severity.setter
    def severity(self, severity):
        self._internal_value[mal.Composite._fieldNumber + 1] = mc.Severity(severity, canBeNull=False, attribName='severity')
        self._isNull = False

    @property
    def generationEnabled(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @generationEnabled.setter
    def generationEnabled(self, generationEnabled):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.Boolean(generationEnabled, canBeNull=False, attribName='generationEnabled')
        self._isNull = False

    @property
    def arguments(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @arguments.setter
    def arguments(self, arguments):
        self._internal_value[mal.Composite._fieldNumber + 3] = mc.ArgumentDefinitionDetailsList(arguments, canBeNull=False, attribName='arguments')
        self._isNull = False


class AlertDefinitionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.ALERTDEFINITIONDETAILS

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
                 self._internal_value.append(AlertDefinitionDetails(v))


class AlertEventDetails(mal.Composite):
    """The AlertEventDetails structure holds the details of an instance of an alert."""

    shortForm = MALShortForm.ALERTEVENTDETAILS
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
            self.argumentValues = value[mal.Composite._fieldNumber + 0]
            self.argumentIds = value[mal.Composite._fieldNumber + 1]

    @property
    def argumentValues(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @argumentValues.setter
    def argumentValues(self, argumentValues):
        self._internal_value[mal.Composite._fieldNumber + 0] = mc.AttributeValueList(argumentValues, canBeNull=True, attribName='argumentValues')
        self._isNull = False

    @property
    def argumentIds(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @argumentIds.setter
    def argumentIds(self, argumentIds):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.IdentifierList(argumentIds, canBeNull=True, attribName='argumentIds')
        self._isNull = False


class AlertEventDetailsList(mal.ElementList):
    shortForm = -MALShortForm.ALERTEVENTDETAILS

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
                 self._internal_value.append(AlertEventDetails(v))


class AlertCreationRequest(mal.Composite):
    """The AlertCreationRequest contains all the fields required when creating a new alert in a provider."""

    shortForm = MALShortForm.ALERTCREATIONREQUEST
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
            self.name = value[mal.Composite._fieldNumber + 0]
            self.alertDefDetails = value[mal.Composite._fieldNumber + 1]

    @property
    def name(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @name.setter
    def name(self, name):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Identifier(name, canBeNull=False, attribName='name')
        self._isNull = False

    @property
    def alertDefDetails(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @alertDefDetails.setter
    def alertDefDetails(self, alertDefDetails):
        self._internal_value[mal.Composite._fieldNumber + 1] = AlertDefinitionDetails(alertDefDetails, canBeNull=False, attribName='alertDefDetails')
        self._isNull = False


class AlertCreationRequestList(mal.ElementList):
    shortForm = -MALShortForm.ALERTCREATIONREQUEST

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
                 self._internal_value.append(AlertCreationRequest(v))


