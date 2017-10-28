# coding: utf-8

# standard library
import os
import sys
import time
import urllib
import webbrowser
from subprocess import Popen, PIPE

# module constants
PORT = 8888
RESERVED = ';/?:@&=+$,'


# functions
def listened(port):
    """Check if the spacified port is listened or not."""
    cmd = "lsof -i :{} | grep 'LISTEN'".format(port)
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    return bool(proc.communicate()[0])


def launch_jupyter(port):
    """Launch a Jupyter Notebook Server with the spacified port."""
    cmd_jupyter = 'jupyter notebook ~/ --port={} --no-browser &'.format(port)
    cmd_launcher = "bash -cl '{}' > /dev/null 2>&1".format(cmd_jupyter)
    proc = Popen(cmd_launcher, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    proc.communicate()


# main part
if __name__ == '__main__':
    ipynbs = sys.argv[1:]

    if not listened(PORT):
        launch_jupyter(PORT)

    while not listened(PORT):
        time.sleep(0.5)

    try:
        home = 'http://localhost:{}'.format(PORT)
        urllib.urlopen(home)
    except IOError:
        home = 'https://localhost:{}'.format(PORT)

    if ipynbs:
        for ipynb in ipynbs:
            path = os.path.relpath(ipynb, os.environ['HOME'])
            note = home + '/notebooks/{}'.format(path)
            webbrowser.open(urllib.quote(note, RESERVED))
    else:
        webbrowser.open(urllib.quote(home, RESERVED))
