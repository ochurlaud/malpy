# SPDX-FileCopyrightText: 2025 Olivier Churlaud <olivier@churlaud.com>
# SPDX-FileCopyrightText: 2025 CNES
#
# SPDX-License-Identifier: MIT

#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The aggregation service allows the user to acquire several parameter values in a single request.
Aggregations are generated either periodically, on an ad-hoc basis, or after a configurable timeout when being filtered. Periodic is where they are generated at a specific generation interval; in this case the periodicity is an aspect of the aggregation rather than the contained parameters. Ad-hoc is when the aggregation generation is triggered by some other deployment-specific mechanism.
Filtering is where an aggregation is only generated when the change in the value of the filtered parameters exceeds a specified threshold or a timeout is passed. Filtering can be applied to both periodic and ad-hoc aggregations.
As there may be a large amount of time between reports of an aggregation when filtering is applied, the filtering concept also has a maximum reporting interval. If a report of the aggregation has not passed the filter in the maximum reporting interval a report is generated regardless. This allows there to be regular reports of an aggregation sent regardless of filtering.
It should be noted that applying a filter with a maximum reporting interval to an ad-hoc aggregation will cause the aggregation to generate reports in a periodic way if the maximum reporting interval is left to expire. This is expected behaviour.
There are a number of intervals defined in the structures of the service, the diagram in Figure 3-12 illustrates the use of these:
 insert timing diagram 
The diagram shows a single report of an aggregation being generated which contains two parameter sets. Each set of parameter values in the aggregation report contains two optional durations, delta time and interval time. 
<ul>
 <li>The timestamp of the first value of the first set (T1) is defined as the timestamp of the aggregation report plus the delta time of the first set.</li>
 <li>The timestamp of the second value of the first set (T2) is defined as the timestamp of the first parameter (T1) plus the interval time of the set.</li>
 <li>The timestamp of the first value of the second set (T3) is defined as the timestamp of the last value of the previous set (T2) plus the delta time of the second set.</li>
 <li>The timestamp of the second value of the second set (T4) is defined as the timestamp of the first parameter (T3) plus the interval time of the set.</li>
</ul>
The COM archive is used to hold the definitions of the aggregations."""

from enum import IntEnum
from malpy.mo import mal
from malpy.mo import com
from malpy.mo import mc

number = 6

# CapabilitySet 1
class MonitorValue(mal.PubSubProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 1



# CapabilitySet 2
class GetValue(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 2



# CapabilitySet 3
class EnableGeneration(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 3


class EnableFilter(mal.SubmitProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 4



# CapabilitySet 4
class ListDefinition(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 5



# CapabilitySet 5
class AddAggregation(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 6


class UpdateDefinition(mal.RequestProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 7


class RemoveAggregation(mal.SubmitProviderHandler):
    AREA = 4
    VERSION = 1
    SERVICE = 6
    OPERATION = 8


class MALShortForm(IntEnum):
    AGGREGATIONCATEGORY = 7
    THRESHOLDTYPE = 8
    GENERATIONMODE = 9
    AGGREGATIONDEFINITIONDETAILS = 1
    AGGREGATIONPARAMETERSET = 2
    AGGREGATIONVALUE = 3
    AGGREGATIONSETVALUE = 4
    AGGREGATIONPARAMETERVALUE = 5
    THRESHOLDFILTER = 6
    AGGREGATIONCREATIONREQUEST = 10
    AGGREGATIONVALUEDETAILS = 11


class AggregationCategoryEnum(IntEnum):
    """AggregationCategory is an enumeration definition holding the categories of aggregations."""

    GENERAL = 1  # General aggregation.
    DIAGNOSTIC = 2  # Diagnostic aggregation.


class AggregationCategory(mal.AbstractEnum):
    """AggregationCategory is an enumeration definition holding the categories of aggregations."""

    shortForm = MALShortForm.AGGREGATIONCATEGORY
    value_type = AggregationCategoryEnum


class AggregationCategoryList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONCATEGORY

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
                 self._internal_value.append(AggregationCategory(v))


class ThresholdTypeEnum(IntEnum):
    """ThresholdType is an enumeration definition holding the types of filtering thresholds."""

    PERCENTAGE = 1  # Threshold value is a percentage.
    DELTA = 2  # Threshold value is a delta.


class ThresholdType(mal.AbstractEnum):
    """ThresholdType is an enumeration definition holding the types of filtering thresholds."""

    shortForm = MALShortForm.THRESHOLDTYPE
    value_type = ThresholdTypeEnum


class ThresholdTypeList(mal.ElementList):
    shortForm = -MALShortForm.THRESHOLDTYPE

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
                 self._internal_value.append(ThresholdType(v))


class GenerationModeEnum(IntEnum):
    """GenerationMode is an enumeration definition holding the reasons for the aggregation to be generated."""

    ADHOC = 1  # The aggregation value was generated because of an ad-hoc implementation dependent reason.
    PERIODIC = 2  # The aggregation value was generated because of a periodic report.
    FILTERED_TIMEOUT = 3  # The item is filtered but it exceeded its timeout value.


class GenerationMode(mal.AbstractEnum):
    """GenerationMode is an enumeration definition holding the reasons for the aggregation to be generated."""

    shortForm = MALShortForm.GENERATIONMODE
    value_type = GenerationModeEnum


class GenerationModeList(mal.ElementList):
    shortForm = -MALShortForm.GENERATIONMODE

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
                 self._internal_value.append(GenerationMode(v))


class AggregationDefinitionDetails(mal.Composite):
    """The AggregationDefinitionDetails structure holds definition details of an aggregation."""

    shortForm = MALShortForm.AGGREGATIONDEFINITIONDETAILS
    _fieldNumber = mal.Composite._fieldNumber + 9

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*9
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
            self.reportInterval = value[mal.Composite._fieldNumber + 2]
            self.sendUnchanged = value[mal.Composite._fieldNumber + 3]
            self.sendDefinitions = value[mal.Composite._fieldNumber + 4]
            self.filterEnabled = value[mal.Composite._fieldNumber + 5]
            self.filteredTimeout = value[mal.Composite._fieldNumber + 6]
            self.generationEnabled = value[mal.Composite._fieldNumber + 7]
            self.parameterSets = value[mal.Composite._fieldNumber + 8]

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
    def reportInterval(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @reportInterval.setter
    def reportInterval(self, reportInterval):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.Duration(reportInterval, canBeNull=False, attribName='reportInterval')
        self._isNull = False

    @property
    def sendUnchanged(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @sendUnchanged.setter
    def sendUnchanged(self, sendUnchanged):
        self._internal_value[mal.Composite._fieldNumber + 3] = mal.Boolean(sendUnchanged, canBeNull=False, attribName='sendUnchanged')
        self._isNull = False

    @property
    def sendDefinitions(self):
        return self._internal_value[mal.Composite._fieldNumber + 4]

    @sendDefinitions.setter
    def sendDefinitions(self, sendDefinitions):
        self._internal_value[mal.Composite._fieldNumber + 4] = mal.Boolean(sendDefinitions, canBeNull=False, attribName='sendDefinitions')
        self._isNull = False

    @property
    def filterEnabled(self):
        return self._internal_value[mal.Composite._fieldNumber + 5]

    @filterEnabled.setter
    def filterEnabled(self, filterEnabled):
        self._internal_value[mal.Composite._fieldNumber + 5] = mal.Boolean(filterEnabled, canBeNull=False, attribName='filterEnabled')
        self._isNull = False

    @property
    def filteredTimeout(self):
        return self._internal_value[mal.Composite._fieldNumber + 6]

    @filteredTimeout.setter
    def filteredTimeout(self, filteredTimeout):
        self._internal_value[mal.Composite._fieldNumber + 6] = mal.Duration(filteredTimeout, canBeNull=False, attribName='filteredTimeout')
        self._isNull = False

    @property
    def generationEnabled(self):
        return self._internal_value[mal.Composite._fieldNumber + 7]

    @generationEnabled.setter
    def generationEnabled(self, generationEnabled):
        self._internal_value[mal.Composite._fieldNumber + 7] = mal.Boolean(generationEnabled, canBeNull=False, attribName='generationEnabled')
        self._isNull = False

    @property
    def parameterSets(self):
        return self._internal_value[mal.Composite._fieldNumber + 8]

    @parameterSets.setter
    def parameterSets(self, parameterSets):
        self._internal_value[mal.Composite._fieldNumber + 8] = AggregationParameterSetList(parameterSets, canBeNull=False, attribName='parameterSets')
        self._isNull = False


class AggregationDefinitionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONDEFINITIONDETAILS

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
                 self._internal_value.append(AggregationDefinitionDetails(v))


class AggregationParameterSet(mal.Composite):
    """The AggregationParameterSet structure holds the identifier and optional filter for a parameter, or set of parameters, in an aggregation."""

    shortForm = MALShortForm.AGGREGATIONPARAMETERSET
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
            self.domain = value[mal.Composite._fieldNumber + 0]
            self.parameters = value[mal.Composite._fieldNumber + 1]
            self.sampleInterval = value[mal.Composite._fieldNumber + 2]
            self.reportFilter = value[mal.Composite._fieldNumber + 3]

    @property
    def domain(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @domain.setter
    def domain(self, domain):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.IdentifierList(domain, canBeNull=True, attribName='domain')
        self._isNull = False

    @property
    def parameters(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @parameters.setter
    def parameters(self, parameters):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.LongList(parameters, canBeNull=False, attribName='parameters')
        self._isNull = False

    @property
    def sampleInterval(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @sampleInterval.setter
    def sampleInterval(self, sampleInterval):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.Duration(sampleInterval, canBeNull=False, attribName='sampleInterval')
        self._isNull = False

    @property
    def reportFilter(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @reportFilter.setter
    def reportFilter(self, reportFilter):
        self._internal_value[mal.Composite._fieldNumber + 3] = ThresholdFilter(reportFilter, canBeNull=True, attribName='reportFilter')
        self._isNull = False


class AggregationParameterSetList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONPARAMETERSET

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
                 self._internal_value.append(AggregationParameterSet(v))


class AggregationValue(mal.Composite):
    """The AggregationValue structure holds the values for one or more sets of parameter values. The value sets must be held in the same order as that defined in the matching AggregationDefinitionDetails."""

    shortForm = MALShortForm.AGGREGATIONVALUE
    _fieldNumber = mal.Composite._fieldNumber + 3

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*3
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
            self.generationMode = value[mal.Composite._fieldNumber + 0]
            self.filtered = value[mal.Composite._fieldNumber + 1]
            self.parameterSetValues = value[mal.Composite._fieldNumber + 2]

    @property
    def generationMode(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @generationMode.setter
    def generationMode(self, generationMode):
        self._internal_value[mal.Composite._fieldNumber + 0] = GenerationMode(generationMode, canBeNull=False, attribName='generationMode')
        self._isNull = False

    @property
    def filtered(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @filtered.setter
    def filtered(self, filtered):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Boolean(filtered, canBeNull=False, attribName='filtered')
        self._isNull = False

    @property
    def parameterSetValues(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @parameterSetValues.setter
    def parameterSetValues(self, parameterSetValues):
        self._internal_value[mal.Composite._fieldNumber + 2] = AggregationSetValueList(parameterSetValues, canBeNull=False, attribName='parameterSetValues')
        self._isNull = False


class AggregationValueList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONVALUE

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
                 self._internal_value.append(AggregationValue(v))


class AggregationSetValue(mal.Composite):
    """The AggregationSetValue structure holds the values for one set of parameter values. If the definition sendUnchanged field is set to FALSE parameter values that are unchanged since the previous report are replaced by a NULL in this list. The parameter values must be held in the same order as that defined in the matching AggregationDefinitionDetails."""

    shortForm = MALShortForm.AGGREGATIONSETVALUE
    _fieldNumber = mal.Composite._fieldNumber + 3

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*3
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
            self.deltaTime = value[mal.Composite._fieldNumber + 0]
            self.intervalTime = value[mal.Composite._fieldNumber + 1]
            self.values = value[mal.Composite._fieldNumber + 2]

    @property
    def deltaTime(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @deltaTime.setter
    def deltaTime(self, deltaTime):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Duration(deltaTime, canBeNull=True, attribName='deltaTime')
        self._isNull = False

    @property
    def intervalTime(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @intervalTime.setter
    def intervalTime(self, intervalTime):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Duration(intervalTime, canBeNull=True, attribName='intervalTime')
        self._isNull = False

    @property
    def values(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @values.setter
    def values(self, values):
        self._internal_value[mal.Composite._fieldNumber + 2] = AggregationParameterValueList(values, canBeNull=False, attribName='values')
        self._isNull = False


class AggregationSetValueList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONSETVALUE

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
                 self._internal_value.append(AggregationSetValue(v))


class AggregationParameterValue(mal.Composite):
    """The structure holds a single parameter value with its definition instance identifier."""

    shortForm = MALShortForm.AGGREGATIONPARAMETERVALUE
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
            self.value = value[mal.Composite._fieldNumber + 0]
            self.paramDefInstId = value[mal.Composite._fieldNumber + 1]

    @property
    def value(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @value.setter
    def value(self, value):
        self._internal_value[mal.Composite._fieldNumber + 0] = mc.services.parameter.ParameterValue(value, canBeNull=False, attribName='value')
        self._isNull = False

    @property
    def paramDefInstId(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @paramDefInstId.setter
    def paramDefInstId(self, paramDefInstId):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Long(paramDefInstId, canBeNull=True, attribName='paramDefInstId')
        self._isNull = False


class AggregationParameterValueList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONPARAMETERVALUE

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
                 self._internal_value.append(AggregationParameterValue(v))


class ThresholdFilter(mal.Composite):
    """The ThresholdFilter structure holds the filter for a parameter."""

    shortForm = MALShortForm.THRESHOLDFILTER
    _fieldNumber = mal.Composite._fieldNumber + 3

    def __init__(self, value=None, canBeNull=True, attribName=None):
        super().__init__(value, canBeNull, attribName)
        self._internal_value += [None]*3
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
            self.thresholdType = value[mal.Composite._fieldNumber + 0]
            self.thresholdValue = value[mal.Composite._fieldNumber + 1]
            self.useConverted = value[mal.Composite._fieldNumber + 2]

    @property
    def thresholdType(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @thresholdType.setter
    def thresholdType(self, thresholdType):
        self._internal_value[mal.Composite._fieldNumber + 0] = ThresholdType(thresholdType, canBeNull=False, attribName='thresholdType')
        self._isNull = False

    @property
    def thresholdValue(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @thresholdValue.setter
    def thresholdValue(self, thresholdValue):
        if thresholdValue is None:
            self._internal_value[mal.Composite._fieldNumber + 1] = mal.Attribute(thresholdValue, canBeNull=False, attribName='thresholdValue')
        else:
            self._internal_value[mal.Composite._fieldNumber + 1] = type(thresholdValue)(thresholdValue, canBeNull=False, attribName='thresholdValue')
        self._isNull = False

    @property
    def useConverted(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @useConverted.setter
    def useConverted(self, useConverted):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.Boolean(useConverted, canBeNull=False, attribName='useConverted')
        self._isNull = False


class ThresholdFilterList(mal.ElementList):
    shortForm = -MALShortForm.THRESHOLDFILTER

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
                 self._internal_value.append(ThresholdFilter(v))


class AggregationCreationRequest(mal.Composite):
    """The AggregationCreationRequest contains all the fields required when creating a new aggregation in a provider."""

    shortForm = MALShortForm.AGGREGATIONCREATIONREQUEST
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
            self.aggDefDetails = value[mal.Composite._fieldNumber + 1]

    @property
    def name(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @name.setter
    def name(self, name):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Identifier(name, canBeNull=False, attribName='name')
        self._isNull = False

    @property
    def aggDefDetails(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @aggDefDetails.setter
    def aggDefDetails(self, aggDefDetails):
        self._internal_value[mal.Composite._fieldNumber + 1] = AggregationDefinitionDetails(aggDefDetails, canBeNull=False, attribName='aggDefDetails')
        self._isNull = False


class AggregationCreationRequestList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONCREATIONREQUEST

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
                 self._internal_value.append(AggregationCreationRequest(v))


class AggregationValueDetails(mal.Composite):
    """This structure holds a specific time stamped value of the aggregation. """

    shortForm = MALShortForm.AGGREGATIONVALUEDETAILS
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
            self.aggId = value[mal.Composite._fieldNumber + 0]
            self.defId = value[mal.Composite._fieldNumber + 1]
            self.timestamp = value[mal.Composite._fieldNumber + 2]
            self.value = value[mal.Composite._fieldNumber + 3]

    @property
    def aggId(self):
        return self._internal_value[mal.Composite._fieldNumber + 0]

    @aggId.setter
    def aggId(self, aggId):
        self._internal_value[mal.Composite._fieldNumber + 0] = mal.Long(aggId, canBeNull=False, attribName='aggId')
        self._isNull = False

    @property
    def defId(self):
        return self._internal_value[mal.Composite._fieldNumber + 1]

    @defId.setter
    def defId(self, defId):
        self._internal_value[mal.Composite._fieldNumber + 1] = mal.Long(defId, canBeNull=False, attribName='defId')
        self._isNull = False

    @property
    def timestamp(self):
        return self._internal_value[mal.Composite._fieldNumber + 2]

    @timestamp.setter
    def timestamp(self, timestamp):
        self._internal_value[mal.Composite._fieldNumber + 2] = mal.Time(timestamp, canBeNull=False, attribName='timestamp')
        self._isNull = False

    @property
    def value(self):
        return self._internal_value[mal.Composite._fieldNumber + 3]

    @value.setter
    def value(self, value):
        self._internal_value[mal.Composite._fieldNumber + 3] = AggregationValue(value, canBeNull=False, attribName='value')
        self._isNull = False


class AggregationValueDetailsList(mal.ElementList):
    shortForm = -MALShortForm.AGGREGATIONVALUEDETAILS

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
                 self._internal_value.append(AggregationValueDetails(v))


