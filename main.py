import time
from utils import *
from nacl.utils import random
from random import shuffle
from nacl.hash import sha256
import nacl
from random import seed
from base64 import b64encode, b64decode

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
        data = data["message"]
        try:
            data = data.encode()
        except:
            pass
        code = data[:4]
        try:
            code = code.decode()
        except:
            pass
        message = data[4:]

        match code:
            case 'pubk':
                self.user.comm_keys.append(message)
                if len(self.user.comm_keys) == 1:
                    self.user.comm_keys.append(self.user.public_key_comm)
            case 'anon':
                self.user.annon_messages.append(message)
            case 'conf':
                split_msg = message.split(b':')
                if((split_msg[0], split_msg[1], split_msg[3]) not in self.user.ids):
                    print("RECEIVED")
                    print(split_msg[1])
                    print(b64decode(split_msg[1]))
                    self.user.ids.append((split_msg[0], split_msg[1], split_msg[3]))
                    self.user.seeds.append(split_msg[2])
                    self.user.annon_messages.append(message)
            case 'seed':
                assert self.user.master_seed == message
            case 'chse':
                if(message not in self.user.choices):
                    self.user.choices.append(message)
            case _:
                print(code)
                raise NotImplementedError("Message code unknown")
        #print("node_message from " + connected_node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")


def main():
    name = "olivier"         # Get from user
    my_ip_address = "192.168.118.120"   # Get from user
    ip_addresses = ["192.168.118.45", "192.168.118.154"] # Get from user; needed ??
    nb_users = len(ip_addresses)+1

    user = User(name, my_ip_address)

    generate_key_pair(user)
    user.network_node = SSSONode(my_ip_address, 65432, user)
    user.network_node.start()
    print("SENT")
    print(user.public_key_choice)
    print(b64encode(user.public_key_choice))
    for ip_address in ip_addresses:
        user.network_node.connect_with_node(ip_address, 65432)
    
    count = 0
    while not len(user.network_node.nodes_outbound) == len(ip_addresses) and count < 5:
        print(len(user.network_node.nodes_outbound))
        for ip_address in ip_addresses:
            user.network_node.connect_with_node(ip_address, 65432)
        time.sleep(1) # Waiting for everyone to connect before talking
        count += 1
    
    #waiting for everyone to share their pub key
    '''user.network_node.send_to_nodes({"message" : (b"pubk" + user.public_key_comm).decode()})
    while len(user.comm_keys) < len(ip_addresses)+1:
        user.network_node.send_to_nodes({"message" : (b"pubk" + user.public_key_comm).decode()})
        time.sleep(1)
    '''
    user.personal_seed = random()
    user.seeds.append(user.personal_seed)
    user.my_id = random(4)

    id_hash = sha256(user.my_id, encoder=nacl.encoding.HexEncoder)
    user.ids.append((id_hash, user.public_key_choice, name.encode()))

    #shuffle(user.comm_keys)
    #send id + pubk + seed anonymously
    #anonymous_comm(user, id_hash + user.public_key_choice + user.personal_seed)
    payload = b"conf" + id_hash + b":" + b64encode(user.public_key_choice) + b":" + user.personal_seed + b":" + name.encode()
    user.network_node.send_to_nodes({"message" : (payload).decode('latin-1')})
    
    print(len(user.network_node.nodes_outbound))
    while(len(user.seeds) < nb_users):
        user.network_node.send_to_nodes({"message" : payload.decode('latin-1')})
        time.sleep(1)
        
    user.master_seed = compile_seeds(user.seeds)
    seed(int.from_bytes(user.master_seed[:4], 'big'))
    
    shuffle(user.ids)
    
    user.network_node.send_to_nodes({"message":b"seed" + user.master_seed})
    
    position = -1
    for i in range(len(user.ids)):
        if(id_hash == user.ids[i][0]):
            position = i
            break
            
    if(position == -1):
        print("ERROR OCCURED")
        exit(-1)
        
    derangement = random_derangement(nb_users)
    pos_to_choose = derangement[position]
    key_to_use = user.ids[pos_to_choose][1]
    
    c = b64encode(encrypt_message(user.my_id, rsa.PublicKey.load_pkcs1(b64decode(key_to_use))))
    #sign the message
    #TODO
    user.network_node.send_to_nodes({"message" : (b"chse" + c).decode("latin-1")})
    user.choices.append(c)
    
    while len(user.choices) < nb_users:
        time.sleep(1)
        user.network_node.send_to_nodes({"message" : (b"chse" + c).decode("latin-1")})
    
    for cipher in user.choices:
        status,plain = decrypt_message(b64decode(cipher), rsa.PrivateKey.load_pkcs1(user.private_key_choice))
        if status:
            user.final_id = plain
            break
    final_id_hash = sha256(user.final_id, encoder=nacl.encoding.HexEncoder)
    sig_key_check = None
    for i in range(len(user.ids)):
        if(final_id_hash == user.ids[i][0]):
            sig_key_check = user.ids[i][1]
            break
    if(sig_key_check == None):
        exit(-1)
    #check signature
    #TODO
    print("FINAL RESULT : ", end='')
    print(final_id_hash)
    for i in user.ids:
        if(i[0] == final_id_hash):
            print(b"You have to give a gift to " + i[2])
    print(id_hash)
        
    user.network_node.stop()


if __name__=='__main__':
    main()