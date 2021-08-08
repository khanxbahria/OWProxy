
class UserID:
    uid = 0
    uid_hex = b''

    @classmethod
    def set_uid(cls, hex=b"", uid=0):
        if uid:
            cls.uid = uid
            cls.uid_hex = uid.to_bytes(4, 'big')
        elif hex:
            cls.uid_hex = hex
            cls.uid = int.from_bytes(hex, 'big')


class Plugin:
    def __init__(self, proxy):
        self.proxy = proxy

    def process_incoming(self, flow):
        pass

    def process_outgoing(self, flow):
        if len(flow.payload) == 27 and flow.payload[-11:-4] == b'\x14\x00\x00\x00\x08\x0c[':
            uid_hex = flow.payload[-4:]
            UserID.set_uid(hex=uid_hex)
        elif b"\x06helper" in flow.payload:
            uid_hex = flow.payload[17:21]
            UserID.set_uid(hex=uid_hex)



