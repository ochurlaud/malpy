#! /bin/python3

import os
import xml.etree.ElementTree as ET
import yaml

MO_XML = {
    'MAL': "../xml/area001-v003-MAL.xml",
    'MC': "../xml/area004-v002-MC.xml",
    'MPD': "../xml/area009-v001-MPD.xml"
    }
AREA_TO_GENERATE = ['MAL', 'MC', 'MPD']
MAL_NS = "http://www.ccsds.org/schema/ServiceSchema"
COM_NS = "http://www.ccsds.org/schema/COMSchema"
OUTFILE = "../src/malpy/mo"
IMPORTS = {
    'MAL': [
        'from enum import IntEnum',
        'from abc import ABC'
        ],
    'MC': [
        'from enum import IntEnum',
        'from malpy.mo import mal'
        ],
   'MPD': [
        'from enum import IntEnum',
        'from malpy.mo import mal'
        ]
    }
PARAMFILE = 'parameters.yaml'

DO_NOT_EDIT = \
"#####################################################\n" + \
"# Generated by generators/generator.py              #\n" + \
"# This file is generated. Do NOT edit it by hand.   #\n" + \
"#####################################################\n\n"


def maltag(name):
    return "{}{}".format('{' + MAL_NS + '}', name)


def comtag(name):
    return "{}{}".format('{' + COM_NS + '}', name)


OPERATIONTYPE = {
    maltag('sendIP'): "Send",
    maltag('requestIP'): "Request",
    maltag('submitIP'): "Submit",
    maltag('invokeIP'): "Invoke",
    maltag('progressIP'): "Progress",
    maltag('pubsubIP'): "PubSub"
    }


MESSAGETYPE = {
    maltag('send'): "SEND",
    maltag('request'): "REQUEST",
    maltag('response'): "RESPONSE",
    maltag('submit'): "SUBMIT",
    maltag('invoke'): "INVOKE",
    maltag('acknowledgement'): "ACK",
    maltag('progress'): "PROGRESS",
    maltag('update'): "UPDATE",
    maltag('publishNotify'): "PUBLISH"
    }


def _parse_datatype(node):
    if node.tag == maltag('fundamental') or node.tag == maltag('attribute'):
        return MALElementXML(node)
    elif node.tag == maltag('composite'):
        return MALCompositeXML(node)
    elif node.tag == maltag('enumeration'):
        return MALEnumerationXML(node)
    else:
        raise RuntimeError("Unexpected node tag : {}".format(node.tag))


def _parse_datatypes(node):
    datatypes_dict = {}
    for subnode in node:
        d = _parse_datatype(subnode)
        dtype = d.datatype
        if dtype not in datatypes_dict:
            datatypes_dict[dtype] = dict()
        datatypes_dict[dtype][d.name] = d
    return datatypes_dict


def _parse_service(node):
    return MALServiceXML(node)


def _parse_errors(node):
    error_dict = {}
    for subnode in node:
        d = MALErrorXML(subnode)
        error_dict[d.name] = d
    return error_dict


class MALAreaXML(object):
    __slots__ = ['name', 'number', 'version', 'comment']

    def __init__(self, node=None):
        self.name = None
        self.number = None
        self.version = None
        self.comment = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        if node.tag != maltag('area'):
            raise RuntimeError("Expected an area")
        self.name = node.attrib['name']
        self.number = node.attrib['number']
        self.version = node.attrib['version']
        if 'comment' in node.attrib:
            self.comment = node.attrib['comment']


class MALMessageFieldXML(object):
    def __init__(self, node=None):
        self.name = None
        self.comment = None
        self.fieldtype = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        if 'comment' in node.attrib:
            self.comment = node.attrib['comment']
        if len(node) != 1:
            raise RuntimeError("In {}, mal:field has more than one subnode".format(self.name))
        typenode = list(node)[0]
        self.fieldType = MALTypeXML(typenode)


class MALMessageXML(object):
    def __init__(self, node=None):
        self.messageType = None
        self.fields = []
        if node is not None:
            self.parse(node)

    def parse(self, node):
        if node.tag == '{http://www.ccsds.org/schema/ServiceSchema}subscriptionKeys':
            print("SubscriptionKeys !!!  Not takenintoAccount")
            return
        self.messageType = MESSAGETYPE[node.tag]
        for subnode in node:
            self.fields.append(MALMessageFieldXML(subnode))


class MALOperationXML(object):
    __slots__ = ['name', 'number', 'comment', 'supportReplay', 'interactionType', 'messages', 'errors']

    def __init__(self, node=None):
        self.name = None
        self.number = None
        self.comment = None
        self.supportReplay = None
        self.interactionType = None
        self.messages = []
        self.errors = []
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.number = int(node.attrib['number'])
        if 'comment' in node.attrib:
            self.comment = node.attrib['comment']
        self.supportReplay = node.attrib['supportInReplay'] == "true"
        self.interactionType = OPERATIONTYPE[node.tag]
        for subnode in node:
            if subnode.tag == maltag('messages'):
                for ssubnode in subnode:
                    self.messages.append(MALMessageXML(ssubnode))
            elif subnode.tag == maltag('errors'):
                print("TODO: errors")
                # errors
                # - errorRef:
                #     type
                #     comment
                #     extrainfo:
                #       comment
                #       type
                # - errorRef
                #self.errors.append( ???(subnode))
            else:
                raise RuntimeError("Did not expect a {} tag in a MALOperation".format(subnode.tag))


class MALServiceDocumentationXML(object):
    __slots__ = ['title', 'order', 'text']

    def __init__(self, node=None):
        self.title = None
        self.order = None
        self.text = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.title = node.attrib['name']
        self.order = int(node.attrib['order'])
        self.text = node.text


class MALCapabilitySetXML(object):
    __slots__ = ['number', 'operations']

    def __init__(self, node=None):
        self.number = None
        self.operations = []
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.number = node.attrib['number']
        for subnode in node:
            self.operations.append(MALOperationXML(subnode))


class MALServiceXML(object):
    __slots__ = ['name', 'number', 'comment', 'documentation', 'capabilitySets', 'features', 'datatypes']

    def __init__(self, node=None):
        self.name = None
        self.number = None
        self.comment = None
        self.documentation = []
        self.capabilitySets = []
        self.features = None
        self.datatypes = []
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.number = node.attrib['number']
        if 'comment' in node.attrib:
            self.comment = node.attrib['comment']
        for subnode in node:
            if subnode.tag == maltag('documentation'):
                self.documentation.append(MALServiceDocumentationXML(subnode))
            elif subnode.tag == maltag('capabilitySet'):
                self.capabilitySets.append(MALCapabilitySetXML(subnode))
            elif subnode.tag == comtag('features'):
                # We don't need features for implementation
                continue
            elif subnode.tag == maltag('dataTypes'):
                self.datatypes = _parse_datatypes(subnode)
            else:
                raise NotImplementedError("Node type {} was not implemented".format(subnode.tag))


class MALElementXML(object):
    __slots__ = ['name', 'fundamental', 'shortFormPart', 'comment', 'extends']
    datatype = "Element"

    def __init__(self, node=None):
        self.fundamental = False
        self.name = None
        self.comment = None
        self.extends = None
        self.shortFormPart = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.fundamental = (node.tag == maltag('fundamental'))
        self.shortFormPart = node.attrib.get('shortFormPart', None)
        self.comment = node.attrib.get('comment', None)
        if node.tag == maltag('attribute'):
            self.extends = MALTypeXML()
            self.extends.area = 'MAL'
            self.extends.name = 'Attribute'
            self.extends.isList = False
        elif len(node) > 0:
            extends_node = list(node)[0]
            if extends_node.tag == maltag('extends'):
                if len(extends_node) != 1:
                    raise RuntimeError("In {}, mal:extends has more than one subnode".format(self.name))
                self.extends = MALTypeXML(list(extends_node)[0])
            else:
                raise NotImplementedError("Node type {} was not implemented".format(extends_node.tag))

        else:
            self.extends = None


class MALTypeXML(object):
    __slots__ = ['name', 'area', 'isList', 'service']
    datatype = "Type"

    def __init__(self, node=None):
        self.name = None
        self.area = None
        self.isList = False
        self.service = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.area = node.attrib['area']
        if 'service' in node.attrib:
            self.service = node.attrib['service']
        self.isList = (node.attrib.get('list', 'false') == 'true')


class MALCompositeFieldXML(object):
    __slots__ = ['name', 'comment', 'canBeNull', 'maltype']
    datatype = "CompositeField"

    def __init__(self, node=None):
        self.name = None
        self.comment = None
        self.canBeNull = None
        self.maltype = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.canBeNull = (node.attrib.get('canBeNull', 'true') == 'true')
        self.comment = node.get('comment', None)
        if len(list(node)) != 1:
            raise RuntimeError("In {}, mal:field has more than one subnode".format(self.name))
        self.maltype = MALTypeXML(list(node)[0])


class MALCompositeXML(object):
    __slots__ = ['name', 'comment', 'shortFormPart', 'extends', 'fields']
    datatype = "Composite"

    def __init__(self, node=None):
        self.name = None
        self.comment = None
        self.extends = None
        self.shortFormPart = None
        self.fields = []
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.shortFormPart = node.attrib.get('shortFormPart', None)
        self.comment = node.attrib.get('comment', None)
        for subnode in node:
            if subnode.tag == maltag('extends'):
                if len(list(subnode)) != 1:
                    raise RuntimeError("In {}, mal:extends has more than one subnode".format(self.name))
                self.extends = MALTypeXML(list(subnode)[0])
            elif subnode.tag == maltag("field"):
                self.fields.append(MALCompositeFieldXML(subnode))
            else:
                raise RuntimeError("Did not expect {} tag in Composite.".format(subnode.tag))


class MALEnumerationItemXML(object):
    __slots__ = ['value', 'nvalue', 'comment']
    datatype = "EnumerationItem"

    def __init__(self, node=None):
        self.value = None
        self.comment = None
        self.nvalue = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        if node.tag != maltag('item'):
            raise RuntimeError("Expected 'item', got {}".format(node.tag))
        self.value = node.attrib['value']
        self.nvalue = node.attrib['nvalue']
        self.comment = node.attrib.get('comment', None)


class MALEnumerationXML(object):
    __slots__ = ['name', 'comment', 'shortFormPart', 'items']
    datatype = "Enumeration"

    def __init__(self, node=None):
        self.name = None
        self.shortFormPart = None
        self.comment = None
        self.items = []
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name']
        self.shortFormPart = node.attrib['shortFormPart']
        self.comment = node.attrib.get('comment', None)
        item_nodes = list(node)
        for item_node in item_nodes:
            self.items.append(MALEnumerationItemXML(item_node))


class MALErrorXML(object):
    __slots__ = ['name', 'number', 'comment']
    datatype = "Error"

    def __init__(self, node=None):
        self.name = None
        self.comment = None
        self.number = None
        if node is not None:
            self.parse(node)

    def parse(self, node):
        self.name = node.attrib['name'].replace(' ', '_')
        self.number = node.attrib['number']
        self.comment = node.attrib.get('comment', None)


class MALBuffer(object):

    def __init__(self, generator, servicename=None):
        self.generator = generator
        self.service = servicename
        self.content = DO_NOT_EDIT

    def write(self, content):
        self.content += content

    def _element_completename(self, elementtype):
        # case maltypes
        if not self.service:
            # same area
            if elementtype.area == self.generator.area.name:
                return elementtype.name
            # different area
            else:
                return "{}.{}".format(elementtype.area.lower(), elementtype.name)
        # case service
        else:
            # pure maltype
            if not elementtype.service:
                return "{}.{}".format(elementtype.area.lower(), elementtype.name)
            # same service
            elif elementtype.service.lower() == self.service:
                return elementtype.name
            # other service
            else:
                return "{}.{}.{}.{}".format(elementtype.area.lower(),
                                            "services",
                                            elementtype.service.lower(),
                                            elementtype.name
                                            )

    def _element_parentclass(self, d, force_parent=None):
        if force_parent is not None:
            return self._element_completename(force_parent)
        elif d.__getattribute__('extends') is None or d.extends is None:
            return 'ABC'
        else:
            return self._element_completename(d.extends)

    def write_module_header(self):
        self.write(
    "\"\"\"{}\"\"\"\n\n".format(self.generator.area.comment) +
    "{}\n".format("\n".join(IMPORTS[self.generator.area.name])) +
    "\n" +
    "name = \"{}\"\n".format(self.generator.area.name) +
    "number = {}\n".format(self.generator.area.number) +
    "version = {}\n".format(self.generator.area.version) +
    "\n"
        )

    def write_shortforms(self, data_types):
        if not data_types:
            return
        self.write(
    "class MALShortForm(IntEnum):\n"
        )
        for dtype in data_types:
            for _, d in data_types[dtype].items():
                if d.shortFormPart:
                    self.write(
    "    {shortform} = {number}\n".format(shortform=d.name.upper(), number=d.shortFormPart)
                    )

        self.write("\n")
        self.write("\n")

    def write_errors(self, error_dict):
        errors = error_dict.values()
        self.write(
    "class {}({}):\n".format("Errors", "IntEnum") +
    "    \"\"\"All MAL errors.\"\"\"\n"
        )
        self.write("\n")

        for e in errors:
            self.write(4*' ' + "{} = {}".format(e.name, e.number))
            if e.comment is not None:
                self.write('  # ' + e.comment)
            self.write('\n')

        self.write("\n")
        self.write("\n")

    def write_enumeration_class(self, d):
        self.write(
    "class {}Enum({}):\n".format(d.name, "IntEnum") +
    "    \"\"\"{classdoc}\"\"\"\n".format(classdoc=d.comment)
        )
        self.write('\n')
        for item in d.items:
            self.write(
    "    {name} = {nvalue}".format(name=item.value, nvalue=item.nvalue)
            )
            if item.comment is not None:
                self.write('  # ' + item.comment)
                self.write('\n')
        self.write("\n")
        self.write("\n")

        enumType = MALTypeXML()
        enumType.area = "MAL"
        enumType.name = "AbstractEnum"
        self.write(
    "class {}({}):\n".format(d.name, self._element_completename(enumType)) +
    "    \"\"\"{classdoc}\"\"\"\n".format(classdoc=d.comment) +
    "\n" +
    "    shortForm = {namespace}.{name}\n".format(namespace="MALShortForm",name=d.name.upper()) +
    "    value_type = {}\n".format(d.name + 'Enum') +
    "\n\n"
        )

    def write_element_class(self, d, blocks=[]):
        parentclass = self._element_parentclass(d)

        self.write(
    "class {}({}):\n".format(d.name, parentclass) +
    "    \"\"\"{classdoc}\"\"\"\n".format(classdoc=d.comment) +
    "\n"
    )
        if d.shortFormPart:
            self.write(
    "    shortForm = {namespace}.{name}\n".format(namespace="MALShortForm",name=d.name.upper())
            )
        else:
            self.write(
    "    shortForm = None\n"
            )

        if d.name in self.generator.typedict:
            self.write(
    "    value_type = {typename}\n".format(typename=self.generator.typedict[d.name])
            )

        if d.name in self.generator.ctrldict:
            self.write("\n")
            minvalue = self.generator.ctrldict[d.name][0]
            maxvalue = self.generator.ctrldict[d.name][1]
            self.write(
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n" +
    "        super().__init__(value, canBeNull, attribName)\n" +
    "        if type(value) == int and ( value < {} or value > {} ):\n".format(minvalue, maxvalue) +
    "            raise ValueError(\"Authorized value is between {} and {}.\")\n".format(minvalue, maxvalue)
            )

        for b in blocks:
            self.write("\n")
            self.write(b)
        self.write("\n")
        self.write("\n")

    def write_abstractelement_class(self, d):
        blockelement = [
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n"
    "        self._isNull = False\n"
    "        self._canBeNull = canBeNull\n"
    "        self.attribName = attribName\n"
    "        if value is None and not self._canBeNull:\n"
    "            raise ValueError('This {} cannot be None.'.format(type(self).__name__))\n"
        ,
    "    @property\n"
    "    def internal_value(self):\n"
    "        if self._isNull:\n"
    "            return None\n"
    "        else:\n"
    "            return self._internal_value\n"
        ]
        self.write_element_class(d, blockelement)

    def write_abstractelementlist_class(self):
        self.write(
    "class {}({}):\n".format("ElementList", "Element") +
    "    shortForm = None\n" +
    "\n" +
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n" +
    "        super().__init__(value, canBeNull, attribName)\n"+
    "\n" +
    "    @property\n" +
    "    def internal_value(self):\n" +
    "       return self._internal_value\n" +
    "\n" +
    "    def copy(self):\n" +
    "        if self._isNull:\n" +
    "            value = None\n" +
    "        else:\n" +
    "            value = []\n"
    "            for v in self.internal_value:\n"
    "                value.append(v.copy())\n"
    "        return self.__class__(value)\n"
        )
        self.write("\n")
        self.write("\n")

    def write_attribute_class(self, d):
        blockattribute = [
    "    value_type = None\n"
        ,
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n"
    "        super().__init__(value, canBeNull, attribName)\n"
    "        if value is None and self._canBeNull:\n"
    "            self._isNull = True\n"
    "        elif type(value) == type(self):\n"
    "            self._internal_value = value.copy().internal_value\n"
    "        elif type(value) == type(self).value_type:\n"
    "            self._internal_value = value\n"
    "        elif type(self) == type(Attribute(None)) and value.shortForm in range(1,19):\n" +
    "            self._internal_value = value.copy().internal_value\n" +
    "            self.shortForm = value.shortForm\n" +
    "            self.value_type = value.value_type\n" +
    "        else:\n"
    "            raise TypeError(\"Expected {}, got {}.\".format(type(self).value_type, type(value)))\n"
        ,
    "    def copy(self):\n"
    "        return self.__class__(self.internal_value, self._canBeNull)\n"
        ]
        self.write_element_class(d, blockattribute)

    def write_objectref_class(self, d):
        blockattribute = [
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n"
    "        Element.__init__(self, value, canBeNull, attribName)\n"
    "        self._internal_value = [None]*4\n"
    "        if value is None and self._canBeNull:\n"
    "            self._isNull = True\n"
    "        elif type(value) == type(self):\n"
    "            if value.internal_value is None:\n"
    "                if self._canBeNull:\n"
    "                    self._isNull = True\n"
    "                else:\n"
    "                    raise ValueError(\"This {} cannot be Null\".format(type(self)))\n"
    "            else:\n"
    "                self._internal_value = value.copy().internal_value\n"
    "        else:\n"
    "            self.domain = value[0]\n"
    "            self.type = value[1]\n"
    "            self.key = value[2]\n"
    "            self.version = value[3]\n"
    ,
    "    @property\n"
    "    def domain(self):\n"
    "        return self._internal_value[0]\n"
    ,
    "    @domain.setter\n"
    "    def domain(self, domain):\n"
    "        self._internal_value[0] = IdentifierList(domain, canBeNull=False, attribName='domain')\n"
    "        self._isNull = False\n"
    ,
    "    @property\n"
    "    def type(self):\n"
    "        return self._internal_value[1]\n"
    ,
    "    @type.setter\n"
    "    def type(self, objecType):\n"
    "        self._internal_value[1] = Long(objecType, canBeNull=False, attribName='type')\n"
    "        self._isNull = False\n"
    ,
    "    @property\n"
    "    def key(self):\n"
    "        return self._internal_value[2]\n"
    ,
    "    @key.setter\n"
    "    def key(self, key):\n"
    "        self._internal_value[2] = Identifier(key, canBeNull=True, attribName='key')  # TODO: change to False when ESA impl is fixed\n"
    "        self._isNull = False\n"
    ,
    "    @property\n"
    "    def version(self):\n"
    "        return self._internal_value[3]\n"
    ,
    "    @version.setter\n"
    "    def version(self, version):\n"
    "        self._internal_value[3] = UInteger(version, canBeNull=False, attribName='version')\n"
    "        self._isNull = False\n"
        ]
        self.write_element_class(d, blockattribute)

    def write_abstract_enum_class(self):
        self.write(
    "class AbstractEnum(Attribute):\n"
    "\n"
    "    value_type = None\n"
    "\n"
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n"
    "        if type(value) == type(''):\n"
    "            for v in list(self.value_type):\n"
    "                 if v.name == value:\n"
    "                     value = v\n"
    "        elif type(value) == type(1):\n"
    "            value = self.value_type(value)\n"
    "        elif type(value) == type(self).value_type:\n"
    "            pass  # Everything is fine\n"
    "        elif type(value) == type(self):\n"
    "            value = value.internal_value\n"
    "        else:\n"
    "            raise TypeError(\"Expected {}, got {}.\".format(type(self).value_type, type(value)))\n"
    "        super().__init__(value, canBeNull, attribName)\n"
    "\n\n"
        )

    def write_abstractcomposite_class(self, d):
        blockcomposite = [
    "    _fieldNumber = 0\n"
        ,
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n"
    "        super().__init__(value, canBeNull, attribName)\n"
    "        self._internal_value = []\n"
        ,
    "    def copy(self):\n"
    "        if self._isNull:\n"
    "            value = None\n"
    "        else:\n"
    "            value = []\n"
    "            for v in self.internal_value:\n"
    "                value.append(v.copy())\n"
    "        return self.__class__(value, self._canBeNull)\n"
        ]

        self.write_element_class(d, blockcomposite)

    def write_composite_class(self, d, blocks=[]):
        parentclass = self._element_parentclass(d)

        # Seems to be a bug in the XML from COM and MC
        if parentclass == 'ABC':
            parentclass = "mal.Composite"
        self.write(
    "class {}({}):\n".format(d.name, parentclass) +
    "    \"\"\"{classdoc}\"\"\"\n".format(classdoc=d.comment)
        )
        self.write("\n")
        if d.shortFormPart:
            self.write(
    "    shortForm = {}.{}\n".format("MALShortForm", d.name.upper())
            )
        else:
            self.write(
    "    shortForm = None\n"
            )
        fieldNumber = "{}._fieldNumber + {}".format(parentclass, len(d.fields))
        self.write(
    "    _fieldNumber = {}\n".format(fieldNumber)
            )

        self.write("\n")
        self.write(
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n" +
    "        super().__init__(value, canBeNull, attribName)\n" +
    "        self._internal_value += [None]*{}\n".format(len(d.fields)) +
    "        if value is None and self._canBeNull:\n" +
    "            self._isNull = True\n" +
    "        elif type(value) == type(self):\n" +
    "            if value.internal_value is None:\n" +
    "                if self._canBeNull:\n" +
    "                    self._isNull = True\n" +
    "                else:\n"
    "                    raise ValueError(\"This {} cannot be Null\".format(type(self)))\n" +
    "            else:\n" +
    "                self._internal_value = value.copy().internal_value\n" +
    "        else:\n"
        )
        if len(d.fields) == 0:
            # In this case it's an abstract composite
            self.write(
    "            raise RuntimeError(\"This class is abstract and should not be directly called\")\n"
        )

        for i, field in enumerate(d.fields):
            index = "{}._fieldNumber + {}".format(parentclass, i)
            self.write(
    "            self.{} = value[{}]\n".format(field.name, index)
            )

        for i, field in enumerate(d.fields):
            index = "{}._fieldNumber + {}".format(parentclass, i)
            fieldtype = self._element_completename(field.maltype)
            fieldtype_known = True

            if field.maltype.isList:
                fieldtype += 'List'

            if fieldtype == 'mal.Attribute' or fieldtype == 'Attribute':
                fieldtype_runtime = "type({})".format(field.name)
                fieldtype_known = False

            self.write("\n")
            self.write(
    "    @property\n" +
    "    def {}(self):\n".format(field.name) +
    "        return self._internal_value[{}]\n".format(index) +
    "\n" +
    "    @{}.setter\n".format(field.name) +
    "    def {0}(self, {0}):\n".format(field.name)
            )
            if fieldtype_known:
                self.write(
    "        self._internal_value[{0}] = {1}({2}, canBeNull={3}, attribName='{2}')\n".format(index, fieldtype, field.name, field.canBeNull)
                )
            else:
                self.write(
    "        if {0} is None:\n".format(field.name) +
    "            self._internal_value[{0}] = {1}({2}, canBeNull={3}, attribName='{2}')\n".format(index, fieldtype, field.name, field.canBeNull) +
    "        else:\n" +
    "            self._internal_value[{0}] = {1}({2}, canBeNull={3}, attribName='{2}')\n".format(index, fieldtype_runtime, field.name, field.canBeNull)
                )
            self.write(
    "        self._isNull = False\n"
            )

        self.write("\n")
        self.write("\n")

    def write_elementlist_class(self, d):
        if self.generator.area.name == "MAL":
            parentclass = "ElementList"
        else:
            parentclass = "mal.ElementList"
        self.write(
    "class {}({}):\n".format(d.name+"List", parentclass)
        )

        if d.shortFormPart:
            self.write(
    "    shortForm = -{}.{}\n".format("MALShortForm", d.name.upper())
            )
        else:
            self.write(
    "    shortForm = None\n"
            )
        self.write(
    "\n" +
    "    def __init__(self, value=None, canBeNull=True, attribName=None):\n" +
    "        super().__init__(value, canBeNull, attribName)\n" +
    "        self._internal_value = []\n" +
    "        if type(value) == type(self):\n" +
    "            if value.internal_value is None:\n" +
    "                if self._canBeNull:\n" +
    "                    self._isNull = True\n" +
    "                else:\n"
    "                    raise ValueError(\"This {} cannot be Null\".format(type(self)))\n" +
    "            else:\n" +
    "                self._internal_value = value.copy().internal_value\n" +
    "        else:\n" +
    "            listvalue = value if type(value) == list else [value]\n" +
    "            for v in listvalue:\n" +
    "                 self._internal_value.append({}(v))\n".format(d.name)
                )

        self.write("\n")
        self.write("\n")

    def write_datatypes(self, data_types):
        self.write_shortforms(data_types)

        # Abstract ElementList is needed for EnumerationLists
        if 'Element' in data_types:
            if 'Element' in data_types['Element']:
                self.write_abstractelement_class(data_types['Element']['Element'])
                self.write_abstractelementlist_class()

        if 'Element' in data_types:
            if 'Attribute' in data_types['Element']:
                self.write_attribute_class(data_types['Element']['Attribute'])
                self.write_elementlist_class(data_types['Element']['Attribute'])
                self.write_abstract_enum_class()
            if 'Composite' in data_types['Element']:
                self.write_abstractcomposite_class(data_types['Element']['Composite'])
                self.write_elementlist_class(data_types['Element']['Composite'])

            for dname, d in data_types['Element'].items():
                if dname in ('Element', 'Attribute', 'Composite', 'ObjectRef'):
                    continue
                self.write_element_class(d)
                self.write_elementlist_class(d)
            if 'ObjectRef' in data_types['Element']:
                self.write_objectref_class(data_types['Element']['ObjectRef'])
                self.write_elementlist_class(data_types['Element']['ObjectRef'])

        if 'Enumeration' in data_types:
            for dname, d in data_types['Enumeration'].items():
                self.write_enumeration_class(d)
                self.write_elementlist_class(d)

        if 'Composite' in data_types:
            for dname, d in data_types['Composite'].items():
                self.write_composite_class(d)
                self.write_elementlist_class(d)

        if 'Element' in data_types and 'ObjectRef' in data_types['Element']:
            self.write(
    "ObjectRef.value_type = ObjectIdentity  # Needed here so that ObjectIdentity is defined\n\n\n"
            )

    def write_serviceprovider_module(self, service):

        self.write(
    "\"\"\"{}\"\"\"\n".format(service.comment) +
    "\n" +
    "{}\n".format("\n".join(IMPORTS[self.generator.area.name])) +
    "from malpy.mo import {}\n".format(self.generator.area.name.lower()) +
    "\n" +
    "number = {}\n".format(service.number)
        )
        for capabilitySet in service.capabilitySets:
            self.write(
    "\n" +
    "# CapabilitySet {}\n".format(capabilitySet.number)
            )
            for operation in capabilitySet.operations:
                for providerConsumer in ['Provider', 'Consumer']:
                    operationname = operation.name + providerConsumer +"Handler"
                    operationclassname = operationname[0].upper() + operationname[1:]
                    parentclassname = "mal." + operation.interactionType + providerConsumer +"Handler"
                    self.write(
    "class {}({}):\n".format(operationclassname, parentclassname) +
    "    AREA = {}\n".format(self.generator.area.number) +
    "    AREA_VERSION = {}\n".format(self.generator.area.version) +
    "    SERVICE = {}\n".format(service.number) +
    "    OPERATION = {}\n".format(operation.number) +
    "\n\n"
                )

                #for message in operation.messages:
                #    print('..', message.fields)

        self.write_datatypes(service.datatypes)

class MALTypeModuleGenerator(object):
    def __init__(self, module, xml_def_filepath, outpath):
        self.module = module
        self.xml_def_filepath = xml_def_filepath
        self.outpath = os.path.join(outpath, module)
        self.datatype_buffer = MALBuffer(self)
        self.service_buffers = {}
        with open(PARAMFILE, 'r') as pf:
            parameters = yaml.load(pf, Loader=yaml.SafeLoader)
        self.typedict = parameters['typedict']
        self.ctrldict = parameters['controldict']

    def save_services(self):
        if not self.service_buffers:
            return
        dirpath = os.path.join(self.outpath,'services')
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        initpath = os.path.join(dirpath, '__init__.py')
        service_string_list = ', '.join(["'{}'".format(s) for s in self.service_buffers.keys()])
        with open(initpath, 'w') as f:
            f.write(
    "__all__ = [{}]\n".format(service_string_list)
            )
        for service in self.service_buffers:
            servicemodulepath = os.path.join(dirpath, service + '.py')
            with open(servicemodulepath, 'w') as f:
                f.write(self.service_buffers[service].content)

    def save_datatypes(self):
        maltypespath = os.path.join(self.outpath, 'maltypes.py')
        initpath = os.path.join(self.outpath, '__init__.py')
        if self.datatype_buffer.content[-2:] == '\n\n':
            self.datatype_buffer.content = self.datatype_buffer.content[:-2]
        if not os.path.isdir(self.outpath):
            os.makedirs(self.outpath)
        with open(initpath, 'w') as f:
            if self.module == 'mal':
                f.write(
    "__all__ = ['maltypes']\n" +
    "from .maltypes import *\n" +
    "from .malinteractions import *\n"
                )
            else:
                f.write(
    "__all__ = ['maltypes', 'services']\n" +
    "from .maltypes import *\n"
                )
        with open(maltypespath, 'w') as f:
            f.write(self.datatype_buffer.content)

    def generate(self):
        """
        Root {
            Area {
                services x N {
                    DataTypes,}
                dataTypes {

                },
                errors {
                    error xN
                }
            }
        }
        """
        root = ET.parse(self.xml_def_filepath).getroot()
        for area_node in list(root):
            self.area = MALAreaXML(area_node)

            services = []
            for area_subnode in list(area_node):
                if area_subnode.tag == maltag('dataTypes'):
                    data_types = _parse_datatypes(area_subnode)
                elif area_subnode.tag == maltag('errors'):
                    error_dict = _parse_errors(area_subnode)
                elif area_subnode.tag == maltag('service'):
                    services.append(_parse_service(area_subnode))
                elif area_subnode.tag == maltag('documentation'):
                    pass
                else:
                    print(area_subnode.tag)

            self.datatype_buffer.write_module_header()
            self.datatype_buffer.write_datatypes(data_types)
            self.datatype_buffer.write_errors(error_dict)

            for service in services:
                servicename = service.name.lower()
                if not servicename in self.service_buffers:
                    self.service_buffers[servicename] = MALBuffer(self, servicename)
                self.service_buffers[servicename].write_serviceprovider_module(service)


if __name__ == "__main__":
    for areaname in AREA_TO_GENERATE:
        definitionfilepath = MO_XML[areaname]
        generator = MALTypeModuleGenerator(areaname.lower(), definitionfilepath, OUTFILE)
        generator.generate()
        generator.save_datatypes()
        generator.save_services()
