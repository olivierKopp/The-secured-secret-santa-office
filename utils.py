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
import rsa


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
        self.annon_messages = []
        self.annon_messages_tmp = []
        
        self.personnal_seed = 0
        self.master_seed = 0
        
        self.network_node = None
        
        self.bits = 1024
        


def generate_key_pair(user):
    (publicKey, privateKey) = rsa.newkeys(user.bits)
    user.private_key_choice = privateKey.save_pkcs1('PEM')
    user.public_key_choice = publicKey.save_pkcs1('PEM')
    
    
    (publicKey, privateKey) = rsa.newkeys(user.bits)
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
    return rsa.encrypt(message, pub_key)
    
def decrypt_message(ciphertext, priv_key):
    try:
        #print("Decryption OK")
        return True,rsa.decrypt(ciphertext, priv_key)
    except:
        print("FAIL TO DECRYPT")
        return False, None
    
def broadcast_message(user, message):
    user.network_node.broadcast(message)

def anonymous_comm(user, message):
    ciphertext = message
    length = (user.bits//8)-11
    for key in user.comm_keys:
        ciphertext = [ciphertext[i:i+length] for i in range(0, len(ciphertext), length)]
        #ciphertext = encrypt_message(ciphertext[0], rsa.PublicKey.load_pkcs1(key))
        ciphertext = [encrypt_message(ciphertext[j], rsa.PublicKey.load_pkcs1(key)) for j in range(0, len(ciphertext))]
        #for c in ciphertext:
        #    print(len(c))
        print(ciphertext)
        ciphertext = b''.join(ciphertext)
        
        #ciphertext = encrypt_message(ciphertext, rsa.PublicKey.load_pkcs1(key))
    user.annon_messages.append(ciphertext)
    print("CIPHERTEXT : ", end='')
    print(ciphertext)
    user.network_node.send_to_nodes({"message" : (b"anon" + ciphertext).decode('latin-1')})
    #broadcast_message(user, b"anon" + ciphertext)