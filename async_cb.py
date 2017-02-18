import time
import selectors
import socket

selector = selectors.DefaultSelector()
task_cnt = 0

def fetch(url):
    global task_cnt
    task_cnt += 1
    response = []
    request = 'GET {} HTTP/1.1\r\nHOST localhost\r\n\r\n'.format(url) # unicorn
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)
    try:
        sock.connect(('localhost', 5000))
    except BlockingIOError:
        pass
    connect_cb = lambda: on_connect(sock, request, response)
    selector.register(sock.fileno(), selectors.EVENT_WRITE, connect_cb)

def on_connect(sock, request, response):
    sock.send(request.encode('ascii'))  # byte code
    selector.unregister(sock.fileno())
    read_cb = lambda: on_read(sock, request, response)
    selector.register(sock.fileno(), selectors.EVENT_READ, read_cb)

def on_read(sock, request, response):
    chunk = sock.recv(4096)
    while True:
        try:
            chunk = sock.recv(4096)
        except BlockingIOError:
            pass
        if chunk:
            response.append(chunk)
        else: break
    # raise Exception("我是故意的")
    print(response[0].split()[1])
    global task_cnt
    task_cnt -= 1

def loop(tasks):
    for task in tasks:
        task
    while task_cnt:
        event = selector.select() 
        for (event_key, event_mask) in event:
            callback = event_key.data
            callback()

start = time.time()
loop([fetch('/'), fetch('/'), fetch('/'), fetch('/'), fetch('/')])
print("time {}".format(time.time() - start))
