from crypt_lib import *

enc = Encryptor()
a = enc.encrypt_bytes('abc'.encode('utf8'))
print(a)
dec = Decryptor()
print(dec.decrypt_bytes(a).decode('utf8'))
