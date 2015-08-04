import socket, threading, time


class EKSResponse:
    def __init__(self, command, status, payload):
        self.command = command
        self.status = status
        self.payload = payload

    def __eq__(self, other):
        if other == None:
            return False
        return self.command == other.command \
                and self.status == other.status \
                and self.payload == other.payload


class EKSConnector(object):

    def __init__ (self, host, port=2444, timeout=5):
        self.host = host
        self.port = port
        self.poll_interval = 1
        self.socket_timeout = timeout


    def __poll(self):
        last_response = None
        while self.polling_enabled:
            self.read_key_state(self.callback)
            time.sleep(self.poll_interval)


    def __send_to_socket(self, msg):
        bytes_sent = self.eks_socket.send(msg)
        return bytes_sent


    def __read_from_socket(self):
        chunks = []
        bytes_recd = 0
        msglen = 123
        command = ''
        status = -1
        start = 0
        length = 0

        while bytes_recd < msglen:
            chunk = self.eks_socket.recv(1)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk.encode("hex"))

            if bytes_recd == 0:
                msglen = ord(chunk)
            if bytes_recd == 1:
                command += chunk
            if bytes_recd == 2:
                command += chunk
            if bytes_recd == 6:
                status = ord(chunk)

            bytes_recd = bytes_recd + len(chunk)
            
        payload = ''.join(chunks[8:len(chunks)])
        return EKSResponse(command, status, payload)


    def read_key_state(self, callback):
        self.eks_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.eks_socket.settimeout(self.socket_timeout)
        self.eks_socket.connect((self.host, self.port))
        
        response = self.__read_from_socket()
        self.__handle_response(response, callback)

        if response.command == "Ek" and response.status == 1:
            self.__send_to_socket("\x07TL\x01\x01\x73\x09")
            response = self.__read_from_socket()    
            self.__handle_response(response, callback)
        
        self.eks_socket.close()
        return response


    def start_listening(self, callback, interval=1):
        self.polling_enabled = True
        self.callback = callback
        self.poll_interval = interval
        self.__poll()


    def stop_listening(self):
        self.polling_enabled = False


    def __handle_response(self, response, callback):
        if response.command == "Ek":
            if response.status == 1:
                callback.did_insert_key()
            elif response.status == 2:   
                callback.did_remove_key()
            elif response.status == 3:
                raise RuntimeError
        elif response.command == "RL":
            callback.did_read_key(response.payload)


class EKSCallback: #abstract

    def did_insert_key(self):
        raise NotImplementedError

    def did_remove_key(self):
        raise NotImplementedError

    def did_read_key(self, data):
        raise NotImplementedError
