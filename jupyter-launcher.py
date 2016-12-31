# coding: utf-8

"""Script for the Jupyter Launcher Application."""

import os
import sys
import time
import webbrowser
from subprocess import Popen, PIPE


def listened(port):
    """Check if the spacified port is listened or not."""
    cmd = "lsof -i :{} | grep 'LISTEN'"
    proc = Popen(cmd.format(port), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    return bool(proc.communicate()[0])


def launch_jupyter(port):
    """Launch a Jupyter Notebook Server with the spacified port."""
    cmd = "bash -cl 'jupyter-notebook ~/ --port={} --no-browser &' > /dev/null 2>&1"
    proc = Popen(cmd.format(port), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    proc.communicate()


if __name__ == '__main__':
    PORT = 8888
    ipynbs = sys.argv[1:]

    if not listened(PORT):
        launch_jupyter(PORT)

    while not listened(PORT):
        time.sleep(0.5)

    if ipynbs:
        for ipynb in ipynbs:
            url = 'http://localhost:{}/notebooks/{}'
            path = os.path.relpath(ipynb, os.environ['HOME'])
            webbrowser.open(url.format(PORT, path))
    else:
        url = 'http://localhost:{}/tree'
        webbrowser.open(url.format(PORT))