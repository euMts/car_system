import unittest

from api.connection import Connect_with_db


class ConnectionTest(unittest.TestCase): # testa a função de conectar ao banco 
    def test_start_connection(self):
        db = Connect_with_db.create_connection()
        self.assertEqual(db["status"], "200")

    def test_close_connection(self):
        db = Connect_with_db.create_connection()
        close_conn = Connect_with_db.close_connection(db["connection"])
        self.assertEqual(close_conn["status"], "200")

if __name__ == "__main__":
    unittest.main()