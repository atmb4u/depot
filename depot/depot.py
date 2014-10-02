#!/usr/bin/python

import argparse
from random import randrange
import uuid
from multiprocessing.managers import SyncManager
from daemon import Daemon

__VERSION__ = "1.0.7"

import socket
import os
from cPickle import dumps, loads


def depot_server(dict_size=4096):
    data_store = {}
    lock_list = []
    secret_dict = {}
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove("/tmp/depotsocket")
    except OSError:
        pass
    print "Starting ..  ."
    s.bind("/tmp/depotsocket")
    while 1:
        s.listen(1)
        conn, addr = s.accept()
        data = conn.recv(dict_size)
        if data:
            packet = loads(data)
            operation = packet.get('operation')
            key = packet.get('key')
            secret = packet.get('secret')
            print data_store
            if operation == "UPDATE":
                if key not in lock_list:
                    data_store.update(packet.get('data'))
                    conn.send('I01\n.')
                else:
                    if secret_dict.get(key) == secret:
                        data_store.update(packet.get('data'))
                        conn.send('I01\n.')
                    else:
                        conn.send('I00\n.')
            elif operation == "SET":
                if key not in lock_list:
                    data_store[packet.get('key')] = packet.get('value')
                    conn.send('I01\n.')
                else:
                    if secret_dict.get(key) == secret:
                        data_store[packet.get('key')] = packet.get('value')
                        conn.send('I01\n.')
                    else:
                        conn.send('I00\n.')
            elif operation == "GET":
                conn.send(dumps(data_store.get(packet.get('key'))))
            elif operation == "GETLOCK":
                lock_list.append(packet.get("key"))
                rand = randrange(0, 10)
                secret = uuid.uuid4().get_hex()[rand: rand + 3]
                secret_dict[key] = secret
                conn.send(dumps(secret))
            elif operation == "FREELOCK":
                if secret_dict[key] == packet.get("secret"):
                    lock_list.remove(packet.get("key"))
                    # secret_dict.pop(key)
                    conn.send('I01\n.')
                else:
                    conn.send('I00\n.')
            elif operation == "DELETE" and key not in lock_list:
                data_store.__delitem__(packet.get('key'))
                conn.send('I01\n.')
            elif operation == "GETLOCKID":
                conn.send(dumps(secret_dict[key]))
        conn.close()


class DepotClient(object):
    def __init__(self, socket_path="/tmp/depotsocket", dict_size=4096):
        self.dict_size = dict_size
        self.initialize(socket_path)

    def initialize(self, socket_path="/tmp/depotsocket"):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(socket_path)

    def update(self, data):
        self.initialize()
        if type(data) == dict:
            self.sock.send(dumps({
                'operation': 'UPDATE',
                'data': data,
            }
            )
            )
            data = loads(self.sock.recv(self.dict_size))
            return data
        else:
            print "Requires dict type object to push."

    def delete(self, key):
        self.initialize()
        self.sock.send(dumps({
            'operation': 'DELETE',
            'key': key,
        }
        )
        )
        data = loads(self.sock.recv(self.dict_size))
        return data

    def getlockid(self, key):
        self.initialize()
        self.sock.send(dumps({
            'operation': 'GETLOCKID',
            'key': key,
        }
        )
        )
        data = loads(self.sock.recv(self.dict_size))
        return data

    def get(self, key):
        self.initialize()
        self.sock.send(dumps({
            'operation': 'GET',
            'key': key,
        }
        )
        )
        data = loads(self.sock.recv(self.dict_size))
        return data

    def getlock(self, key):
        self.initialize()
        self.sock.send(dumps({
            'operation': 'GETLOCK',
            'key': key,
        }
        )
        )
        data = loads(self.sock.recv(self.dict_size))
        return data

    def freelock(self, key, secret):
        self.initialize()
        self.sock.send(dumps({
            'operation': 'FREELOCK',
            'key': key,
            'secret': secret
        }
        )
        )
        data = loads(self.sock.recv(self.dict_size))
        return data

    def set(self, key, value):
        self.initialize()
        self.sock.send(dumps({
            'operation': 'SET',
            'key': key,
            'value': value,
        }
        )
        )
        data = loads(self.sock.recv(self.dict_size))
        return data

    def close(self):
        self.sock.close()


class DepotDaemon(Daemon):
    def run(self):
        depot_server()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test|start|stop|restart|version')
    parser.add_argument('status', action="store", type=str)
    depot_daemon = DepotDaemon('/tmp/depot.pid')
    if parser.parse_args().status == "test":
        depot_server()
    if parser.parse_args().status == "start":
        depot_daemon.start()
    elif parser.parse_args().status == "stop":
        depot_daemon.stop()
    elif parser.parse_args().status == "restart":
        depot_daemon.restart()
    elif parser.parse_args().status == "version":
        print "Depot v%s (https://github.com/atmb4u/depot/) \ndepot -h for help" % __VERSION__
