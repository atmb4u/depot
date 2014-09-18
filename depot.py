#!/usr/bin/python

import argparse
from multiprocessing.managers import SyncManager
from daemon import Daemon

__VERSION__ = "1.0.3"


class Depot(object):
    """
    Depot object is the parent object to create SyncManager with 
    args: ip, port, key
    """
    sync_depot = {}

    def __init__(self, ip="127.0.0.1", port=9000, key="random_key"):
        self.manager = SyncManager((ip, port), authkey=key)

    def get_depot(self):
        return self.sync_depot


class DepotServer(Depot):
    """
    Class for Depot server. start_server function creates a manager
    and waits for requests
    """

    def start_server(self):
        SyncManager.register("sync_depot", self.get_depot)
        self.manager.start()
        self.manager.join()
        raw_input("Press any key to kill server".center(50, "-"))


class DepotClient(Depot):
    """
    DepotClient is used to connect to the server and to get and set data
    """
    def __init__(self, ip="127.0.0.1", port=9000, key="random_key"):
        self.manager = SyncManager((ip, port), authkey=key)
        SyncManager.register("sync_depot")
        self.manager.connect()
        self.sync_depot = self.manager.sync_depot()

    def set(self, key, value):
        """
        Update key with corresponding value
        """
        try:
            self.sync_depot.update([(key, value)])
        except (EOFError, IOError):
            print "Server process hung up. Restart and reinitialise client."
            return False

    def delete(self, key):
        """
        delete the value stored in the key and sets it to None
        """
        self.sync_depot.update([(key, None)])

    def get(self, key):
        """
        Get the data stored in a particular 'key'
        """
        try:
            return self.get_depot().get(key)
        except (EOFError, IOError):
            print "Server process hung up. Restart and reinitialise client."
            return False


class DepotDaemon(Daemon):
    """
    Start the depot server in daemon mode
    """
    def run(self):
        d = DepotServer()
        d.start_server()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start|stop|restart|version')
    parser.add_argument('status', action="store", type=str)
    depot_daemon = DepotDaemon('/tmp/depot.pid')
    if parser.parse_args().status == "start":
        depot_daemon.start()
    elif parser.parse_args().status == "stop":
        depot_daemon.stop()
    elif parser.parse_args().status == "restart":
        depot_daemon.restart()
    elif parser.parse_args().status == "version":
        print "Depot v%s (https://github.com/atmb4u/depot/) \ndepot -h for help" % __VERSION__
