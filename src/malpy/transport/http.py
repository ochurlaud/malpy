# SPDX-FileCopyrightText: 2025 Olivier Churlaud <olivier@churlaud.com>
# SPDX-FileCopyrightText: 2025 CNES
#
# SPDX-License-Identifier: MIT

import socket as pythonsocket
import time
import pickle
import http.client
import urllib.parse
import logging
import json

from email.header import Header, decode_header, make_header
from io import BytesIO
from malpy.malpydefinitions import MALPY_ENCODING
from malpy.mo import mal
from struct import *  # pack() unpack()


from .abstract_transport import MALSocket

VERSION_NUMBER = 1  # Version number of the transport

def _encode_uri(uri):
    return '{}:{}'.format(uri[0], uri[1])


def _decode_uri(uri):
    splitted_uri = uri.split(':')
    #host = splitted_uri[1][2:]  # Remove //
    #port = splitted_uri[2]
    host = splitted_uri[0]
    port = splitted_uri[1]
    
    return (host, port)

# Split uri in <schem>://<host>:<port>/<path>
def _split_uri(uri):
    logger = logging.getLogger(__name__)

    host = None
    port = None
    path = None

    splitted_uri = uri.split(':')
    if splitted_uri[0].lower() in ["http", "https", "malhttp"]:
        host = splitted_uri[1][2:]
        rest_uri = uri.split(':',2)[2]
    else:
        host = splitted_uri[0]
        rest_uri = uri.split(':',1)[1]

    splitted_rest_uri = rest_uri.split('/',1)
    port = splitted_rest_uri[0]
    if len(splitted_rest_uri) > 1:
        path = splitted_rest_uri[1]

    logger.debug('urlparsed {} host {} port {} path {}'.format(uri, host, port, path))

    return (host,port,path)


def _encode_time(t):
    s = time.strftime("%Y-%jT%H:%M:%S", time.localtime(t))
    # Time is in seconds.
    # We retrieve the decimal part only
    # 0.xxxxx and from that 1 -> 4 chars => .xxx
    s += ("%.9f" % (t % 1,))[1:5]
    return s


def _decode_time(s):
    return time.mktime(time.strptime(s[:-4], "%Y-%jT%H:%M:%S")) + float(s[-4:])


def _encode_qos_level(qos_level):
    d = {
        mal.QoSLevelEnum.BESTEFFORT: "BESTEFFORT",
        mal.QoSLevelEnum.ASSURED: "ASSURED",
        mal.QoSLevelEnum.QUEUED: "QUEUED",
        mal.QoSLevelEnum.TIMELY: "TIMELY"
    }
    return d[qos_level]


def _decode_qos_level(qos_level):
    d = {
        "BESTEFFORT": mal.QoSLevelEnum.BESTEFFORT,
        "ASSURED": mal.QoSLevelEnum.ASSURED,
        "QUEUED": mal.QoSLevelEnum.QUEUED,
        "TIMELY": mal.QoSLevelEnum.TIMELY
    }
    return d[qos_level]


def _encode_session(session):
    d = {
        mal.SessionTypeEnum.LIVE: "LIVE",
        mal.SessionTypeEnum.SIMULATION: "SIMULATION",
        mal.SessionTypeEnum.REPLAY: "REPLAY"
    }
    return d[session]


def _decode_session(session):
    d = {
        "LIVE": mal.SessionTypeEnum.LIVE,
        "SIMULATION": mal.SessionTypeEnum.SIMULATION,
        "REPLAY": mal.SessionTypeEnum.REPLAY
    }
    return d[session]


def _encode_ip_type(ip_type):
    d = {
        mal.InteractionTypeEnum.SEND: "SEND",
        mal.InteractionTypeEnum.SUBMIT: "SUBMIT",
        mal.InteractionTypeEnum.REQUEST: "REQUEST",
        mal.InteractionTypeEnum.INVOKE: "INVOKE",
        mal.InteractionTypeEnum.PROGRESS: "PROGRESS",
        mal.InteractionTypeEnum.PUBSUB: "PUBSUB"
    }
    return d[ip_type]


def _decode_enum(value, enumeration):
    if type(value) == int:
        return enumeration(value)
    elif type(value) == str:
        for k in enumeration:
            if k.name == value:
                return k
        raise ValueError("{} not found in enumeration {}".format(value, enumeration))
    else:
        raise ValueError("{} not found in enumeration {}".format(value, enumeration))


def _encode_ascii(s):
    return Header(s, "us-ascii").encode()


def _decode_ascii(s):
    return str(make_header(decode_header(s)))


class Status:
    def __init__(self, code, message=""):
        self.code = code
        self.message = message


#TODO: check if http uses \r\n \n or anything x...

class HTTPSocket(MALSocket):
    _messagesize = 1024
    struct_format = '!I'

    def __init__(self, socket=None, CONTEXT=None,  private=False, private_host=None, private_port=None):
        self._private = private
        self.CONTEXT=CONTEXT
        if private and socket is None:
            self.socket = pythonsocket.socket(pythonsocket.AF_INET,
                                              pythonsocket.SOCK_STREAM)
        else:
            self.socket = socket
        self._lastCommandIsSend = False
        self.client = None
        self.private_host=private_host
        self.private_port=private_port

    def bind(self, uri):
        """ @param uri: (host, port) """
        self.socket.bind(uri)

    def listen(self, unacceptedconnectnb=0):
        self.socket.listen(unacceptedconnectnb)

    def waitforconnection(self):
        logger = logging.getLogger(__name__)
        conn, addr = self.socket.accept()
        logger.debug('Header {} body {}'.format(conn, addr))
        return HTTPSocket(conn, private=self._private, CONTEXT=self.CONTEXT)

    def connect(self, uri):
        """ @param uri: (host, port) """
        self._uri=uri
		
    def unbind(self):
        self.socket.close()

    def disconnect(self):
        self.socket.close()

    def send(self, message):
        logger = logging.getLogger(__name__)
        logger.debug("[**] private '{}' LastCommandIsSend {}".format(self._private, self._lastCommandIsSend))

        headers = self._header_mal_to_http(message)

        if self.encoding == MALPY_ENCODING.XML:
            headers['Content-Type'] = "application/mal-xml"
        else:
            headers['Content-Type'] = "application/mal"
            raise NotImplementedError("Only the XML Encoding is implemented with the HTTP Transport.")
        body = message.msg_parts

        logger.info("headers : {}\nbody : {}".format(json.dumps(headers,indent=4),body.decode('utf-8')))

        # For deregister stage, request is not private
        if headers['X-MAL-Interaction-Stage'] ==  str(mal.MAL_IP_STAGES.PUBSUB_DEREGISTER):
           self._private = False

        if self._private is False :
            self._send_http_request(target=message.header.uri_to, body=body, headers=headers)
        else:
            self._send_pickle_response(headers, body)


        if self._private is False and self._lastCommandIsSend is False:
            self._private = True

        if self._private is True and self._lastCommandIsSend is False:
            self._private = False

        self._lastCommandIsSend = True
        logger.debug("[**] private '{}' LastCommandIsSend {}".format(self._private, self._lastCommandIsSend))


    def recv(self):
        logger = logging.getLogger(__name__)

        logger.debug("[**] private '{}' LastCommandIsSend {}".format(self._private, self._lastCommandIsSend))

        if self._private is True:
            headers, body = self._receive_pickle_request()
            logger.info("headers : {}\nbody : {}".format(headers,body.decode('utf-8')))
        else:
            headers, body=self._receive_http_response()
            logger.info("headers : {}\nbody : {}".format(headers,body))
#        logger.info("headers : {}\nbody : {}".format(json.dumps(headers,indent=4),body.decode('utf-8')))

        malheader = self._header_http_to_mal(headers)

        if self.encoding == MALPY_ENCODING.XML and headers['Content-Type'] != "application/mal-xml":
            raise RuntimeError("Unexpected encoding. Expected 'application/mal-xml', got '{}'".format(headers['Content-Type']))

        if self._private is False and \
           self._lastCommandIsSend is True and \
           (headers['X-MAL-Interaction-Stage'] != str(mal.MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER_ACK) and headers['X-MAL-Interaction-Stage'] != str(mal.MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER_ACK)):
            self._private = True

        self._lastCommandIsSend = False
        logger.debug("[**] private '{}' LastCommandIsSend {}".format(self._private, self._lastCommandIsSend))
     

        return mal.MALMessage(header=malheader, msg_parts=body)

    @property
    def uri(self):
        return (self._uri)

    def _header_http_to_mal(self, headers):

        if int(headers['X-MAL-Version-Number']) != VERSION_NUMBER:
            raise RuntimeError("The incoming version number was {}, expected was {}".format(headers['X-MAL-Version-Number'], VERSION_NUMBER))

        malheader = mal.MALHeader()
        malheader.auth_id = b''.fromhex(headers['X-MAL-Authentication-Id'])
        malheader.uri_from = headers['X-MAL-URI-From']
        malheader.uri_to = headers['X-MAL-URI-To']
        malheader.timestamp = _decode_time(headers['X-MAL-Timestamp'])
        malheader.qos_level = _decode_qos_level(headers['X-MAL-QoSlevel'])
        malheader.priority = int(headers['X-MAL-Priority'])
        malheader.domain = _decode_ascii(headers['X-MAL-Domain']).split('.')
        malheader.network_zone = _decode_ascii(headers['X-MAL-Network-Zone'])
        malheader.session = _decode_session(headers['X-MAL-Session'])
        malheader.session_name = _decode_ascii(headers['X-MAL-Session-Name'])
        malheader.ip_type = _decode_enum(headers['X-MAL-Interaction-Type'], mal.InteractionTypeEnum)
        malheader.ip_stage = int(headers['X-MAL-Interaction-Stage'])
        malheader.transaction_id = int(headers['X-MAL-Transaction-Id'])
        malheader.area = int(headers['X-MAL-Service-Area'])
        malheader.service = int(headers['X-MAL-Service'])
        malheader.operation = int(headers['X-MAL-Operation'])
        malheader.area_version = int(headers['X-MAL-Area-Version'])
        malheader.is_error_message = (headers["X-MAL-Is-Error-Message"] == "True")

        return malheader

    def _header_mal_to_http(self, message):

        headers = {
            "Content-Length": len(message),
            "X-MAL-Authentication-Id": message.header.auth_id.hex(),
            "X-MAL-URI-From": message.header.uri_from,
            "X-MAL-URI-To": message.header.uri_to,
            "X-MAL-Timestamp": _encode_time(message.header.timestamp),
            "X-MAL-QoSlevel": message.header.qos_level.name,
            "X-MAL-Priority": str(message.header.priority),
            "X-MAL-Domain": ".".join([ _encode_ascii(x) for x in message.header.domain ]),
            "X-MAL-Network-Zone": _encode_ascii(message.header.network_zone),
            "X-MAL-Session": message.header.session.name,
            "X-MAL-Session-Name": _encode_ascii(message.header.session_name),
            "X-MAL-Interaction-Type": message.header.ip_type.name,
            "X-MAL-Interaction-Stage": str(message.header.ip_stage),
            "X-MAL-Transaction-Id": str(message.header.transaction_id),
            "X-MAL-Service-Area": str(message.header.area),
            "X-MAL-Service": str(message.header.service),
            "X-MAL-Operation": str(message.header.operation),
            "X-MAL-Area-Version": str(message.header.area_version),
            "X-MAL-Is-Error-Message": "True" if message.header.is_error_message else "False",
            "X-MAL-Version-Number": str(VERSION_NUMBER)
        }

        return headers


    def _send_http_request(self, target, headers, body):
        logger = logging.getLogger(__name__)

	#modif httpsconnection request method header body en sendpostrequest
        #logger.debug('Target [{}] Header {} body {}'.format(target, headers, body.decode('utf-8')))

        host,port,path = _split_uri(target)
        # If client doesn't exist
        if not self.client:
             logger.debug('Create Client')
             self.client = http.client.HTTPSConnection(_encode_uri((host,port)), context=self.CONTEXT)
             self.client.set_debuglevel(0)
        
        #try:
        logger.debug('Send POST \nrequest url : {} \nheaders : {} \nbody : {}'.format(target, json.dumps(headers,indent=4), body.decode('utf-8)')))
        self.client.request('POST', url=target, body=body, headers=headers)
        #except Exception as e:
        #    logger.warning("Exception {} URL {}".format(e, target))

        # Dans certains cas, il faut faire un getreponse()
        if ( headers['X-MAL-Interaction-Type'] == _encode_ip_type(mal.InteractionTypeEnum.SEND) ) or \
           ( headers['X-MAL-Interaction-Type'] == _encode_ip_type(mal.InteractionTypeEnum.INVOKE) and \
               headers['X-MAL-Interaction-Stage'] == str(mal.MAL_IP_STAGES.INVOKE_RESPONSE))  or  \
           ( headers['X-MAL-Interaction-Type'] == _encode_ip_type(mal.InteractionTypeEnum.PROGRESS) and \
               ( (headers['X-MAL-Interaction-Stage'] == str(mal.MAL_IP_STAGES.PROGRESS_RESPONSE) ) or (headers['X-MAL-Interaction-Stage'] == str(mal.MAL_IP_STAGES.PROGRESS_UPDATE)))) or \
           ( headers['X-MAL-Interaction-Type'] == _encode_ip_type(mal.InteractionTypeEnum.PUBSUB) and \
               headers['X-MAL-Interaction-Stage'] == str(mal.MAL_IP_STAGES.PUBSUB_PUBLISH)  ):
            logger.debug('Interaction Type {} Stage {} -> getresponse()'.format(headers['X-MAL-Interaction-Type'], headers['X-MAL-Interaction-Stage']))
            response=self.client.getresponse()


    def _receive_http_response(self):
        response=self.client.getresponse()
        headers=response.headers
        body=response.read().decode('utf-8')
        if response.status != 200:
            raise RuntimeError("Got en error: {} - {}\n{}".format(response.status, response.reason, body))
        return headers, body

    def _receive_pickle_request(self):
        logger = logging.getLogger(__name__)

        if self.socket is None:
            server_socket = pythonsocket.socket(pythonsocket.AF_INET,
                                              pythonsocket.SOCK_STREAM)    
            server_socket.bind((self.private_host, self.private_port))
            server_socket.listen(10)
            logger.info("[*] Server listening on {} {}".format(self.private_host, self.private_port))
            conn, addr = server_socket.accept()
            logger.debug('socket accept  {} {}'.format(conn, addr))
            self.socket = conn

 
        # Read first message lenght
        logger.debug("[**] Recv() ask  {} bytes".format(calcsize(self.struct_format)))
        size_packed = self.socket.recv(calcsize(self.struct_format))

        # Perhaps pipe broken
        if size_packed == b'':
            # Close socket
            self.socket.close()

            # Rebuild a new server_socket
            logger.warning("Perhaps pipe broken. Create new server socket")
            server_socket = pythonsocket.socket(pythonsocket.AF_INET,
                                              pythonsocket.SOCK_STREAM)    
            server_socket.bind((self.private_host, self.private_port))
            server_socket.listen(10)
            logger.info("[*] Server listening on {} {}".format(self.private_host, self.private_port))
            conn, addr = server_socket.accept()
            logger.info('socket accept  {} {}'.format(conn, addr))
            self.socket = conn

            logger.info("[**] Recv() ask  {} bytes".format(calcsize(self.struct_format)))
            size_packed = self.socket.recv(calcsize(self.struct_format))




        logger.info("[**] Received {} bytes".format(size_packed))
        size = unpack(self.struct_format,size_packed)[0]
        logger.debug("[**] Received {} bytes '{}'".format(size,size_packed))

        message = self.socket.recv(int(size))
        logger.debug("[**] Received {} bytes '{}'".format(len(message),message))

        # Get message from http server
        data = pickle.loads(message)
        #logger.debug("[**] data '{}'".format(data))
        logger.debug("[**] Headers {} Body '{}'".format(data['headers'], data['body'].decode('utf-8')))

        headers = data['headers']
        body = data['body']

        return headers, body

    def _send_pickle_response(self, headers, body):
        logger = logging.getLogger(__name__)

        logger.debug('Header {} body {}'.format(headers, body))
        response_dict= {
            'headers': headers,
            'body': body
        }

        try:
            data_response=pickle.dumps(response_dict)
            data_response_lenght = len(data_response)
            data_response_lenght_packed = pack(self.struct_format,data_response_lenght)

            # Send data lenght
            logger.debug("Send {} bytes '{}'".format(len(data_response_lenght_packed),data_response_lenght_packed))
            self.socket.send(data_response_lenght_packed)

            # Send data
            logger.debug("Send {} bytes '{}'".format(data_response_lenght,data_response))
            self.socket.send(data_response)
        except Exception as e:
            logger.warning("Exception {} ".format(e))



class HTTPSocketPubSub(HTTPSocket):

    def __init__(self, socket=None, CONTEXT=None,  private=False, private_host=None, private_port=None):
        super().__init__(socket, CONTEXT,   private, private_host, private_port)

    def recv(self):
        logger = logging.getLogger(__name__)

        # Read HTTP body an headers
        body = self.socket.body
        headers = self.socket.headers
        logger.info("headers [{}] , body [{}]".format(headers,body.decode('utf-8')))
 
        # Set MAL header from HTTP header
        malheader = self._header_http_to_mal(headers)

        if self.encoding == MALPY_ENCODING.XML and headers['Content-Type'] != "application/mal-xml":
            raise RuntimeError("Unexpected encoding. Expected 'application/mal-xml', got '{}'".format(headers['Content-Type']))

        # Rajouter un send_http_response() dans le cas de la reception d'un PUBSUB_PUBLISH
        if ( headers['X-MAL-Interaction-Type'] == _encode_ip_type(mal.InteractionTypeEnum.PUBSUB) and \
             headers['X-MAL-Interaction-Stage'] == str(mal.MAL_IP_STAGES.PUBSUB_PUBLISH)  ):
            logger.debug('Interaction Type {} Stage {} -> getresponse()'.format(headers['X-MAL-Interaction-Type'], headers['X-MAL-Interaction-Stage']))
            self.send_http_response(b'')

        # Return a MAL message
        return mal.MALMessage(header=malheader, msg_parts=body)
        

    def send(self, message):
        logger = logging.getLogger(__name__)

        # Set HTTP headers from MAL message
        headers = self._header_mal_to_http(message)
        body = message.msg_parts
        logger.info("headers : {}\nbody : {}".format(json.dumps(headers,indent=4),body.decode('utf-8')))

        if self.encoding == MALPY_ENCODING.XML:
            headers['Content-Type'] = "application/mal-xml"
        else:
            headers['Content-Type'] = "application/mal"
            raise NotImplementedError("Only the XML Encoding is implemented with the HTTP Transport.")

        # For stage NOTIFY, the request is a HTTP POST request
        if headers['X-MAL-Interaction-Stage'] == str(mal.MAL_IP_STAGES.PUBSUB_NOTIFY) :
            self._send_http_request(target=message.header.uri_to, body=body, headers=headers)
        else:

            logger.info("send http response")
# For other cases it's a 200 http response
            self.socket.send_response(200, 'OK')

            # Write headers in HTTP response
            for key, value in headers.items():
                self.socket.send_header(key,value)
            self.socket.end_headers()

            # send response
            self.socket.wfile.write(body)

    def send_http_response(self, message):
        # Send HTTP response 200
        logger = logging.getLogger(__name__)

        self.socket.send_response(200, 'OK')
        logger.debug("message {}".format(message))
        self.socket.end_headers()
        self.socket.wfile.write(message)

 


