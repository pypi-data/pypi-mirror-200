import re

IPv6_PORT = r"^(\[[\d\D]{1,}\]):([0-9]{1,5})$"
IPv6 = r"^(\[[\d\D]{1,}\])$"

IPv4_PORT = r"^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}):([0-9]{1,5})$"
IPv4 = r"^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$"

TLD_PORT = r"^(.*):([0-9]{1,5})$"
TLD = r"^(.*)$"

PATTERNS = [
    IPv6_PORT,
    IPv6,
    IPv4_PORT,
    IPv4,
    TLD_PORT,
    TLD
]

def addr_parser(addr: str, default_port: int):

    for pattern in PATTERNS:
        i = re.findall(pattern, addr)
        if i:
            if isinstance(i[0], str):
                return i[0], default_port

            return i[0][0], int(i[0][1])
