import os
import json
import re

from core_plugins.session_userid import UserID


class OutfitInfo:
    def __init__(self, data):
        self.data = data
        self.payload = self.gen_outfit_payload()

    def gen_outfit_payload(self):
        payload = ( b"\x01\x00\x00\x01\x87\x00\x00\x00\x83\xff\xff\x0c["
                 + UserID.uid_hex + (len(self.data)).to_bytes(2,"big") )
        for item in self.data:
            type, path = item["type"], item["path"]
            payload += ( b"\x01A\x00\x02\x19X" + len(type).to_bytes(2,"big")
                        + type.encode()+b"\x19?"+len(path).to_bytes(2,"big")
                        + path.encode() )

        payload = (len(payload)).to_bytes(4,"big") + payload
        return payload



class OutfitManager:
    outfits = {}
    current_outfit = OutfitInfo([])
    wl_active = False
    is_active = False


    @classmethod
    def load_data(cls):
        for fname in os.listdir('outfits'):
            if not fname.endswith('.json'):
                continue
            name = fname[:-5]
            with open(f'outfits/{fname}') as f:
                cls.outfits[name] = json.load(f)

    @classmethod
    def save_outfit(cls, name):
        cls.outfits[name] = cls.current_outfit.data
        with open(f'outfits/{name}.json' , 'w') as f:
            json.dump(cls.current_outfit.data, f, indent=4)

    @classmethod
    def delete_outfit(cls, name):
        del cls.outfits[name]
        os.remove(f'outfits/{name}.json')

    @classmethod
    def select_current_outfit(cls, name):
        cls.wl_active = False
        outfit_data = cls.outfits.get(name, None)
        if outfit_data:
            cls.current_outfit = OutfitInfo(outfit_data)

    @classmethod
    def activate_wl(cls, x=True):
        if x:
            cls.current_outfit = OutfitInfo([])
            cls.wl_active = True
        else:
            cls.wl_active = False

  




OutfitManager.load_data()
OutfitManager.select_current_outfit("Wishlist")


class Plugin:
    def __init__(self, proxy):
        self.proxy = proxy
        self.send_next = False

    def process_outgoing(self, flow):
        # flow.payload
        pass

    def process_incoming(self, flow):
        if OutfitManager.is_active:
            self._process_incoming(flow)

    def _process_incoming(self, flow):
        if self.send_next:
            # Send outfit payload
            self.show_outfit()
            self.send_next = False

        others_items_cond = (b"i/avatars" in flow.payload
                         and not UserID.uid_hex in flow.payload)


        wl_cond = (b"\x0c<\x00\x00\x00\x02" in flow.payload 
                and b"\xff\xfc\x0c\x14\x00\x00\x00\x08\x0cv" in flow.payload
                 and my_items_cond)

        if OutfitManager.wl_active and wl_cond:
            # Wishlist detected refresh outfit
            outfit_data = self.payload_to_outfit(flow.payload)
            OutfitManager.current_outfit = OutfitInfo(outfit_data)
            self.send_next = True

        elif others_items_cond:
            # If any item detected refresh outfit
            self.send_next = True


    def show_outfit(self):
        cur_outfit = OutfitManager.current_outfit
        if cur_outfit.data:
            self.proxy.send_outgoing_payload(cur_outfit.payload)
            self.proxy.send_incoming_payload(cur_outfit.payload)

    def force_update(self):
        if OutfitManager.wl_active:
            self.ask_wl()
        self.show_outfit()

    def ask_wl(self):
        payload = ( b'\x00\x00\x00\x1d\x01\x00\x00\x00a\x00\x08\x00G'
                    b'\x00\x03\x0c[' + UserID.uid_hex +b'\x0c\x14\x00\x00'
                    +b'\x00\x08\x0c<\x00\x00\x00\x02' )
        self.proxy.send_outgoing_payload(payload)

    def payload_to_outfit(self,payload):
        # dont parse payload if too long
        if len(payload) > 2444:
            return []
        try:
            data = self.p2fit1(payload)
        except:
            try:
                data = self.p2fit2(payload)
            except:
                # print(f"Couldn't parse outfit payload {payload}")
                data = []
        return data



    def p2fit1(self, payload):
        paths_i = [m.start() for m in re.finditer(b'i/avatars', payload)]
        paths_len = [int.from_bytes(payload[i-2:i], 'big') for i in paths_i]
        paths = [payload[i:i+path_len].decode() for i, path_len in zip(paths_i, paths_len)]
        types_i = [m.start() for m in re.finditer(b'\r7', payload)]
        types_len = [int.from_bytes(payload[i+8:i+10], 'big') for i in types_i]
        types = [payload[i+10:i+10+type_len].decode() for i, type_len in zip(types_i, types_len)]
        tup = zip(types, paths)
        return [{"type":type, "path":path} for type,path in tup]

    def p2fit2(self, message):
        """
        Parses the types and paths of the
        items and adds them to a dictionaries
        and returns them in a list.
        """
        items   = []
        clothes = message.split(b"\x01A")[1:]
        for item in clothes:
            len_type = int.from_bytes(
                    item[item.find(b"\x19X")+2:][0:2],
                    "big"
            )
            len_path = int.from_bytes(
                    item[item.find(b"\x19?")+2:][0:2],
                    "big"
            )
            type = item[item.find(b"\x19X")+4:][0:len_type].decode()
            path = item[item.find(b"\x19?")+4:][0:len_path].decode()
            items.append({"type": type, "path": path})
        return items


