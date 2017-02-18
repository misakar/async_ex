import socket
import time

def fetch(url):
    # AF_INET: ipv4, SOCK_STREAM: tcp socket
    request = 'GET {} HTTP/1.1\r\nHOST localhost\r\n\r\n'.format(url)
    response = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5000))  # blocking
    sock.send(request.encode('ascii')) # byte stream, blocking
    # Transfer-Encoding: chunk
    chunk = sock.recv(2048)  # blocking -> system call
    while chunk:
        response.append(chunk)
        chunk = sock.recv(2048)  # blocking
    print(response[0].split()[1])

def main(tasks):
    for task in tasks:
        task

start = time.time()
main([fetch('/'), fetch('/')])
print('time: {}'.format(time.time()-start))
