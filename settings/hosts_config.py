import os
import platform
from traceback import print_exc
import subprocess


class HostsConfig:
    def __init__(self, gamehosts={}):
        self.os = platform.system()
        self.hostspath = self.get_hosts_path()
        self.gamehosts = gamehosts
    
    def get_hosts_path(self):
        if self.os == "Windows":
            return "C:\\Windows\\System32\\Drivers\\etc\\hosts"
        else:
            return "/etc/hosts"

    def flush_dns(self):
        if self.os == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["ipconfig", "/flushdns"],
                             shell=False, startupinfo=startupinfo)
        else:
            subprocess.run(["killall", "-HUP", "mDNSResponder"])

    def load_hosts(self):
        try:
            with open(self.hostspath, "r") as f:
                return f.read()
        except:
            print_exc()
            return False

    def save_hosts(self, content):
        with open(self.hostspath, "w") as f:
            f.write(content)

        self.flush_dns()
        

    def rem_host_overrides(self):
        newhosts = ""
        oldhosts = self.load_hosts()
        if not oldhosts: return

        for line in oldhosts.split("\n"):
            if len(line) <= 1: continue
            badline = False
            for host in self.gamehosts:
                if host in line: badline = True

            if badline: continue

            newhosts += line + "\n"
        return self.save_hosts(newhosts)

    def add_host_overrides(self, domain=None):
        # remove any host overrides if there
        self.rem_host_overrides()
        newhosts = self.load_hosts()

        if not domain:
            for host, _ in self.gamehosts.items():
                newhosts += "127.0.0.1" + " " + host + "\n"
        else:
            for host in self.gamehosts:
                newhosts += self.gamehosts[domain] + " " + host + "\n"
        return self.save_hosts(newhosts)


