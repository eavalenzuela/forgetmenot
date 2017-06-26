import socket, re
s = socket.socket()
host = socket.gethostname()
print('Please select a port to receive on.')
port = input()
print('Please enter a filename to output.')
filename = raw_input()

if re.match('\d{1,5}', str(port)) and filename != "" and filename != None:
    s.bind(('', port))
    with open(filename, 'w') as f:
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

