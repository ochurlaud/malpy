#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The action service allows consumers to submit an action for execution and to subsequently monitor the execution progress of these actions via the COM activity tracking pattern. The progress of the action is split into two parts, firstly transfer from the consumer to the provider, and secondly execution in the provider.
An action is submitted to the provider using the submitAction operation, the progress of which can be monitored using the COM activity tracking pattern, which completes when the action has been delivered to the provider. The action is then executed in the provider which can also be monitored using the activity tracking pattern. The submitAction operation takes the object instance identifier of the submitted action and uses that to populate the source fields of the activity tracking events. Coordination may be required between action service consumers to ensure the action object instance identifiers are unique. How this is done is outside the scope of this specification however a good approach is the use of a central COM archive as that can provide the unique instance identifiers.
The nominal sequence of action submission and execution monitoring are shown in Figure 3-1:
 insert sequence diag here 
The consumer is responsible for creating and archiving the action instance object and then using the submitAction operation to submit it to the action provider for execution. The action provider reports, using the COM ActivityTracking service, both the execution progress of the submitAction operation and also the execution of the action itself. Once the supplied action instance details have been checked and execution of the action started by the submitAction operation, that operation finishes, whilst the execution of the action possibly continues (depends on the actual action). The final interaction in the sequence shows the execution events of the executing action instance, the '*' at the start of that line indicates zero to many events being published.
If the execution of an action fails with an error, the action service provider can publish an ActionFailure COM event to hold the error code being reported by the failure. If no error code is required to be reported then there is no need to publish the event as the normal COM ActivityTracking event contains a success indication.
The service also includes an operation, preCheckAction, which checks that an action would be accepted for execution without actually submitting it for execution. It is expected to be provided by local action proxies, rather than the remote system, to allow for localised checking of things such as link state, argument values, action safety, before sending the action over long and slow space links.
The action service defines three types of objects, the first type is the ActionIdentity object that holds the name of an action. The second type is the ActionDefinition object that holds the description of an action with the list of required/optional arguments. The third type is the ActionInstance object that holds details of a specific action instance namely a value for each of the arguments of the action."""

from enum import IntEnum
from mo import mal
from mo import com
from mo import mc

number = 1

# CapabilitySet 1
class SubmitAction(mal.SubmitProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 1
    OPERATION = 1


class PreCheckAction(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 1
    OPERATION = 2



# CapabilitySet 2
class ListDefinition(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 1
    OPERATION = 3



# CapabilitySet 3
class AddAction(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 1
    OPERATION = 4


class UpdateDefinition(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 1
    OPERATION = 5


class RemoveAction(mal.SubmitProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 1
    OPERATION = 6


class MALShortForm(IntEnum):
    ACTIONCATEGORY = 4
    ACTIONDEFINITIONDETAILS = 1
    ACTIONINSTANCEDETAILS = 2
    ACTIONCREATIONREQUEST = 3


class ActionCategoryEnum(IntEnum):
    """Contains the default Action category values. It is implementation specific what the meaning of the values are in a particular context."""

    DEFAULT = 1  # Default category
    HIPRIORITY = 2  # Category for high priority actions
    CRITICAL = 3  # Category for critical actions


class ActionCategory(mal.AbstractEnum):
    """Contains the default Action category values. It is implementation specific what the meaning of the values are in a particular context."""

    shortForm = MALShortForm.ACTIONCATEGORY
    value_type = ActionCategoryEnum


class ActionCategoryList(mal.ElementList):
    shortForm = -MALShortForm.ACTIONCATEGORY

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
                 self._internal_value.append(ActionCategory(v))


class ActionDefinitionDetails(mal.Composite):
    """The ActionDefinitionDetails structure holds the definition information of an action."""

    shortForm = MALShortForm.ACTIONDEFINITIONDETAILS
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
            self.category = value[mal.Composite._fieldNumber + 1]
            self.progressStepCount = value[mal.Composite._fieldNumber + 2]
            self.arguments = value[mal.Composite._fieldNumber + 3]

    @property
    def description(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @description.setter
    def description(self, description):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.String(description, canBeNull=False, attribName='description')
        self._isNull = False

    @property
    def category(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @category.setter
    def category(self, category):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.UOctet(category, canBeNull=False, attribName='category')
        self._isNull = False

    @property
    def progressStepCount(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @progressStepCount.setter
    def progressStepCount(self, progressStepCount):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.UShort(progressStepCount, canBeNull=False, attribName='progressStepCount')
        self._isNull = False

    @property
    def arguments(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @arguments.setter
    def arguments(self, arguments):
        self._internal_value[mal.Composite._fieldNumber + 3] = mc.ArgumentDefinitionDetailsList(arguments, canBeNull=True, attribName='arguments')
        self._isNull = False


class ActionDefinitionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.ACTIONDEFINITIONDETAILS

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
                 self._internal_value.append(ActionDefinitionDetails(v))


class ActionInstanceDetails(mal.Composite):
    """The ActionInstanceDetails structure holds the information required for an instance of an Action such as the argument values to use."""

    shortForm = MALShortForm.ACTIONINSTANCEDETAILS
    _fieldNumber = mal.Composite._fieldNumber + 7

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*7
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
            self.defInstId = value[mal.Composite._fieldNumber + 0]
            self.stageStartedRequired = value[mal.Composite._fieldNumber + 1]
            self.stageProgressRequired = value[mal.Composite._fieldNumber + 2]
            self.stageCompletedRequired = value[mal.Composite._fieldNumber + 3]
            self.argumentValues = value[mal.Composite._fieldNumber + 4]
            self.argumentIds = value[mal.Composite._fieldNumber + 5]
            self.isRawValue = value[mal.Composite._fieldNumber + 6]

    @property
    def defInstId(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @defInstId.setter
    def defInstId(self, defInstId):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Long(defInstId, canBeNull=False, attribName='defInstId')
        self._isNull = False

    @property
    def stageStartedRequired(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @stageStartedRequired.setter
    def stageStartedRequired(self, stageStartedRequired):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Boolean(stageStartedRequired, canBeNull=False, attribName='stageStartedRequired')
        self._isNull = False

    @property
    def stageProgressRequired(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @stageProgressRequired.setter
    def stageProgressRequired(self, stageProgressRequired):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.Boolean(stageProgressRequired, canBeNull=False, attribName='stageProgressRequired')
        self._isNull = False

    @property
    def stageCompletedRequired(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @stageCompletedRequired.setter
    def stageCompletedRequired(self, stageCompletedRequired):
        self._internal_value[mal.Composite._fieldNumber + 3] = mal.Boolean(stageCompletedRequired, canBeNull=False, attribName='stageCompletedRequired')
        self._isNull = False

    @property
    def argumentValues(self):
        return self._internal_value[mal.Composite._fieldNumber + 4]

    @argumentValues.setter
    def argumentValues(self, argumentValues):
        self._internal_value[mal.Composite._fieldNumber + 4] = mc.AttributeValueList(argumentValues, canBeNull=True, attribName='argumentValues')
        self._isNull = False

    @property
    def argumentIds(self):
        return self._internal_value[mal.Composite._fieldNumber + 5]

    @argumentIds.setter
    def argumentIds(self, argumentIds):
        self._internal_value[mal.Composite._fieldNumber + 5] = mal.IdentifierList(argumentIds, canBeNull=True, attribName='argumentIds')
        self._isNull = False

    @property
    def isRawValue(self):
        return self._internal_value[mal.Composite._fieldNumber + 6]

    @isRawValue.setter
    def isRawValue(self, isRawValue):
        self._internal_value[mal.Composite._fieldNumber + 6] = mal.BooleanList(isRawValue, canBeNull=True, attribName='isRawValue')
        self._isNull = False


class ActionInstanceDetailsList(mal.ElementList):
    shortForm = -MALShortForm.ACTIONINSTANCEDETAILS

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
                 self._internal_value.append(ActionInstanceDetails(v))


class ActionCreationRequest(mal.Composite):
    """The ActionCreationRequest contains all the fields required when creating a new action in a provider."""

    shortForm = MALShortForm.ACTIONCREATIONREQUEST
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
            self.actionDefDetails = value[mal.Composite._fieldNumber + 1]

    @property
    def name(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @name.setter
    def name(self, name):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Identifier(name, canBeNull=False, attribName='name')
        self._isNull = False

    @property
    def actionDefDetails(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @actionDefDetails.setter
    def actionDefDetails(self, actionDefDetails):
        self._internal_value[mal.Composite._fieldNumber + 1] = ActionDefinitionDetails(actionDefDetails, canBeNull=False, attribName='actionDefDetails')
        self._isNull = False


class ActionCreationRequestList(mal.ElementList):
    shortForm = -MALShortForm.ACTIONCREATIONREQUEST

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
                 self._internal_value.append(ActionCreationRequest(v))


