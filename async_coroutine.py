import time
import selectors
import socket

selector = selectors.DefaultSelector()
task_cnt = 0

class Future:  # future object, coroutine yield for
    def __init__(self):
        self.result = None
        self._callback = None

    def add_done_callback(self, fn):
        self._callback = fn

    def resolve_result(self, result):
        self.result = result
        if self._callback:
            self._callback(self)

class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.result = None # start coroutine
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step) # and pass next_future in

def fetch(url):
    global task_cnt
    response = []
    task_cnt += 1
    request = 'GET {} HTTP/1.1\r\nHOST localhost\r\n\r\n'.format(url) # unicorn

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)
    try:
        sock.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(sock.fileno(), selectors.EVENT_WRITE, f)
    yield f
    sock.send(request.encode('ascii'))  # byte code
    selector.unregister(sock.fileno())

    while True:
        f = Future()
        selector.register(sock.fileno(), selectors.EVENT_READ, f)
        yield f
        selector.unregister(sock.fileno())
        chunk = sock.recv(4096)
        if chunk:
            response.append(chunk)
        else:
            print(response[0].split()[1])
            task_cnt -= 1
            return

def loop(tasks):
    for task in tasks:
        Task(task)
    while task_cnt:
        event = selector.select() 
        for (event_key, event_mask) in event:
            f = event_key.data
            f.resolve_result(None)

start = time.time()
loop([fetch('/'), fetch('/'), fetch('/'), fetch('/'), fetch('/')])
print("time {}".format(time.time() - start))
