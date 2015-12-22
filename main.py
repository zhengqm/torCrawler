import threading
import time
import random
import requesocks

from stem.control import Controller, Signal
from Queue import Queue

def load_template(template_file):
    lines = filter(lambda x: len(x) > 0 and x[0] != '#', open(template_file).read().split('\n'))
    return map(lambda x: x.split(','), lines)

def download_data(queue, templates, to_sleep, config):
    session = requesocks.session()

    session.proxies = {
        'http': '{}://{}:{}'.format(config['protocal'], config['address'], config['port']),
        'https': '{}://{}:{}'.format(config['protocal'], config['address'], config['port']),
    }

    while True:
        try:
            n = queue.get(timeout=0.1)
        except Exception:
            return

        # Download the specified page
        print "Downloading data of bug_{}".format(n)

        for url_template, file_template in templates:
            url = url_template.format(n)
            resp = session.get(url)
            with open(file_template.format(n), 'w') as f:
                f.write(resp.text)

        # Finish downloading...

        if queue.empty():
            return
        
        time.sleep(random.randint(1, to_sleep))
        
        

def change_circuit(controller, to_sleep):
    while True:        
        controller.signal(Signal.NEWNYM)
        time.sleep(to_sleep)
        print "Changing circuit"
        circuits = controller.get_circuits()

        print "End Point:"
        for circ in circuits:
            entry = circ.path[-1]
            fingerprint, nickname = entry
            desc = controller.get_network_status(fingerprint, None)
            address = desc.address if desc else 'unknown'
            print address
        


def config_tor_browser():
    controller = Controller.from_port(port = 9151)
    controller.authenticate()
    return controller


def load_config(config_file):
    lines = filter(lambda x: len(x) > 0 and x[0] != '#', open(config_file).read().split('\n'))
    return dict(map(lambda x: x.split(':'), lines))

if __name__ == '__main__':
    controller = config_tor_browser()
    template = load_template('template.txt')
    download_threads = 10
    config = load_config('configuration.txt')
    queue = Queue()

    # Initialize queue
    start = 1
    end = 100
    for i in range(start, end+1):
        queue.put(i)


    # Initialize thread for changing circuit
    t1 = threading.Thread(target = change_circuit, args = (None, 60,))
    t1.daemon = True
    t1.start()

    # Initialize thread for downloading pages
    for _ in range(download_threads):
        t = threading.Thread(target=download_data, args = (queue, template, 10, config,))
        t.daemon = True
        t.start()
    
    # Wait for downloading
    while threading.active_count() > 2:
        time.sleep(0.1)


