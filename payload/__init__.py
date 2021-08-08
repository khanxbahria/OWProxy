import base64

class TCPFlow:
    def __init__(self, payload):
        self.payload = payload

class Payload:
    def __init__(self, payload):
        self.payload = payload
    def encode(self):
        return b"<m>" + base64.b64encode(self.payload) + b"</m>\x00"
    def decode(self):
        return base64.b64decode(self.payload[3:-5])