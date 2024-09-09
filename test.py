from Crypto.Cipher import ARC4
import binascii

def rc4_encrypt(data, key):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def generate_66_char_encrypted_string(input_string):
    key = input_string.encode('utf-8')
    data = input_string.encode('utf-8')
    encrypted_data = rc4_encrypt(data, key)
    while len(encrypted_data) < 66:
        encrypted_data += rc4_encrypt(encrypted_data, key)
    return binascii.hexlify(encrypted_data).decode('utf-8')[:66]
