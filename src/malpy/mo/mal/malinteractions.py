# SPDX-FileCopyrightText: 2025 Olivier Churlaud <olivier@churlaud.com>
# SPDX-FileCopyrightText: 2025 CNES
#
# SPDX-License-Identifier: MIT

import time
from enum import IntEnum
from .maltypes import QoSLevelEnum, SessionTypeEnum, InteractionTypeEnum, number

class MAL_IP_STAGES:
    # Send
    SEND = 1

    # Submit
    SUBMIT = 1
    SUBMIT_ACK = 2

    # Request
    REQUEST = 1
    REQUEST_RESPONSE = 2

    # Invoke
    INVOKE = 1
    INVOKE_ACK = 2
    INVOKE_RESPONSE = 3

    # Progress
    PROGRESS = 1
    PROGRESS_ACK = 2
    PROGRESS_UPDATE = 3
    PROGRESS_RESPONSE = 4

    # PubSub
    PUBSUB_REGISTER = 1
    PUBSUB_REGISTER_ACK = 2
    PUBSUB_PUBLISH_REGISTER = 3
    PUBSUB_PUBLISH_REGISTER_ACK = 4
    PUBSUB_PUBLISH = 5
    PUBSUB_NOTIFY = 6
    PUBSUB_DEREGISTER = 7
    PUBSUB_DEREGISTER_ACK = 8
    PUBSUB_PUBLISH_DEREGISTER = 9
    PUBSUB_PUBLISH_DEREGISTER_ACK = 10


class MAL_IP_ERRORS:
    SUBMIT_ERROR = 2
    REQUEST_ERROR = 2
    INVOKE_ACK_ERROR = 2
    INVOKE_RESPONSE_ERROR = 3
    PROGRESS_ACK_ERROR = 2
    PROGRESS_UPDATE_ERROR = 3
    PROGRESS_RESPONSE_ERROR = 5
    PUBSUB_REGISTER_ACK_ERROR = 2
    PUBSUB_PUBLISH_REGISTER_ERROR = 4
#    PUBSUB_PUBLISH_ERROR = 
#    PUBSUB_NOTIFY_ERROR = 17


class MalformedMessageError(Exception):
    pass


class InvalidIPStageError(Exception):
    """ Error in case of invalid IP. 
        Should be called as InvalidIPStageError((message.header.ip_type, message.header.ip_stage)) or
          InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(InteractionTypeEnum.SEND, 1),
                              ip=(message.header.ip_type, message.header.ip_stage), message='You must have messed up something)
    """
    def __init__(self, ip, classname=None, expected_ip=None, message=None):
      errormessage = []
      if classname is not None:
          errormessage.append("In {}.".format(classname))
      if expected_ip is not None:
          expected_iptype = expected_ip[0].name
          expected_ipstage = expected_ip[1]
          errormessage.append("Expected {}:{}.".format(expected_iptype, expected_ipstage))

      iptype = ip[0].name
      ipstage = ip[1]
      errormessage.append("Got {}:{}.".format(iptype, ipstage))

      if message is not None:
          errormessage.append(message)
      super().__init__(" ".join(errormessage))


class BackendShutdown(Exception):
    pass


class MALHeader(object):
    """
    A MALHeader objects in the python representation of the
    MAL message header
    """

    # TODO: This object is a great candidate for a Cython cpdef struct
    # which will allow fast copies and attribute affectations.

    __slots__ = ['area_version', 'ip_type', 'ip_stage',
                 'area', 'service', 'operation',
                 'is_error_message', 'qos_level', 'session',
                 'transaction_id', 'priority', 'uri_from',
                 'uri_to', 'timestamp', 'network_zone',
                 'session_name', 'domain', 'auth_id']

    def __init__(self):
        self.area_version = None
        self.ip_type = None
        self.ip_stage = None
        self.area = None
        self.service = None
        self.operation = None
        self.is_error_message = None
        self.qos_level = None
        self.session = None
        self.transaction_id = None
        self.priority = None
        self.uri_from = None
        self.uri_to = None
        self.timestamp = None
        self.network_zone = None
        self.session_name = None
        self.domain = None
        self.auth_id = None

    def copy(self):
        instance = self.__class__()
        instance.area_version = self.area_version
        instance.ip_type = self.ip_type
        instance.ip_stage = self.ip_stage
        instance.area = self.area
        instance.service = self.service
        instance.operation = self.operation
        instance.is_error_message = self.is_error_message
        instance.qos_level = self.qos_level
        instance.session = self.session
        instance.transaction_id = self.transaction_id
        instance.priority = self.priority
        instance.uri_from = self.uri_from
        instance.uri_to = self.uri_to
        instance.timestamp = self.timestamp
        instance.network_zone = self.network_zone
        instance.session_name = self.session_name
        instance.domain = self.domain
        instance.auth_id = self.auth_id
        return instance


class MALMessage(object):
    """
    A simple structure to hold a decoded MAL header
    and a set of encoded message parts.
    """

    def __init__(self, header=None, msg_parts=[]):
        self.header = header or MALHeader()
        self.msg_parts = msg_parts

    def __len__(self):
        def _sublen(k):
            if type(k) is list:
                return sum([_sublen(x) for x in k])
            else:
                return len(k)

        return _sublen(self.msg_parts)


class Handler(object):
    AREA = None
    AREA_VERSION = 1
    SERVICE = None
    OPERATION = None

    def __init__(self, transport, encoding):
        self.transport = transport
        self.encoding = encoding
        self.transport.parent = self
        self.encoding.parent = self

    def send_message(self, message):
        message = self.encoding.encode(message)
        return self.transport.send(message)

    def receive_message(self):
        message = self.transport.recv()
        return self.encoding.decode(message)


class ConsumerHandler(Handler):
    """
    A consumer handler is a logical structure composed of a set of
    MAL message processing functions for the consumer side of a MAL
    operation. This set of functions depends on the interaction pattern
    of the operation (send, submit, progress etc.).
    The lifespan of the consumer handler is the lifespan of the
    transaction (from the initiation of the operation from the consumer,
    to the final response of the provider)
    """

    IP_TYPE = None
    _transaction_id_counter = 0

    @classmethod
    def get_new_transaction_id(cls):
        cls._transaction_id_counter += 1
        return cls._transaction_id_counter

    def __init__(self, transport, encoding, provider_uri="", consumer_uri="", 
                 session=SessionTypeEnum.LIVE, session_name="", domain=[], network_zone=None,
                 priority=0, auth_id=b"", qos_level=QoSLevelEnum.BESTEFFORT):
        super().__init__(transport, encoding)
        self.consumer_uri = consumer_uri
        self.provider_uri = provider_uri
        self.session = session
        self.session_name = session_name
        self.domain = domain
        self.network_zone = network_zone
        self.priority = priority
        self.auth_id = auth_id
        self.qos_level = qos_level
        self.interaction_terminated = False
        self.transaction_id = self.get_new_transaction_id()

    def create_message_header(self, ip_stage):
        header = MALHeader()
        header.ip_type = self.IP_TYPE
        header.ip_stage = ip_stage
        header.area = self.AREA
        header.service = self.SERVICE
        header.operation = self.OPERATION
        header.area_version = self.AREA_VERSION
        header.is_error_message = None
        header.qos_level = self.qos_level
        header.session = self.session
        header.transaction_id = self.transaction_id
        header.priority = self.priority
        header.uri_from = self.consumer_uri
        header.uri_to = self.provider_uri
        header.timestamp = time.time()
        header.network_zone = self.network_zone
        header.session_name = self.session_name
        header.domain = self.domain
        header.auth_id = self.auth_id
        return header

    def connect(self, uri):
        self.transport.connect(uri)


class ProviderHandler(Handler):
    """
    A provider handler is a logical structure composed of a set of
    MAL message processing functions for the provider side of a MAL
    operation. This set of functions depends on the interaction pattern
    of the operation (send, submit, progress etc.).
    The lifespan of the provider handler is the lifespan of the
    transaction (from the initiation of the operation from the consumer,
    to the final response of the provider)
    """

    AREA = None
    AREA_VERSION = 1
    SERVICE = None
    OPERATION = None

    IP_TYPE = None
    _transaction_id_counter = 0

    @classmethod
    def get_new_transaction_id(cls):
        cls._transaction_id_counter += 1
        return cls._transaction_id_counter

    def __init__(self, transport, encoding,  broker_uri=None, provider_uri="", 
                 session=SessionTypeEnum.LIVE, session_name="", domain=[], network_zone=None,
                 priority=0, auth_id=b"", qos_level=QoSLevelEnum.BESTEFFORT):
        super().__init__(transport, encoding)
        self.broker_uri = broker_uri
        self.provider_uri = provider_uri
        self.response_header = None
        self.session = session
        self.session_name = session_name
        self.domain = domain
        self.network_zone = network_zone
        self.priority = priority
        self.auth_id = auth_id
        self.qos_level = qos_level
        self.interaction_terminated = False
        self.transaction_id = self.get_new_transaction_id()

    def define_header(self, received_message_header):
        self.response_header = received_message_header.copy()
        uri_from = self.response_header.uri_to
        self.response_header.uri_to = self.response_header.uri_from
        self.response_header.uri_from = uri_from

    def create_message_header(self, ip_stage, is_error_message=False, uri_to=None):
        if not self.response_header:
            header = MALHeader()
            header.ip_type = self.IP_TYPE
            header.ip_stage = ip_stage
            header.area = self.AREA
            header.service = self.SERVICE
            header.operation = self.OPERATION
            header.area_version = self.AREA_VERSION
            header.is_error_message = None
            header.qos_level = QoSLevelEnum.BESTEFFORT
            header.session = SessionTypeEnum.LIVE
            header.transaction_id = 0
            header.priority = 0
            header.uri_from = self.provider_uri
            header.timestamp = time.time()
            header.network_zone = None
            header.session_name = ""
            header.domain = self.domain
            header.auth_id = b""
        else:
           header = self.response_header.copy()
        header.ip_stage = ip_stage
        header.is_error_message = is_error_message

        # If parameter uri_to is defined
        if uri_to :
            header.uri_to = uri_to
        elif self.broker_uri:
            # if  parameter uri_to is defined and broker_uri is defined
            header.uri_to = self.broker_uri
        # else:
        #     # Nothing is defined, keep uri_to value
 
        return header


class SendProviderHandler(ProviderHandler):
    """
    A provider handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.SEND

    def receive_send(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.SEND:
            self.interaction_terminated = True
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.SEND), ip=(ip_type, ip_stage))


class SendConsumerHandler(ConsumerHandler):
    """
    A consumer handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.SEND

    def send(self, body):
        header = self.create_message_header(MAL_IP_STAGES.SEND)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)
        self.interaction_terminated = True


class SubmitProviderHandler(ProviderHandler):
    """
    A provider handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.SUBMIT

    def receive_submit(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.SUBMIT:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.SUBMIT), ip=(ip_type, ip_stage))

    def ack(self, body, async_send=False):
        header = self.create_message_header(MAL_IP_STAGES.SUBMIT_ACK)
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)

    def error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.SUBMIT_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)


class SubmitConsumerHandler(ConsumerHandler):
    """
    A consumer handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.SUBMIT

    def submit(self, body):
        header = self.create_message_header(MAL_IP_STAGES.SUBMIT)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.SUBMIT_ACK:
            self.interaction_terminated = True
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.SUBMIT_ERROR:
            self.interaction_terminated = True
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.SUBMIT_ACK), ip=(ip_type, ip_stage))


class RequestProviderHandler(ProviderHandler):
    """
    A provider handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.REQUEST

    def receive_request(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.REQUEST:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.REQUEST), ip=(ip_type, ip_stage))

    def response(self, body, async_send=False):
        header = self.create_message_header(MAL_IP_STAGES.REQUEST_RESPONSE)
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)

    def error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.REQUEST_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)


class RequestConsumerHandler(ConsumerHandler):
    """
    A consumer handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.REQUEST

    def request(self, body):
        header = self.create_message_header(MAL_IP_STAGES.REQUEST)
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def receive_response(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.REQUEST_RESPONSE:
            self.interaction_terminated = True
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.REQUEST_ERROR:
            self.interaction_terminated = True
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.REQUEST_RESPONSE), ip=(ip_type, ip_stage))


class InvokeProviderHandler(ProviderHandler):
    """
    A provider handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.INVOKE

    def receive_invoke(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.INVOKE:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.INVOKE), ip=(ip_type, ip_stage))

    def ack(self, body, async_send=False):
        header = self.create_message_header(MAL_IP_STAGES.INVOKE_ACK)
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def ack_error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.INVOKE_ACK_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def response(self, body, async_send=False):
        header = self.create_message_header(MAL_IP_STAGES.INVOKE_RESPONSE)
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)

    def response_error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.INNVOKE_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)


class InvokeConsumerHandler(ConsumerHandler):
    """
    A consumer handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.INVOKE

    def invoke(self, body):
        header = self.create_message_header(MAL_IP_STAGES.INVOKE)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)
        self.interaction_terminated = True

    def receive_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.INVOKE_ACK:
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.INVOKE_ACK_ERROR:
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.INVOKE_ACK), ip=(ip_type, ip_stage))

    def receive_response(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.INVOKE_RESPONSE:
            self.interaction_terminated = True
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.INVOKE_RESPONSE_ERROR:
            self.interaction_terminated = True
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.INVOKE_RESPONSE), ip=(ip_type, ip_stage))


class ProgressProviderHandler(ProviderHandler):
    """
    A provider handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.PROGRESS

    def receive_progress(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PROGRESS:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PROGRESS), ip=(ip_type, ip_stage))

    def ack(self, body, async_send=False):
        header = self.create_message_header(MAL_IP_STAGES.PROGRESS_ACK)
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def ack_error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.PROGRESS_ACK_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def update(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PROGRESS_UPDATE)
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def update_error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.PROGRESS_UPDATE_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        return self.send_message(message)

    def response(self, body, async_send=False):
        header = self.create_message_header(MAL_IP_STAGES.PROGRESS_RESPONSE)
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)

    def response_error(self, body):
        header = self.create_message_header(MAL_IP_ERRORS.PROGRESS_RESPONSE_ERROR)
        header.is_error_message = True
        message = MALMessage(header=header, msg_parts=body)
        self.interaction_terminated = True
        return self.send_message(message)


class ProgressConsumerHandler(ConsumerHandler):
    """
    A consumer handler for operations belonging to the SEND
    interaction pattern
    """

    IP_TYPE = InteractionTypeEnum.PROGRESS

    def progress(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PROGRESS)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PROGRESS_ACK:
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PROGRESS_ACK_ERROR:
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PROGRESS_ACK), ip=(ip_type, ip_stage))

    def receive_update(self):
        """ As it is not possible to know beforehand if the received message is
        an update or the final response, we only do receive_update. The content of
        the header message will let us know te corresponding state.
        """
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PROGRESS_UPDATE:
            return message
        elif not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PROGRESS_RESPONSE:
            self.interaction_terminated = True
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PROGRESS_UPDATE_ERROR:
            self.interaction_terminated = True
            raise RuntimeError(message)
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PROGRESS_RESPONSE_ERROR:
            self.interaction_terminated = True
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PROGRESS_UPDATE), ip=(ip_type, ip_stage))

#    def receive_response(self):
#        message = self.receive_message()
#        ip_type = message.header.ip_type
#        if ip_stage == MAL_IP_STAGES.PROGRESS_RESPONSE:
#            self.interaction_terminated = True
#            return message
#        elif ip_stage == MAL_IP_STAGES.PROGRESS_RESPONSE_ERROR:
#            self.interaction_terminated = True
#            raise RuntimeError(message)
#        else:
#            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.SEND), ip=(ip_type, ip_stage))


class PubSubProviderHandler(ProviderHandler):

    IP_TYPE = InteractionTypeEnum.PUBSUB

    def publish_register(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_publish_register_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER_ACK:
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PUBSUB_PUBLISH_REGISTER_ERROR:
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER_ACK), ip=(ip_type, ip_stage))

    def publish_deregister(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_publish_deregister_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER_ACK:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER_ACK), ip=(ip_type, ip_stage))

    def publish(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    # def receive_publish_error(self):
    #     message = self.receive_message()
    #     ip_type = message.header.ip_type
    #     is_error_message = message.header.is_error_message
    #     if is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PUBSUB_PUBLISH_ERROR:
    #         return message
    #     else:
    #         raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.SEND), ip=(ip_type, ip_stage))


class PubSubBrokerHandler(ProviderHandler):

    IP_TYPE = InteractionTypeEnum.PUBSUB

    def receive_registration_message(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_REGISTER:
            return message
        elif not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_DEREGISTER:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_REGISTER), ip=(ip_type, ip_stage))

    def register_ack(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_REGISTER_ACK)
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def register_error(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_REGISTER_ACK_ERROR)
        header.is_error_message = True
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def deregister_ack(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_DEREGISTER_ACK)
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def deregister_error(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_DEREGISTER_ACK_ERROR)
        header.is_error_message = True
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_deregister(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_DEREGISTER:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_DEREGISTER), ip=(ip_type, ip_stage))

    def notify(self, body, uri_to):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_NOTIFY, uri_to=uri_to)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    # def notify_error(self, body):
    #     header = self.create_message_header(MAL_IP_STAGES.PUBSUB_NOTIFY_ERROR)
    #     self.define_header(header)
    #     message = MALMessage(header=header, msg_parts=body)
    #     self.send_message(message)

    def receive_publish_registration_message(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER:
            return message
        elif not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER), ip=(ip_type, ip_stage))

    def publish_register_ack(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER_ACK)
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def publish_register_error(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER_ERROR)
        header.is_error_message = True
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_publish_deregister(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER), ip=(ip_type, ip_stage))

    def publish_deregister_ack(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER_ACK)
        self.define_header(header)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_publish(self):
        message = self.receive_message()
        self.define_header(message.header)
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_PUBLISH:
            return message
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_PUBLISH), ip=(ip_type, ip_stage))

    # def publish_error(self, body):
    #     header = self.create_message_header(MAL_IP_STAGES.PUBSUB_PUBLISH_ERROR)
    #     self.define_header(header)
    #     message = MALMessage(header=header, msg_parts=body)
    #     self.send_message(message)


class PubSubConsumerHandler(ConsumerHandler):

    IP_TYPE = InteractionTypeEnum.PUBSUB

    def register(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_REGISTER)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_register_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_REGISTER_ACK:
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PUBSUB_REGISTER_ACK_ERROR:
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_REGISTER_ACK), ip=(ip_type, ip_stage))

    def deregister(self, body):
        header = self.create_message_header(MAL_IP_STAGES.PUBSUB_DEREGISTER)
        message = MALMessage(header=header, msg_parts=body)
        self.send_message(message)

    def receive_deregister_ack(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_DEREGISTER_ACK:
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_STAGES.PUBSUB_DEREGISTER_ACK_ERROR:
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_DEREGISTER_ACK), ip=(ip_type, ip_stage))

    def receive_notify(self):
        message = self.receive_message()
        ip_type = message.header.ip_type
        ip_stage = message.header.ip_stage
        is_error_message = message.header.is_error_message
        if not is_error_message and  ip_stage == MAL_IP_STAGES.PUBSUB_NOTIFY:
            return message
        elif is_error_message and ip_type == self.IP_TYPE and ip_stage == MAL_IP_ERRORS.PUBSUB_NOTIFY_ERROR:
            raise RuntimeError(message)
        else:
            raise InvalidIPStageError(classname=self.__class__.__name__, expected_ip=(self.IP_TYPE, MAL_IP_STAGES.PUBSUB_NOTIFY), ip=(ip_type, ip_stage))

