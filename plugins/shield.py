import re
from urllib.parse import urlparse

class URLParser:
    def __init__(self, flow):
        self.flow = flow
        self.og_payload = flow.payload
        self.og_with_len = b""
        self.new_url = "http://8.8.8.8"
        self.og_url = ""
        self.og_hostname = ""
        self.new_payload = b""
    
    def parse(self):
        if not b"http" in self.og_payload:
            return
        r = re.search(b"(?P<url>https?://[^\s]+)",
                             self.og_payload, flags=re.DOTALL)
        if not r:
            return False
        url_i = r.start()
        url_len = int.from_bytes(self.og_payload[url_i-2:url_i], 'big')
        self.og_with_len = self.og_payload[url_i-2:url_i+url_len]
        self.og_url = self.og_with_len[2:].decode()
        self.og_hostname = urlparse(self.og_url).netloc
        return self.og_url

    def replace(self):
        new_with_len = len(self.new_url).to_bytes(2, 'big') 
        new_with_len += self.new_url.encode()
        new_payload = self.og_payload\
                            .replace(self.og_with_len, new_with_len)
        self.flow.payload = new_payload

    def replace_unknown(self):
        # print("url found --->", self.og_url)
        trusted = ["cdn-ssl.ourworld.com", "ourworld.com"]
        if self.og_hostname not in trusted:
            # print("url is not trusted")
            self.replace()
            # print("replaced", self.flow.payload)

    def block_malicious(self):
        if self.parse():
            self.replace_unknown()
        av_ident = b"/players/g"
        if av_ident in self.flow.payload:
            # print("blocking avi image")
            self.flow.payload = self.flow.payload\
                                    .replace(av_ident, b"a"*len(av_ident))


class Plugin:
    is_active = False
    def __init__(self, proxy):
        self.proxy = proxy

    def process_incoming(self, flow):
        if self.is_active:
            URLParser(flow).block_malicious()

    def process_outgoing(self, flow):
        pass