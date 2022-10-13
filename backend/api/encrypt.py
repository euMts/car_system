from dotenv import load_dotenv
from pathlib import Path
import os
from cryptography.fernet import Fernet

def encrypt_str(my_text: str):
    try:
        dotenv_path = Path('./backend/api/SECRET.env')
        load_dotenv(dotenv_path=dotenv_path)

        secret_key = os.getenv("SECRET_KEY")
        if secret_key == None: # variável de ambiente só está configurada com DOCKER
            secret_key = "b+sIrZ+Lk1AvpG8M2PkR6WtG9MNHhsLzargmzLiepLo="
        cipher_suite = Fernet(secret_key)
        ciphered_text = cipher_suite.encrypt(str.encode(my_text))   

        return {"text":ciphered_text.decode()}
    except Exception as e:
        print(e)

def decrypt_str(my_text):
    try:
        dotenv_path = Path('./backend/api/SECRET.env')
        load_dotenv(dotenv_path=dotenv_path)

        secret_key = os.getenv("SECRET_KEY")
        if secret_key == None: # variável de ambiente só está configurada com DOCKER
            secret_key = "b+sIrZ+Lk1AvpG8M2PkR6WtG9MNHhsLzargmzLiepLo="
        cipher_suite = Fernet(secret_key)

        unciphered_text = (cipher_suite.decrypt(my_text.encode()))

        return {"text":unciphered_text}
    except Exception as e:
        print(e)

if __name__ == "__main__":
    a = encrypt_str("toor")["text"]
    # print(encrypt_str("toor"))
    print(a)
    print(decrypt_str(a.encode()))