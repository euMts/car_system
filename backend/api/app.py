from flask import Flask, Response, request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from datetime import datetime
import json
from dotenv import load_dotenv
from pathlib import Path
import os

from connection import Connect_with_db
from utils import (
    show_clients, 
    show_client_by_id,
    create_client, 
    create_car, 
    delete_client, 
    delete_car,
    get_token,
    create_user,
    delete_user
    )

dotenv_path = Path('./backend/api/SECRET.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)
secret = os.getenv("SECRET_KEY")
if secret == None: # variável de ambiente só está configurada com DOCKER
    secret = "b+sIrZ+Lk1AvpG8M2PkR6WtG9MNHhsLzargmzLiepLo="
app.config["JWT_SECRET_KEY"] = secret
jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def root():
    return {
        "status":"Im alive!!",
        "datetime":datetime.now()
    }

@app.route("/user/login", methods=["POST"])
def login_user():
    try:
        body = request.get_json()
        user = get_token(
            user_name=body["username"],
            user_password=body["password"],
            )
        access_token = create_access_token(identity=body["username"])
        user["access_token"] = access_token
        return Response(json.dumps(user, indent=4, default=str), int(user["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/create_client_route() - Error at {e}")
        return Response(json.dumps({"message":"Usuário não encontrado"}), 401, {'ContentType':'application/json'})

@app.route("/user/create", methods=["POST"])
def create_user_route():
    try:
        body = request.get_json()
        user = create_user(
            username=body["username"],
            password=body["password"],
            )
        return Response(json.dumps(user, indent=4, default=str), int(user["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/create_client_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 401, {'ContentType':'application/json'})

@app.route("/user/delete/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    try:
        user = delete_user(
            user_id=user_id
            )
        return Response(json.dumps(user, indent=4, default=str), int(user["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/delete_client_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

@app.route("/clients", methods=["GET"])
@jwt_required()
def show_clients_route():
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        dict_cursor = database["dict_cursor"]
        clients = show_clients(
            database=database,
            connection=connection,
            cursor=cursor,
            dict_cursor=dict_cursor
            )
        Connect_with_db.close_connection(connection)
        return Response(json.dumps(clients, indent=4, default=str), int(clients["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/show_clients_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

@app.route("/client/<client_id>", methods=["GET"])
@jwt_required()
def show_client_by_id_route(client_id):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        dict_cursor = database["dict_cursor"]
        client = show_client_by_id(
            client_id=client_id,
            database=database,
            connection=connection,
            cursor=dict_cursor
            )
        Connect_with_db.close_connection(connection)
        return Response(json.dumps(client, indent=4, default=str), int(client["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/show_client_by_id_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

@app.route("/client/add", methods=["POST"])
@jwt_required()
def create_client_route():
    try:
        body = request.get_json()
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        client = create_client(
            name=body["name"],
            age=body["age"],
            cellphone=body["cellphone"],
            database=database,
            connection=connection,
            cursor=cursor
            )
        Connect_with_db.close_connection(connection)
        return Response(json.dumps(client, indent=4, default=str), int(client["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/create_client_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

@app.route("/client/delete/<client_id>", methods=["DELETE"])
@jwt_required()
def delete_client_route(client_id):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        client = delete_client(
            client_id=client_id,
            database=database,
            connection=connection,
            cursor=cursor
            )
        Connect_with_db.close_connection(connection)
        return Response(json.dumps(client, indent=4, default=str), int(client["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/delete_client_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

@app.route("/car/add", methods=["POST"])
@jwt_required()
def create_car_route():
    try:
        body = request.get_json()
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        car = create_car(
            color=body["color"],
            owner=body["owner_id"],
            model=body["model"],
            database=database,
            connection=connection,
            cursor=cursor
            )
        Connect_with_db.close_connection(connection)
        return Response(json.dumps(car, indent=4, default=str), int(car["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/create_car_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

@app.route("/car/delete/<car_id>", methods=["DELETE"])
@jwt_required()
def delete_car_route(car_id):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        car = delete_car(
            car_id=car_id,
            database=database,
            connection=connection,
            cursor=cursor
            )
        Connect_with_db.close_connection(connection)
        return Response(json.dumps(car, indent=4, default=str), int(car["status"]), {'ContentType':'application/json'})
    except Exception as e:
        print(f"app.py/delete_car_route() - Error at {e}")
        return Response(json.dumps({"message":"Algo deu errado"}), 500, {'ContentType':'application/json'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)