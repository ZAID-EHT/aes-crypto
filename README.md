# 🔐 AES-Cryptor

A terminal-based AES-256 file encryption tool for Kali Linux & other distros.

## Features
- AES-256 CBC encryption
- PBKDF2 password-based key generation
- Encrypts/Decrypts any file format
- Kali-style colored UI

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/aes-cryptor.git
cd aes-cryptor
chmod +x *.sh *.py
./aescryptor.sh
## Installation Tronuleshooting
#Step 1 - sudo apt-get install dos2unix
#step 2 - dos2unix aescryptor.sh
dos2unix aescryptor.py
 or
sed -i 's/\r$//' aescryptor.sh
sed -i 's/\r$//' aescryptor.py
#step 3 - ./aescryptor.sh
#bonus - chmod +x aescryptor.sh aescryptor.py



