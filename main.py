import threading
import time
import random
from stem.control import Controller, Signal
#import requests

from Queue import Queue

def load_template(config_file):
    lines = filter(lambda x: len(x) > 0 and x[0] != '#', open(config_file).read().split('\n'))
    return map(lambda x: x.split(','), lines)

def download_data(queue, template, to_sleep, config, build_request):
    while True:
        try:
            n = queue.get(timeout=0.1)
        except Exception:
            return

        print "Downloading data of bug_{}".format(n)
        
        if queue.empty():
            return
        
        time.sleep(random.randint(1, to_sleep))
        
        

def change_circuit(controller, to_sleep):
    while True:
        time.sleep(random.randint(1, to_sleep))
        controller.signal(Signal.NEWNYM)
        print "Changing circuit"
        


def config_tor_browser():
    controller = Controller.from_port(port = 9151)
    controller.authenticate()
    return controller

def build_request(url, config):
    pass
    # return request

if __name__ == '__main__':
    controller = config_tor_browser()
    template = load_template('template.txt')
    download_threads = 10
    config = load_config('configuration.txt')

    queue = Queue()

    start = 1
    end = 100
    for i in range(start, end+1):
        queue.put(i)


    t1 = threading.Thread(target = change_circuit, args = (None, 3,))
    t1.daemon = True
    t1.start()

    for _ in range(download_threads):
        t = threading.Thread(target=download_data, args = (queue, template, 5, config, build_request,))
        t.daemon = True
        t.start()
    
    while threading.active_count() > 2:
        time.sleep(0.1)


