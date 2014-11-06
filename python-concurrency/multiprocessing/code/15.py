"""
Sometimes it is useful to allow more than one worker access to a resource at a
time, while still limiting the overall number. For example, a connection pool
might support a fixed number of simultaneous connections, or a network
application might support a fixed number of concurrent downloads. A Semaphore
is one way to manage those connections.
"""

import multiprocessing
import time
import random

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.mgr = multiprocessing.Manager()
        self.active = self.mgr.list()
        self.lock = multiprocessing.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)

    def __str__(self):
        with self.lock:
            return str(self.active)

def worker(s, pool):
    name = multiprocessing.current_process().name
    with s:
        pool.makeActive(name)
        print 'Now running:', str(pool)
        time.sleep(random.random())
        pool.makeInactive(name)

if __name__ == '__main__':
    pool = ActivePool()
    s = multiprocessing.Semaphore(3)

    jobs = [multiprocessing.Process(target=worker, name=str(i), args=(s, pool))
            for i in range(10)]

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
        print 'Now running: %s' % str(pool)
