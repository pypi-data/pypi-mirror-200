import random, string

__all__ = [
    "ProxyUtils"
]

class ProxyUtils(object):
    def __init__(self):
        self.proxyList = []
    
    def addProxies(self, proxyList: list):
        for v in proxyList:
            self.proxyList.append(v)

    def random_proxy(self):
        return random.choice(self.proxyList)
    
    def get_proxy(self, username, password, host, port):
        proxy = f"{username}:{password}@{host}:{port}"
        return {
            "http": proxy,
            "https": proxy
        }
    
    def new_session_id(self):
        return random.choices(string.ascii_lowercase + string.digits, k=8)
