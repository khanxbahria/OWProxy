from .hosts_config import HostsConfig

GAMEHOSTS = {
    "game2.ourworld.com": "35.247.43.97",
    "game3.ourworld.com": "34.83.142.207",
    "game52.ourworld.com": "35.247.19.106",
    "game53.ourworld.com": "34.105.109.230",
}

class Settings:
    gamehost_ip = ""
    hosts_config = HostsConfig(GAMEHOSTS)

    @classmethod
    def set_gamehost(cls, gamehost):
        cls.gamehost_ip = GAMEHOSTS.get(gamehost, cls.gamehost_ip)


