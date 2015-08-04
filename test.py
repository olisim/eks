import socket
import time

class Response:
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload

class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def mysend(self, msg):
        bytes_sent = self.sock.send(msg)
        return bytes_sent
        # totalsent = 0
        # while totalsent < len(msg):
        #     sent = self.sock.send(msg[totalsent:])
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        msglen = 123
        command = ''
        status = -1

        while bytes_recd < msglen:
            chunk = self.sock.recv(1)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)

            if bytes_recd == 0:
                msglen = ord(chunk)
            if bytes_recd == 1:
                command += chunk
            if bytes_recd == 2:
                command += chunk
            if bytes_recd == 6:
                status = ord(chunk)

            bytes_recd = bytes_recd + len(chunk)
            # print "(" + str(bytes_recd) + ") \t" + str(ord(chunk)) + "\t" + str(msglen)


        # if bytes_recd > 3:
        # print command + "/" + str(status)
        # print ''.join(chunks)
        if command == "Ek":
            if status == 1:
                return Response("EKS_KEY_IN", None)
            if status == 2:
                return Response("EKS_KEY_OUT", None)
            if status == 3:
                return Response("EKS_KEY_OTHER", None)
        else:
            return Response(command, ''.join(chunks))


mysock = mysocket()
mysock.connect("127.0.0.1", 2444)
status = ''
while True:
    mysock.mysend("\x07Ek\x01\x00\x00\x00")
    new_status = mysock.myreceive()
    if new_status != status:
        print 'new status'
        status = new_status
        print new_status
        print status

    if status == "EKS_KEY_IN":
        mysock.mysend("\x07TL\x01\x00\x00\x74")
        print mysock.myreceive()
