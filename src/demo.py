from eks import EKSConnector, EKSCallback
import datetime, time

class EKSConnectorMock(EKSConnector):

    def __init__ (self, callback, host, port=2444):
        super(EKSConnectorMock, self).__init__(callback, host, port)
        self.expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        self.is_active = False

    def read_key_state(self, callback): # override networking
        now = datetime.datetime.now()

        if self.is_active:
            callback.did_insert_key()
            callback.did_read_key("12345678")
        else:
            callback.did_remove_key()

        if now > self.expiration_date:
            self.is_active = not self.is_active
            self.expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=5)

class MyEKSCallback(EKSCallback):

    def did_insert_key(self):
        print "did insert key"

    def did_remove_key(self):
        print "did remove key"

    def did_read_key(self, data):
        print "did read key: %s" % data

callback = MyEKSCallback()
eks = EKSConnector("127.0.0.1", 2444)

print "single call: "
eks.read_key_state(callback)

print "\npermanent call: "
eks.start_listening(callback)
