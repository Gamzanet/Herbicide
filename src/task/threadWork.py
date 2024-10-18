import threading



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

def f(x):
    return 1


thread = ThreadWithReturnValue(target=f, args=(5))


thread.start()


result = thread.join()

print(f"결과: {result}")