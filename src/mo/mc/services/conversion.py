#####################################################
# Generated by generators/generator.py              #
# This file is generated. Do NOT edit it by hand.   #
#####################################################

"""The conversion service provides a set of basic conversion definition types that allows the specification of a conversion between two representations. These conversions are used by the other MC services (such as Action, Alert, and Parameter) to define conversions from raw field representations to some engineering representation.
Conversions are associated with other entities such as parameters or action/alert arguments through the configuration of the relevant service (action/alert/parameter).
The conversion service does not provide any operations directly, but allows consumers to add, remove, and modify conversion definitions via the COM archive."""

from enum import IntEnum
from mo import mal
from mo import com
from mo import mc

number = 7
class MALShortForm(IntEnum):
    DISCRETECONVERSIONDETAILS = 1
    LINECONVERSIONDETAILS = 2
    POLYCONVERSIONDETAILS = 3
    RANGECONVERSIONDETAILS = 4


class DiscreteConversionDetails(mal.Composite):
    """The DiscreteConversionDetails structure holds a bidirectional conversion between raw and converted values. The first element of the pair is the raw value and the second is the converted value. Both sets of values must be unique."""

    shortForm = MALShortForm.DISCRETECONVERSIONDETAILS

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
            self.mapping = value[0]

    @property
    def mapping(self):
        return self._value[0]

    @mapping.setter
    def mapping(self, mapping):
        self._value[0] = mal.PairList(mapping, canBeNull=False, attribName='mapping')


class DiscreteConversionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.DISCRETECONVERSIONDETAILS

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
                 self._value.append(DiscreteConversionDetails(v))


class LineConversionDetails(mal.Composite):
    """The LineConversionDetails structure is a bi-directional conversion between raw and converted values. It is defined by a series of points between which values are to be interpolated. The extrapolate attribute indicates if values can also be linearly extrapolated beyond the initial and final points."""

    shortForm = MALShortForm.LINECONVERSIONDETAILS

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
            self.extrapolate = value[0]
            self.points = value[1]

    @property
    def extrapolate(self):
        return self._value[0]

    @extrapolate.setter
    def extrapolate(self, extrapolate):
        self._value[0] = mal.Boolean(extrapolate, canBeNull=False, attribName='extrapolate')

    @property
    def points(self):
        return self._value[1]

    @points.setter
    def points(self, points):
        self._value[1] = mal.PairList(points, canBeNull=False, attribName='points')


class LineConversionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.LINECONVERSIONDETAILS

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
                 self._value.append(LineConversionDetails(v))


class PolyConversionDetails(mal.Composite):
    """The PolyConversionDetails structure holds only forward (raw to converted) polynomial conversions. They are defined by a series of points for the polynomial coefficients."""

    shortForm = MALShortForm.POLYCONVERSIONDETAILS

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
            self.points = value[0]

    @property
    def points(self):
        return self._value[0]

    @points.setter
    def points(self, points):
        self._value[0] = mal.PairList(points, canBeNull=False, attribName='points')


class PolyConversionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.POLYCONVERSIONDETAILS

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
                 self._value.append(PolyConversionDetails(v))


class RangeConversionDetails(mal.Composite):
    """The RangeConversionDetails structure holds a range for a one-way conversion to convert between a continuous range to a discrete value. A range is defined as from this point up to, but not including, the next point."""

    shortForm = MALShortForm.RANGECONVERSIONDETAILS

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
            self.points = value[0]

    @property
    def points(self):
        return self._value[0]

    @points.setter
    def points(self, points):
        self._value[0] = mal.PairList(points, canBeNull=False, attribName='points')


class RangeConversionDetailsList(mal.ElementList):
    shortForm = -MALShortForm.RANGECONVERSIONDETAILS

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
                 self._value.append(RangeConversionDetails(v))


