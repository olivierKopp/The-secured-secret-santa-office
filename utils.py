'''
generate/provide key pair
share public key for anonymous comm
generate random number (ID)
generate a random seed (int)
hash the number
distribute hash+pub_key+seed to everyone + HMAC later

Receive all tuple
compile all seed to master seed
compile tuple in array (deterministically with the seed)
send results to everyone
check received results
If there is an error => restart

get my position in the array
generate a derangement with the seed
encrypt my name with the public key corresponding to my previous position
send it to everyone

receive all ciphertext
try to decrypt everything
if none/more than one work => restart
else the decrypted name is your pick => wipe the key pair


1. comm anonymous
2. generate key
3. generate seed
3b. compile all seeds
4. generate ID
5. shuffle deterministic
6. encryption/decryption
7. generate derangement
'''
from Crypto.PublicKey import ECC


class User:
    def __init__(self, ip_addr = "127.0.0.1", name = ""):
        self.my_id = ""
        self.my_ip = ip_addr
        self.my_name = name
        self.private_key_choice = None
        self.public_key_choice = None
        self.private_key_comm = None
        self.public_key_comm = None
        self.comm_keys = []
        
        self.personnal_seed = 0
        self.master_seed = 0
        
        self.network_node = None
        


def generate_key_pair(user, bits = 8196):
    (publicKey, privateKey) = rsa.newkeys(bits)
    user.private_key_choice = privateKey.save_pkcs1('PEM')
    user.public_key_choice = publicKey.save_pkcs1('PEM')
    
    
    (publicKey, privateKey) = rsa.newkeys(bits)
    user.private_key_comm = privateKey.save_pkcs1('PEM')
    user.public_key_comm = publicKey.save_pkcs1('PEM')
    print("comm keys : ")
    print(user.private_key_comm)
    print(user.public_key_comm)
    print("choice keys : ")
    print(user.private_key_choice)
    print(user.public_key_choice)

#def loadKeys(pub_key, priv_key):
#    return rsa.PublicKey.load_pkcs1(pub_key), rsa.PrivateKey.load_pkcs1(priv_key)

def encrypt_message(message, pub_key):
    return rsa.encrypt(message.encode('utf-8'), pub_key)
    
def decrypt_message(ciphertext, priv_key):
    try:
        return rsa.decrypt(ciphertext, priv_key).decode('utf-8')
    except:
        return False
    
def broadcast_message(user, message):
    user.network_node.broadcast(message)

def anonymous_comm(keys, message):
    ciphertext = message
    for key in keys:
        ciphertext = encrypt_message(ciphertext, rsa.PublicKey.load_pkcs1(pub_key))
    broadcast_message(b"anon" + ciphertext)