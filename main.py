import time
from utils import *
from pythonp2p import Node
from nacl.utils import random
from nacl.hash import sha256


class SSSONode(Node):
    def __init__(self, user):
        self.user = user
        super(self)

    def on_message(self, message, sender, private):
        code = message[:4]
        message = message[4:]

        print(f"Received message with code {code}")

        match code:
            case b'pubk':
                if len(self.user.comm_keys) == 0:
                    self.user.comm_keys.append(self.user.public_key_comm)
                self.user.comm_keys.append(message)
            case b'anon':
                if len(self.user.comm_keys) == 0:
                    self.user.comm_keys.append(self.user.public_key_comm)
                self.user.comm_keys.append(message)
            case _:
                raise NotImplementedError("Message code unknown")


def main():
    name = ""         # Get from user
    my_ip_address = ""   # Get from user
    ip_addresses = [] # Get from user; needed ??
    nb_users = 10     # Get from user

    user = User(name, ip_address)

    generate_key_pair(user)

    user.network_node = SSSONode()

    for ip_address in ip_addresses:
        user.network_node.connect_to(ip_address)
        if len(user.network_node.node_connected) > 0:
            break # We connected to a node, no need to keep on

    while not len(user.network_node.nodes_connected) == len(ip_addresses):
        time.sleep(1) # Waiting for everyone to connect before talking

    user.network_node.send_message(b"pubk" + user.public_key_comm)

    user.personal_seed = random()
    user.my_id = random(4)

    id_hash = sha256(user.my_id, encoder=nacl.encoding.HexEncoder)

    user.network_node.send_message(b"anon" + user.id_hash + user.public_key_choice + user.personal_seed)


if __name__=='__main__':
    main()