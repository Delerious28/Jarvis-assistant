import socket


def wake_on_lan(mac_address):
    """
    Send a magic packet to wake up a computer on the network.
    
    Parameters:
    mac_address (str): The MAC address of the computer to wake up.
    """
    if len(mac_address) == 17 and mac_address.count(':') == 5:
        pass
    else:
        raise ValueError("Incorrect MAC address format")
    
    mac_address_bytes = bytes.fromhex(mac_address.replace(':', ''))
    magic_packet = b'\xff' * 6 + mac_address_bytes * 16
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, ('<broadcast>', 9))
