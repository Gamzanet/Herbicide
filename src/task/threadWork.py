import threading
import os
import subprocess
class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

def testRun(command):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'engine', 'gamza-dynamic'))
    print(command)
    path = os.path.abspath(__file__)
    print(path)
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=target_dir)
    return result
def threadRun(command):
    thread = ThreadWithReturnValue(target=testRun, args=(command,))
    thread.start()
    return thread
    