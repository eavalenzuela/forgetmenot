import socket, re, sys
s = socket.socket()
host = socket.gethostname()
print('Please select a port to receive on.')
port = input()

if re.match('\d{1,5}', str(port)):
    s.bind(('', port))
    s.listen(5)
    print('Waiting for connection...')
    while True:
        c,addr = s.accept()
        print('Incoming connection from ', addr)
        print('Receiving file name...')
        if sys.version_info < (3, 0):
            fn = (c.recv(1024)).decode('utf-8')
        else:
            fn = c.recv(1024)
        c.close()
        break
    
    if fn is None or fn is "":
        print('File name not received. Please enter.')
        fn = rawinput()

    print('filename: '+fn)
    with open(fn, 'w') as f:
        s.listen(5)
        print('Waiting for connection...')
        while True:
            c, addr = s.accept()
            print('Incoming connection from ', addr)
            print('Receiving file...')
            l = c.recv(1024)
            while l:
                print('Receiving file...')
                f.write(l)
                l = c.recv(1024)
            f.close()
            print('Done receiving')
            c.send('File received. Closing connection.')
            c.close()
            break

