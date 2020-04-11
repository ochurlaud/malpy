#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The parameter service allows the user to subscribe to parameter value report and optionally be able to set new values. A single PUBSUB operation is provided for monitoring and publishing of parameter values.
A parameter value also contains a calculation of the validity of the parameter, the flow chart for this calculation is provided in Figure 3-3:
 validity calculation flow chart 

This standard supports the concept of non-standard invalidity states but the meaning and calculation of these is outside the scope of this standard.
The generation of value reports can be controlled using the enableGeneration operation, which supports the use of groups. Groups must reference parameter identities or groups of parameter identities only.
The parameter service does not include any value checking, this is delegated to the check service.
Parameter definitions are maintained using the operations defined in this service but storage of definitions is delegated to the COM archive."""

from enum import IntEnum
from mo import mal
from mo import com
from mo.mc import *

number = 2

# CapabilitySet 1
class MonitorValue(mal.PubSubProviderHandler):
    pass


# CapabilitySet 2
class GetValue(mal.RequestProviderHandler):
    pass


# CapabilitySet 3
class SetValue(mal.SubmitProviderHandler):
    pass


# CapabilitySet 4
class EnableGeneration(mal.RequestProviderHandler):
    pass


# CapabilitySet 5
class ListDefinition(mal.RequestProviderHandler):
    pass


# CapabilitySet 6
class AddParameter(mal.RequestProviderHandler):
    pass

class UpdateDefinition(mal.RequestProviderHandler):
    pass

class RemoveParameter(mal.SubmitProviderHandler):
    pass

class MALShortForm(IntEnum):
    VALIDITYSTATE = 4
    PARAMETERDEFINITIONDETAILS = 1
    PARAMETERVALUE = 2
    PARAMETERCONVERSION = 3
    PARAMETERCREATIONREQUEST = 5
    PARAMETERRAWVALUE = 6
    PARAMETERVALUEDETAILS = 7


class ValidityState(IntEnum):
    """Convenience enumeration that holds the validity states and their numeric values."""

    shortForm = MALShortForm.VALIDITYSTATE

    VALID = 0 # Valid.
    EXPIRED = 1 # The parameter has a timeout associated which has expired
    INVALID_RAW = 2 # The parameter raw value cannot be obtained, or calculated for synthetic parameters
    INVALID_CONVERSION = 3 # The validity expression either has evaluated to TRUE or there is no validity defined, but the conversion of the parameter value has failed (for example an unexpected value for a discrete conversion)
    UNVERIFIED = 4 # The validity of the validity expression has been evaluated to FALSE and therefore cannot be used to verify the current value
    INVALID = 5 # The validity expression has been evaluated to FALSE


class ParameterDefinitionDetails(mal.Composite):
    """The ParameterDefinitionDetails structure holds a parameter definition. The conversion field defines the conditions where the relevant conversion is applied. For onboard parameters, the report interval should be a multiple of the minimum sampling interval of that parameter."""

    shortForm = MALShortForm.PARAMETERDEFINITIONDETAILS

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
            self._value = [None]*7
            self.description = value[0]
            self.rawType = value[1]
            self.rawUnit = value[2]
            self.generationEnabled = value[3]
            self.reportInterval = value[4]
            self.validityExpression = value[5]
            self.conversion = value[6]

    @property
    def description(self):
        return self._value[0]

    @description.setter
    def description(self, description):
        self._value[0] = mal.String(description, canBeNull=False, attribName='description')

    @property
    def rawType(self):
        return self._value[1]

    @rawType.setter
    def rawType(self, rawType):
        self._value[1] = mal.Octet(rawType, canBeNull=False, attribName='rawType')

    @property
    def rawUnit(self):
        return self._value[2]

    @rawUnit.setter
    def rawUnit(self, rawUnit):
        self._value[2] = mal.String(rawUnit, canBeNull=True, attribName='rawUnit')

    @property
    def generationEnabled(self):
        return self._value[3]

    @generationEnabled.setter
    def generationEnabled(self, generationEnabled):
        self._value[3] = mal.Boolean(generationEnabled, canBeNull=False, attribName='generationEnabled')

    @property
    def reportInterval(self):
        return self._value[4]

    @reportInterval.setter
    def reportInterval(self, reportInterval):
        self._value[4] = mal.Duration(reportInterval, canBeNull=False, attribName='reportInterval')

    @property
    def validityExpression(self):
        return self._value[5]

    @validityExpression.setter
    def validityExpression(self, validityExpression):
        self._value[5] = ParameterExpression(validityExpression, canBeNull=True, attribName='validityExpression')

    @property
    def conversion(self):
        return self._value[6]

    @conversion.setter
    def conversion(self, conversion):
        self._value[6] = ParameterConversion(conversion, canBeNull=True, attribName='conversion')


class ParameterDefinitionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.PARAMETERDEFINITIONDETAILS

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
                 self._value.append(ParameterDefinitionDetails(v))


class ParameterValue(mal.Composite):
    """This structure holds a specific value of the parameter. The type of the value shall match that specified in the parameter definition."""

    shortForm = MALShortForm.PARAMETERVALUE

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
            self.validityState = value[0]
            self.rawValue = value[1]
            self.convertedValue = value[2]

    @property
    def validityState(self):
        return self._value[0]

    @validityState.setter
    def validityState(self, validityState):
        self._value[0] = mal.UOctet(validityState, canBeNull=False, attribName='validityState')

    @property
    def rawValue(self):
        return self._value[1]

    @rawValue.setter
    def rawValue(self, rawValue):
        self._value[1] = mal.Attribute(rawValue, canBeNull=True, attribName='rawValue')

    @property
    def convertedValue(self):
        return self._value[2]

    @convertedValue.setter
    def convertedValue(self, convertedValue):
        self._value[2] = mal.Attribute(convertedValue, canBeNull=True, attribName='convertedValue')


class ParameterValueList(mal.ElementList):
    shortForm = -MALShortForm.PARAMETERVALUE

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
                 self._value.append(ParameterValue(v))


class ParameterConversion(mal.Composite):
    """The ParameterConversion structure holds information about the conversions to be applied to a parameter."""

    shortForm = MALShortForm.PARAMETERCONVERSION

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
            self.convertedType = value[0]
            self.convertedUnit = value[1]
            self.conditionalConversions = value[2]

    @property
    def convertedType(self):
        return self._value[0]

    @convertedType.setter
    def convertedType(self, convertedType):
        self._value[0] = mal.Octet(convertedType, canBeNull=False, attribName='convertedType')

    @property
    def convertedUnit(self):
        return self._value[1]

    @convertedUnit.setter
    def convertedUnit(self, convertedUnit):
        self._value[1] = mal.String(convertedUnit, canBeNull=True, attribName='convertedUnit')

    @property
    def conditionalConversions(self):
        return self._value[2]

    @conditionalConversions.setter
    def conditionalConversions(self, conditionalConversions):
        self._value[2] = ConditionalConversionList(conditionalConversions, canBeNull=False, attribName='conditionalConversions')


class ParameterConversionList(mal.ElementList):
    shortForm = -MALShortForm.PARAMETERCONVERSION

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
                 self._value.append(ParameterConversion(v))


class ParameterCreationRequest(mal.Composite):
    """The ParameterCreationRequest contains all the fields required when creating a new parameter in a provider."""

    shortForm = MALShortForm.PARAMETERCREATIONREQUEST

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
            self._value = [None]*2
            self.name = value[0]
            self.paramDefDetails = value[1]

    @property
    def name(self):
        return self._value[0]

    @name.setter
    def name(self, name):
        self._value[0] = mal.Identifier(name, canBeNull=False, attribName='name')

    @property
    def paramDefDetails(self):
        return self._value[1]

    @paramDefDetails.setter
    def paramDefDetails(self, paramDefDetails):
        self._value[1] = ParameterDefinitionDetails(paramDefDetails, canBeNull=False, attribName='paramDefDetails')


class ParameterCreationRequestList(mal.ElementList):
    shortForm = -MALShortForm.PARAMETERCREATIONREQUEST

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
                 self._value.append(ParameterCreationRequest(v))


class ParameterRawValue(mal.Composite):
    """The ParameterRawValue structure holds a new raw value for a specific parameter."""

    shortForm = MALShortForm.PARAMETERRAWVALUE

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
            self._value = [None]*2
            self.paramInstId = value[0]
            self.rawValue = value[1]

    @property
    def paramInstId(self):
        return self._value[0]

    @paramInstId.setter
    def paramInstId(self, paramInstId):
        self._value[0] = mal.Long(paramInstId, canBeNull=False, attribName='paramInstId')

    @property
    def rawValue(self):
        return self._value[1]

    @rawValue.setter
    def rawValue(self, rawValue):
        self._value[1] = mal.Attribute(rawValue, canBeNull=True, attribName='rawValue')


class ParameterRawValueList(mal.ElementList):
    shortForm = -MALShortForm.PARAMETERRAWVALUE

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
                 self._value.append(ParameterRawValue(v))


class ParameterValueDetails(mal.Composite):
    """This structure holds a specific time stamped value of the parameter. The type of the value shall match that specified in the parameter definition."""

    shortForm = MALShortForm.PARAMETERVALUEDETAILS

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
            self._value = [None]*4
            self.paramId = value[0]
            self.defId = value[1]
            self.timestamp = value[2]
            self.value = value[3]

    @property
    def paramId(self):
        return self._value[0]

    @paramId.setter
    def paramId(self, paramId):
        self._value[0] = mal.Long(paramId, canBeNull=False, attribName='paramId')

    @property
    def defId(self):
        return self._value[1]

    @defId.setter
    def defId(self, defId):
        self._value[1] = mal.Long(defId, canBeNull=False, attribName='defId')

    @property
    def timestamp(self):
        return self._value[2]

    @timestamp.setter
    def timestamp(self, timestamp):
        self._value[2] = mal.Time(timestamp, canBeNull=False, attribName='timestamp')

    @property
    def value(self):
        return self._value[3]

    @value.setter
    def value(self, value):
        self._value[3] = ParameterValue(value, canBeNull=False, attribName='value')


class ParameterValueDetailsList(mal.ElementList):
    shortForm = -MALShortForm.PARAMETERVALUEDETAILS

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
                 self._value.append(ParameterValueDetails(v))


