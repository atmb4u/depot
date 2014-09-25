#!/usr/bin/python

import argparse
from multiprocessing.managers import SyncManager
from daemon import Daemon

__VERSION__ = "1.0.7"

import socket
import os
from cPickle import dumps, loads


def depot_server(dict_size=4096):
    data_store = {}
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
            if operation == "UPDATE":
                data_store.update(packet.get('data'))
                print data_store
                conn.send("S'True'\np1\n.")
            elif operation == "GET":
                conn.send(dumps(data_store.get(packet.get('key'))))
            elif operation == "DELETE":
                data_store.__delitem__(packet.get('key'))
                conn.send("S'True'\np1\n.")
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

    def close(self):
        self.sock.close()


class DepotDaemon(Daemon):
    def run(self):
        depot_server()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start|stop|restart|version')
    parser.add_argument('status', action="store", type=str)
    depot_daemon = DepotDaemon('/tmp/depot.pid')
    if parser.parse_args().status == "start":
        depot_server()
    elif parser.parse_args().status == "stop":
        depot_daemon.stop()
    elif parser.parse_args().status == "restart":
        depot_daemon.restart()
    elif parser.parse_args().status == "version":
        print "Depot v%s (https://github.com/atmb4u/depot/) \ndepot -h for help" % __VERSION__
