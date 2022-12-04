import time
from utils import *
from pythonp2p import Node
from nacl.utils import random
from nacl.hash import sha256
import nacl

from p2pnetwork.node import Node

class SSSONode (Node):
    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0, user):
        super(MyOwnPeer2PeerNode, self).__init__(host, port, id, callback, max_connections)
        self.user = user

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        code = data[:4]
        message = data[4:]

        match code:
            case 'pubk':
                if len(self.user.comm_keys) == 0:
                    self.user.comm_keys.append(self.user.public_key_comm)
                self.user.comm_keys.append(message)
            case 'anon':
                if len(self.user.comm_keys) == 0:
                    self.user.comm_keys.append(self.user.public_key_comm)
                self.user.comm_keys.append(message)
            case _:
                raise NotImplementedError("Message code unknown")
        print("node_message from " + connected_node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")


def main():
    name = "olivier"         # Get from user
    my_ip_address = "192.168.118.120"   # Get from user
    ip_addresses = ["192.168.118.45"] # Get from user; needed ??
    nb_users = 10     # Get from user

    user = User(name, my_ip_address)

    generate_key_pair(user)
    user.network_node = SSSONode(user)
    user.network_node.start()
        
    for ip_address in ip_addresses:
        user.network_node.connect_with_node(ip_address)
    
    while not len(user.network_node.nodes_inbound) == len(ip_addresses):
        print(len(user.network_node.nodes_inbound))
        for ip_address in ip_addresses:
            user.network_node.connect_to(ip_address)
        time.sleep(1) # Waiting for everyone to connect before talking
    
    print("TEST")
    user.network_node.send_to_nodes({"message":(b"pubk" + user.public_key_comm).decode('latin-1')})

    user.personal_seed = random()
    user.my_id = random(4)

    id_hash = sha256(user.my_id, encoder=nacl.encoding.HexEncoder)

    user.network_node.send_to_nodes({"message":(b"anon" + id_hash + user.public_key_choice + user.personal_seed).decode('latin-1')})
    
    
    time.sleep(10)
    user.network_node.stop()


if __name__=='__main__':
    main()