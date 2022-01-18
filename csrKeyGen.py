import rsa #Asymetrical Encryption module

#Path where the key goes
path = str(input("Key folder (default is: keys): "))
name = str(input("Key name (if _ it will be saved has the default keys): "))

#Set up public and private keys
(pubkey,privkey) = rsa.newkeys(2048)
print("Generating new keys...")
#Save public key in a file
pukey = open(f'{path}\{name}_publickey.key','wb')
pukey.write(pubkey.save_pkcs1('PEM'))
pukey.close()

#Save Private key in a file
prkey = open(f'{path}\{name}_privatekey.key','wb')
prkey.write(privkey.save_pkcs1('PEM'))
prkey.close()

print(f"\nPrivate .key file need to be saved somewhere securised.")
print("NEVER share your private key to ANYBODY.")