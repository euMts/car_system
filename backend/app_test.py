import unittest
import json

from requests import get, post, delete

class AppTest(unittest.TestCase): # testa a conexão com a api
    token = ""
    def test_0_api_status(self): # status check
        api_response = get("http://localhost:5000")
        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response.json()["status"], "Im alive!!")

    def test_1_register_default(self): # registrar usuario
        data = {
            "username":"firstUser",
            "password":"12345"
            }
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        api_response = post("http://localhost:5000/user/create", data=json.dumps(data), headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test_2_login_default(self): # logar com usuario
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        data = {
            "username":"root",
            "password":"toor"
            }
        api_response = post("http://localhost:5000/user/login", data=json.dumps(data), headers=headers)
        self.assertEqual(api_response.json()["status"], "200")
        self.__class__.token = api_response.json()["access_token"]

    def test_3_delete(self): # deletar usuario
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        api_response = delete("http://localhost:5000/user/delete/2", headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test_4_clients(self): # visualizar clientes
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        api_response = get("http://localhost:5000/clients", headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test_5_client(self): # visualizar cliente
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        api_response = get("http://localhost:5000/client/1", headers=headers)
        self.assertEqual(api_response.json()["status"], "200")
        
    def test_6_client_add(self): # adicionar cliente
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        data = {
            "name":"Matheus Eduardo",
	        "age": 20,
	        "cellphone": "23123213213"
        }
        api_response = post("http://localhost:5000/client/add", data=json.dumps(data), headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test_9_delete_client(self): # deletar cliente
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        api_response = delete("http://localhost:5000/client/delete/4", headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test_8_car_add(self): # adicionar carro
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        data = {
            "color":"yellow",
            "model":"sedan",
            "owner_id":3
            }
        api_response = post("http://localhost:5000/car/add", data=json.dumps(data), headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test_9_delete_car(self): # deletar carro
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        api_response = delete("http://localhost:5000/car/delete/5", headers=headers)
        self.assertEqual(api_response.json()["status"], "200")

    def test__1_car_add(self): # verifica se o limite de 3 carros está funcionando
        headers = {'Authorization' : f'Bearer {self.__class__.token}', 'Content-Type':'application/json'}
        data = {
            "color":"yellow",
            "model":"sedan",
            "owner_id":1
            }
        api_response = post("http://localhost:5000/car/add", data=json.dumps(data), headers=headers)
        self.assertEqual(api_response.json()["status"], "500")

if __name__ == "__main__":
    unittest.main()