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