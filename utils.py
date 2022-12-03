'''
generate/provide key pair
generate random number (ID)
generate a random seed (int)
hash the number
distribute hash+pub_key+seed to everyone

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

class User:
    def __init__(self, ip_addr = "127.0.0.1", name = ""):
        self.my_id = ""
        self.my_ip = ip_addr
        self.my_name = name
        self.private_key_choice = None
        self.public_key_choice = None
        self.private_key_comm = None
        self.public_key_comm = None
        self.personnal_seed = 0
        self.master_seed = 0
        

from cryptography.hazmat.primitives.asymmetric import ec


def generate_key_pair(user, curve = ec.SECP384R1()):
    user.private_key_choice = ec.generate_private_key(curve)
    user.public_key_choice = private_key.public_key()
    user.private_key_comm = ec.generate_private_key(curve)
    user.public_key_comm = private_key.public_key()


def encrypt_message(message, key):
    
    
def broadcast_message(sockets, message):
    for s in sockets:
        

def anonymous_comm()