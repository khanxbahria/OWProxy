import asyncio
import sys
import importlib
import os
from os import path
import json
from traceback import print_exc


from settings import Settings
from payload import Payload, TCPFlow

from core_plugins.session_userid import UserID

class ProxyServer:
    def __init__(self):
        Settings.set_gamehost("game2.ourworld.com")
        self.sessions = []
        self.plugins = self.load_plugins("core_plugins")\
                                         + self.load_plugins("plugins")

    def load_plugins(self, plugin_type):
        json_path = path.abspath(path.join(
                            path.dirname(__file__), 'plugins.json'))
        with open(json_path) as f:
            data = json.load(f)
        plugin_names = data[plugin_type]
        plugins = [
            importlib.import_module(
                f"{plugin_type}.{plugin}").Plugin(self) for plugin in plugin_names
        ]
        return plugins

    def switch_gamehost(self, gamehost):
        Settings.set_gamehost(gamehost)
        self.close_current_sessions()

    async def handle_client(self, local_reader, local_writer):
        print("[+] New session connected.")
        remote_reader, remote_writer = await asyncio.open_connection(
                                        Settings.gamehost_ip, 9310,
                                         limit=4096*2000)
        session = Session(local_reader, local_writer,
                         remote_reader, remote_writer, self.plugins)
        self.sessions.append(session)
        pipe1 = session.pipe(is_outgoing=True)
        pipe2 = session.pipe(is_outgoing=False)
        try:
            await asyncio.gather(pipe1, pipe2)
        except:
            print_exc()
        finally:
            if session in self.sessions:
                session.close()

    def send_outgoing_payload(self, payload):
        if UserID.uid:
            for session in self.sessions:
                session.send_payload(payload, is_outgoing=True)


    def send_incoming_payload(self, payload):
        if UserID.uid:
            for session in self.sessions:
                session.send_payload(payload, is_outgoing=False)

    def close_current_sessions(self):
        for session in self.sessions[:]:
            print("[+] Closing connection.")
            session.close()
            self.sessions.remove(session)



    async def start(self):
        server = await asyncio.start_server(
        self.handle_client, '127.0.0.1', 9310)
        print(f'Serving')
        async with server:
            await server.serve_forever()


class Session:
    def __init__(self, local_reader, local_writer,
                 remote_reader, remote_writer, plugins):
        self.local_reader = local_reader
        self.local_writer = local_writer
        self.remote_reader = remote_reader
        self.remote_writer = remote_writer
        self.plugins = plugins

    async def pipe(self, is_outgoing):
        if is_outgoing:
            src_reader = self.local_reader
            dst_writer = self.remote_writer
        else:
            src_reader = self.remote_reader
            dst_writer = self.local_writer

        while not src_reader.at_eof():
            try:
                p = await src_reader.readuntil(b'\x00')
            except Exception as e:
                raise e
                
            payload = Payload(p).decode()
            flow = TCPFlow(payload)

            for plugin in self.plugins:
                try:
                    if is_outgoing:
                        plugin.process_outgoing(flow)
                    else:
                        plugin.process_incoming(flow)
                except:
                    print_exc()

            if flow.payload:
                payload = Payload(flow.payload).encode()
                dst_writer.write(payload)
                    

    def send_payload(self, payload, is_outgoing):
        try:
            if is_outgoing:
                self.remote_writer.write(Payload(payload).encode())
            else:
                self.local_writer.write(Payload(payload).encode())
        except:
            pass


    def close(self):
        try:
            self.local_writer.close()
            self.remote_writer.close()
        except Exception as e:
            # print(f"Couldn't close session.")
            pass


if __name__ == "__main__":
    Settings.hosts_config.add_host_overrides()
    proxy_server = ProxyServer()

    try:
        asyncio.run(proxy_server.start())
    except KeyboardInterrupt:
        pass
    Settings.hosts_config.rem_host_overrides()
    sys.exit()