import ipaddress


def validate_ipv4(address: str) -> bool:
    try:
        ipaddress.IPv4Network(address)
        return True
    except:
        return False
