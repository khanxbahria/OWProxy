import re

class URLBlocker:
    def __init__(self, flow):
        self.flow = flow
        self.new_avi_img_with_len = b"\x00\x1ci/players/group55/user110008"

    def replace_avi_image(self):
        parts_i = [m.start() + 4 for m in re.finditer(b"\x19L", self.flow.payload, flags=re.DOTALL)]
        parts_len = [int.from_bytes(self.flow.payload[part_i-2:part_i], 'big') for part_i in parts_i]
        parts_with_len = [self.flow.payload[part_i-2:part_i+part_len] for part_i, part_len in zip(parts_i, parts_len)]
        for part in parts_with_len:
            self.flow.payload = self.flow.payload.replace(part, self.new_avi_img_with_len)      

    def block_malicious(self):
        self.flow.payload = self.flow.payload.replace(b"http",b"abcd")
        if b"\x19L" in self.flow.payload:
            self.replace_avi_image()

class Plugin:
    is_active = False
    def __init__(self, proxy):
        self.proxy = proxy

    def process_incoming(self, flow):
        if self.is_active:
            URLBlocker(flow).block_malicious()

    def process_outgoing(self, flow):
        pass