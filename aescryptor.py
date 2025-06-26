#!/usr/bin/env python3

import os
import sys
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

RED, GREEN, YELLOW, RESET = '\033[91m', '\033[92m', '\033[93m', '\033[0m'
backend = default_backend()

def banner():
    os.system("clear")
    print(f"""{GREEN}
    █████╗ ███████╗███████╗     ██████╗██████╗ ██████╗ ████████╗ ██████╗ ██████╗ 
   ██╔══██╗╚══███╔╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
   ███████║  ███╔╝ █████╗      ██║     ██████╔╝██████╔╝   ██║   ██║   ██║██████╔╝
   ██╔══██║ ███╔╝  ██╔══╝      ██║     ██╔═══╝ ██╔═══╝    ██║   ██║   ██║██╔═══╝ 
   ██║  ██║███████╗███████╗    ╚██████╗██║     ██║        ██║   ╚██████╔╝██║     
   ╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝╚═╝     ╚═╝        ╚═╝    ╚═════╝ ╚═╝     
                    {YELLOW}AES-256 File Encryptor • Kali Ready{RESET}
    """)

def derive_key(password, salt):
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=salt, iterations=100000, backend=backend
    ).derive(password.encode())

def encrypt_file(file_path, password):
    salt, iv = os.urandom(16), os.urandom(16)
    key = derive_key(password, salt)

    try:
        data = open(file_path, 'rb').read()
    except FileNotFoundError:
        print(f"{RED}[-] File not found!{RESET}")
        return

    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    ciphertext = cipher.encryptor().update(padded) + cipher.encryptor().finalize()

    open(file_path + '.enc', 'wb').write(salt + iv + ciphertext)
    print(f"{GREEN}[+] Encrypted file saved as: {file_path}.enc{RESET}")

def decrypt_file(enc_path, password):
    try:
        content = open(enc_path, 'rb').read()
    except FileNotFoundError:
        print(f"{RED}[-] Encrypted file not found!{RESET}")
        return

    salt, iv, ciphertext = content[:16], content[16:32], content[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    try:
        padded = cipher.decryptor().update(ciphertext) + cipher.decryptor().finalize()
        data = padding.PKCS7(128).unpadder().update(padded) + padding.PKCS7(128).unpadder().finalize()
    except Exception:
        print(f"{RED}[-] Wrong password or corrupted file.{RESET}")
        return

    out = enc_path.replace('.enc', '.dec')
    open(out, 'wb').write(data)
    print(f"{GREEN}[+] Decrypted file saved as: {out}{RESET}")

def main():
    banner()
    print("1. Encrypt File\n2. Decrypt File\n3. Exit")
    choice = input(f"{YELLOW}Select option: {RESET}")
    if choice == '1':
        encrypt_file(input("Path to file: "), getpass("Password: "))
    elif choice == '2':
        decrypt_file(input("Path to .enc file: "), getpass("Password: "))
    else:
        print("Exiting...")

if __name__ == '__main__':
    main()
