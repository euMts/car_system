import unittest

from api.encrypt import decrypt_str, encrypt_str

class EncryptTest(unittest.TestCase): # testa a função de encriptar as senhas 
    def test_encrypt_str(self):
        my_string = "toor"
        my_string_encrypted = encrypt_str(my_string)["text"]
        my_string_decrypted = decrypt_str(my_string_encrypted)["text"].decode()
        self.assertEqual(my_string, my_string_decrypted)

if __name__ == "__main__":
    unittest.main()