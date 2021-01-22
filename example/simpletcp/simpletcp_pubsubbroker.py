#! /bin/python

import sys
sys.path.append('../../src')

import threading

from mo import mal
import transport.tcp
import encoding


"""
Pubsubprovider :
    1) démarre
    2) trouve le broker
    3) Publish_register : Définit la subscription
    4) publie .. pubie
    5) publish_deregister

PubSubBrokerHandler:
    1) Démarre
    2) attend réception d'un subscriber / publisher (2 cotés :  threads)'
    2a) réception subscription publisher:
        2a1) stocke dans une table le lien subscription / ProviderHandler et ouvre une socket vers ce nouveau provider
        2a2) attend un publish de ce provider
    2b) réception subscription consumer
        2a1à Stocke dans une table le lien


provider: 8001
consumers 9001, 9002


"""
def servicethread(socket, broker_backend):
    enc = encoding.PickleEncoder()
    broker = mal.PubSubBrokerHandler(socket, enc)
    message = broker.receive_any_registration_message()
    if message.ip_stage == mal.MAL_IP_STAGES.PUBSUB_REGISTER:
        broker_backend.register_consumer(message.msg_parts, broker)
    elif message.ip_stage == mal.MAL_IP_STAGES.PUBSUB_DEREGISTER:
        broker_backend.deregister_consumer(message.msg_parts, broker)
    elif message.ip_stage == mal.MAL_IP_STAGES.PUBSUB_PUBLISH_REGISTER:
        broker_backend.register_provider(message.msg_parts, broker)
    elif message.ip_stage == mal.MAL_IP_STAGES.PUBSUB_PUBLISH_DEREGISTER:
        broker_backend.deregister_provider(message.msg_parts, broker)

    print("[**] Received '{}'".format(message.msg_parts.decode('utf8')))
    request.response("I got it!".encode('utf8'))
    print("[**] Closing connection with %s %d." % (socket.uri[0], socket.uri[1]))
    socket.disconnect()

class ThreadSafeBrokerBackend():
    def __init__(self):
        provider_table = {}
        consumer_table = {}
        mutex = threading.Lock()

    def register_consumer(self, subscribtion, broker):
        self.mutex.acquire()
        try:
            self.consumer_table[subscription_id] = entityKey
        finally:
            self.mutex.release()

    def deregister_consumer(self, subscription_ids, broker):
        self.mutex.acquire()
        try:
            for subscription_id in subscription_ids:
                del self.consumer_table[subscription_id]
        finally:
            self.mutex.release()

    def register_provider(self, entitykeys, broker):

        self.mutex.acquire()
        try:
            for entitykey in entitykeys:
                self.provider_table[entitykey]
        finally:
            self.mutex.release()

        while True:
            message = broker.receive_publish()
            update_headers, update_value = decode_message(message)
            self.mutex.acquire()
            rechercher dans tous les consumers:
                si consumer concerné:
                    broker_du_consumer.notify(identifier, update, updatevalues)
            self.mutex.release()
def main():
    try:

        host = '127.0.0.1'
        port = 8009
        s = transport.tcp.TCPSocket()
        s.bind((host, port))
        s.listen(10)
        print("[*] Server listening on %s %d" % (host, (port)))

        while True:
            newsocket = s.waitforconnection()
            print("[**] Incoming connection from %s %d" % (newsocket.uri[0], newsocket.uri[1]))
            threading.Thread(
                target=pubsubthread,
                args=(newsocket, broker_backend)
                ).start()
        s.unbind()

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
