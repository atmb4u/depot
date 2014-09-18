#!/usr/bin/python

import argparse
from multiprocessing.managers import SyncManager
from daemon import Daemon


class Depot(object):
    sync_depot = {}

    def __init__(self, ip="127.0.0.1", port=9000, key="random_key"):
        self.manager = SyncManager((ip, port), authkey=key)

    def get_depot(self):
        return self.sync_depot


class DepotServer(Depot):

    def start_server(self):
        SyncManager.register("sync_depot", self.get_depot)
        self.manager.start()
        self.manager.join()
        raw_input("Press any key to kill server".center(50, "-"))
        # self.manager.shutdown()


class DepotClient(Depot):

    def __init__(self, ip="127.0.0.1", port=9000, key="random_key"):
        self.manager = SyncManager((ip, port), authkey=key)
        SyncManager.register("sync_depot")
        self.manager.connect()
        self.sync_depot = self.manager.sync_depot()

    def set(self, key, value):
        try:
            self.sync_depot.update([(key, value)])
        except (EOFError, IOError):
            print "Server process hung up. Restart and reinitialise client."
            return False

    def delete(self, key):
        self.sync_depot.update([(key, None)])

    def get(self, key):
        try:
            return self.get_depot().get(key)
        except (EOFError, IOError):
            print "Server process hung up. Restart and reinitialise client."
            return False


class DepotDaemon(Daemon):
    def run(self):
        d = DepotServer()
        d.start_server()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start|stop|restart')
    parser.add_argument('status', action="store", type=str)
    # depot_daemon = DepotDaemon()
    # daemon_runner = runner.DaemonRunner(depot_daemon)
    # daemon_runner.do_action()
    depot_daemon = DepotDaemon('/tmp/depot.pid')
    if parser.parse_args().status == "start":
        depot_daemon.start()
    elif parser.parse_args().status == "stop":
        depot_daemon.stop()
    elif parser.parse_args().status == "restart":
        depot_daemon.restart()
