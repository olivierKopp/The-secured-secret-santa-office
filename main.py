import time
from utils import *
from nacl.utils import random
from random import shuffle
from nacl.hash import sha256
import nacl

from p2pnetwork.node import Node

class SSSONode(Node):
    # Python class constructor
    def __init__(self, host, port, user, id=None, callback=None, max_connections=0):
        super(SSSONode, self).__init__(host, port, id, callback, max_connections)
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
        print("DATA")
        print(data)
        print(len(data))
        code = data[:4]
        print(code)
        try:
            code = code.decode()
        except:
            pass
        message = data[4:]

        match code:
            case 'pubk':
                if len(self.user.comm_keys) == 0:
                    self.user.comm_keys.append(self.user.public_key_comm)
                self.user.comm_keys.append(message.encode())
            case 'anon':
                self.user.annon_messages.append(message)
            case _:
                print(code)
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
    user.network_node = SSSONode(my_ip_address, 65432, user)
    user.network_node.start()
        
    for ip_address in ip_addresses:
        user.network_node.connect_with_node(ip_address, 65432)
    
    while not len(user.network_node.nodes_inbound) == len(ip_addresses):
        #print(len(user.network_node.nodes_inbound))
        for ip_address in ip_addresses:
            user.network_node.connect_with_node(ip_address, 65432)
        time.sleep(1) # Waiting for everyone to connect before talking
    
    user.network_node.send_to_nodes((b"pubk" + user.public_key_comm))
    
    while len(user.comm_keys) < len(ip_addresses)+1:
        time.sleep(1)

    for c in user.comm_keys:
        print("KEY :",end='')
        print(c)

    user.personal_seed = random()
    user.my_id = random(4)

    id_hash = sha256(user.my_id, encoder=nacl.encoding.HexEncoder)

    shuffle(user.comm_keys)
    anonymous_comm(user, id_hash + user.public_key_choice + user.personal_seed)
    #user.network_node.send_to_nodes((b"anon" + id_hash + user.public_key_choice + user.personal_seed))
    
    
    input()
    user.network_node.stop()


if __name__=='__main__':
    main()