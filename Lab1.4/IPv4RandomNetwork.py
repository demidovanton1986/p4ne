import ipaddress
import random


class IPv4RandomNetwork(ipaddress.IPv4Network):
    def __init__(self):
        net = random.randint(0x0B000000, 0xDF000000)
        mask = random.randint(8, 24)
        ipaddress.IPv4Network.__init__(self, (net, mask), strict=False)
