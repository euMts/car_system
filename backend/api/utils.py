from datetime import datetime

from connection import Connect_with_db
from encrypt import encrypt_str, decrypt_str

# pegar ultimo id
def get_last_id(id_name:str, table_name: str): # cursor normal, funcao independente
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                query = f"SELECT MAX({id_name}) FROM {table_name};"
                cursor.execute(query)
                result = cursor.fetchall()
                Connect_with_db.close_connection(connection)
                return {"status":"200", "message":"Dados retornados com sucesso.", "last_id": int(result[0][0])}
            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao retornar dados.", 
                    "last_id": None
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "last_id": None
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "value": None
            }

# listar todos os clientes
def show_clients(database, connection, cursor, dict_cursor):
    try:
        if connection != None:
            try:
                query = f"SELECT COUNT(client_id) AS number_of_clients FROM clients;"
                cursor.execute(query)
                result = cursor.fetchall()
                all_clients = []
                for x in range(result[0][0]):
                    all_clients.append(show_client_by_id(
                        int(x+1),
                        database=database,
                        connection=connection,
                        cursor=dict_cursor
                        )["value"])
                return {
                    "status":"200", 
                    "message":"Dados retornados com sucesso.", 
                    "value": all_clients
                    }
            except Exception as e:
                print(f"Error at {e}")
                return {
                    "status":"500", 
                    "message":"Erro ao retornar dados.", 
                    "value": None
                    }
        else:
            print(f"Error at {database}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "value": None
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "value": None
            }

# listar um cliente
def show_client_by_id(client_id: int, database, connection, cursor): # cursor dict
    try:
        if connection != None:
            try:
                query = f"SELECT * FROM `carford_car_shop_database`.`clients` WHERE `client_id` = {client_id}"
                cursor.execute(query)
                result = cursor.fetchall()
                client_info = result[0]
                client_info["cars"] = get_cars_by_owner(
                    client_id=client_id, 
                    database=database, 
                    cursor=cursor, 
                    connection=connection
                    )["value"]
                return {
                    "status":"200", 
                    "message":"Dados retornados com sucesso.", 
                    "value": client_info
                    }
            except Exception as e:
                return {
                    "status":"404", 
                    "message":"O usuario nao existe.", 
                    "value": None
                    }
        else:
            print(f"Error at {database}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "value": None
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "value": None
            }

# listar carros de um cliente
def get_cars_by_owner(client_id: int, database, connection, cursor): # cursor dict
    try:
        if connection != None:
            try:
                query = f"SELECT * FROM `carford_car_shop_database`.`cars` WHERE `owner` = {client_id}"
                cursor.execute(query)
                result = cursor.fetchall()
                return {
                    "status":"200", 
                    "message":"Dados retornados com sucesso.", 
                    "value": result
                    }
            except Exception as e:
                print(f"Error at {e}")
                return {
                    "status":"500", 
                    "message":"Erro ao retornar dados.", 
                    "value": []
                    }
        else:
            print(f"Error at {database}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "value": []
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "value": []
            }

# adicionar um cliente
def create_client(name: str, age: int, cellphone: str, database, connection, cursor):
    try:
        if connection != None:
            try:
                date_and_time = datetime.now()
                query = f"""INSERT INTO clients 
                (name, age, cellphone, sale_opportunity, created_at, updated_at)
                VALUES
                ("{name}", {age}, "{cellphone}", 1, "{date_and_time}", "{date_and_time}");"""
                cursor.execute(query)
                cursor.close()
                connection.commit()
                last_id = get_last_id(
                    id_name="client_id",
                    table_name="clients"
                    )["last_id"]
                client = {
                    "client_id":last_id,
                    "name":name,
                    "age":age,
                    "cellphone":cellphone,
                    "sale_opportunity":1,
                    "created_at":date_and_time,
                    "updated_at":date_and_time
                }
                return {
                    "status":"200", 
                    "message":"Cliente criado com sucesso.",
                    "client": client
                    }
            except Exception as e:
                print(f"Error at {e}")
                return {
                    "status":"500", 
                    "message":"Erro ao criar cliente.", 
                    "client": None
                    }
        else:
            print(f"Error at {database}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "client": None
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            "client": None
            }

# adicionar um carro
def create_car(color: str, model: str, owner: int, database, connection, cursor):
    try:
        client_able = check_if_client_is_able(client_id=owner, model=model, color=color)
        update_sale_oportunity(client_id=owner, sale_opportunity=0)
        if connection != None and client_able["client_able"]:
            try:
                date_and_time = datetime.now()
                query = f"""INSERT INTO cars 
                (color, model, owner, created_at, updated_at)
                VALUES
                ("{color}", "{model}", {owner}, "{date_and_time}", "{date_and_time}");"""
                cursor.execute(query)
                cursor.close()
                connection.commit()
                last_id = get_last_id(
                    id_name="car_id",
                    table_name="cars"
                    )["last_id"]
                car = {
                    "car_id":last_id,
                    "color":color,
                    "model":model,
                    "owner":owner,
                    "created_at":date_and_time,
                    "updated_at":date_and_time
                }
                return {
                    "status":"200",
                    "message":"Carro criado com sucesso.",
                    "car": car
                }
            except Exception as e:
                return {
                    "status":"500", 
                    "message":"Erro ao criar carro.", 
                    "car": None
                    }
        else:
            return {
                "status":"500", 
                "message":client_able["reason"], 
                "car": None
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            "car": None
            }

# listar carros de um cliente
def get_cars_from_client(client_id:int): # cursor normal, funcao independente
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                query = f"SELECT COUNT(*) FROM cars WHERE owner = {client_id}"
                cursor.execute(query)
                result = cursor.fetchall()
                Connect_with_db.close_connection(connection)
                return {"status":"200", "message":"Dados retornados com sucesso.", "cars_count": int(result[0][0])}
            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao retornar dados.", 
                    "cars_count": None
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "cars_count": None
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "cars_count": None
            }

# verificar se um cliente esta apto a ter um carro
def check_if_client_is_able(client_id: int, model: str, color: str):
    models = ["hatch", "sedan", "convertible"]
    colors = ["yellow", "blue", "gray"]
    reason = None
    client_able = False
    if model not in models:
        reason = "Este modelo nao e suportado"
        return {
            "client_able": client_able,
            "reason": reason
        }
    elif color not in colors:
        reason = "Esta cor nao e suportada"
        return {
            "client_able": client_able,
            "reason": reason
        }
    elif get_cars_from_client(client_id)["cars_count"] >= 3:
        reason = "Este cliente ja tem 3 carros"
        return {
            "client_able": client_able,
            "reason": reason
        }
    else:
        return {
            "client_able": True,
            "reason": reason
        }

# deletar um cliente por id
def delete_client(client_id: int, database, connection, cursor):
    try:
        if connection != None:
            try:
                delete_all_cars_of_client(client_id)
                query = f"DELETE FROM `clients` WHERE `client_id` = {client_id}"
                cursor.execute(query)
                count = cursor.rowcount
                cursor.close()
                connection.commit()
                if count > 0:
                    return {
                        "status":"200", 
                        "message":"Cliente deletado com sucesso.",
                        }
                else:
                    return {
                        "status":"404", 
                        "message":"Nao existe cliente com esta id",
                        }
            except Exception as e:
                print(f"Error at {e}")
                return {
                    "status":"500", 
                    "message":"Erro ao deletar cliente.", 
                    }
        else:
            print(f"Error at {database}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            }

# deletar todos os carros de um cliente
def delete_all_cars_of_client(client_id: int): # cursor normal, funcao independente
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                update_sale_oportunity(client_id=client_id, sale_opportunity=1)
                query = f"DELETE FROM `cars` WHERE `owner` = {client_id}"
                cursor.execute(query)
                count = cursor.rowcount
                cursor.close()
                connection.commit()
                if count > 0:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"200", 
                        "message":"Carro deletado com sucesso.",
                        }
                else:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"404", 
                        "message":"Nao existe carro com esta id",
                        }
            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao deletar carro.", 
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            }

# deletar apenas um carro
def delete_car(car_id: int, database, connection, cursor):
    try:
        if connection != None:
            try:
                client_id = get_owner_of_a_car(car_id)
                if client_id["owner"] != None:
                    cars_of_owner = get_cars_by_owner(
                        client_id=client_id["owner"],
                        database=database, 
                        cursor=cursor, 
                        connection=connection)
                    if len(cars_of_owner["value"]) <= 1:
                        update_sale_oportunity(client_id=client_id["owner"], sale_opportunity=1)
                query = f"DELETE FROM `cars` WHERE `car_id` = {car_id}"
                cursor.execute(query)
                count = cursor.rowcount
                connection.commit()
                cursor.close()
                if count > 0:
                    return {
                        "status":"200", 
                        "message":"Carro deletado com sucesso.",
                        }
                else:
                    return {
                        "status":"404", 
                        "message":"Nao existe carro com esta id",
                        }
            except Exception as e:
                print(f"Error at {e}")
                return {
                    "status":"500", 
                    "message":"Erro ao deletar carro.", 
                    }
        else:
            print(f"Error at {database}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                }
    except Exception as e:
        print(f"Error at {e}")
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            }

# atualizar possivel comprador
def update_sale_oportunity(client_id: int, sale_opportunity: int):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                query = f"UPDATE `clients` SET sale_opportunity = {sale_opportunity} WHERE `client_id` = {client_id}"
                cursor.execute(query)
                count = cursor.rowcount
                cursor.close()
                connection.commit()
                if count > 0:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"200", 
                        "message":"Tabela atualizada com sucesso.",
                        }
                else:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"404", 
                        "message":"Nao existe cliente com esta id",
                        }
            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao alterar tabela.", 
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            }

# encontrar dono do carro pela id do carro
def get_owner_of_a_car(car_id: int):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                query = f"SELECT `owner` FROM cars WHERE car_id = {car_id}"
                cursor.execute(query)
                result = cursor.fetchall()
                if result != []:
                    Connect_with_db.close_connection(connection)
                    return {"status":"200", "message":"Dados retornados com sucesso.", "owner": int(result[0][0])}
                else:
                    Connect_with_db.close_connection(connection)
                    return {"status":"500", "message":"Erro ao retornar dados.", "owner": None}

            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao retornar dados.", 
                    "owner": None
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "owner": None
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "owner": None
            }

# adicionar um usuario
def create_user(username: str, password: str):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                date_and_time = datetime.now()
                encrypted_password = encrypt_str(password)["text"]
                query = f"""INSERT INTO users 
                (username, password, created_at, updated_at)
                VALUES
                ("{username}", "{encrypted_password}", "{date_and_time}", "{date_and_time}");"""
                cursor.execute(query)
                cursor.close()
                connection.commit()
                last_id = get_last_id(
                    id_name="user_id",
                    table_name="users"
                    )["last_id"]
                user = {
                    "user_id":last_id,
                    "username":username,
                    "password":encrypted_password,
                    "created_at":date_and_time,
                    "updated_at":date_and_time
                }
                Connect_with_db.close_connection(connection)
                return {
                    "status":"200", 
                    "message":"Usuario criado com sucesso.",
                    "user": user
                    }
            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao criar usuario.", 
                    "user": None
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "user": None
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            "user": None
            }

# deletar usuario
def delete_user(user_id: int):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["cursor"]
        if connection != None:
            try:
                query = f"DELETE FROM `users` WHERE `user_id` = {user_id}"
                cursor.execute(query)
                count = cursor.rowcount
                connection.commit()
                cursor.close()
                if count > 0:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"200", 
                        "message":"Usuario deletado com sucesso.",
                        }
                else:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"404", 
                        "message":"Nao existe usuario com esta id",
                        }
            except Exception as e:
                print(f"Error at {e}")
                Connect_with_db.close_connection(connection)
                return {
                    "status":"500", 
                    "message":"Erro ao deletar usuario.", 
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido",
            }

# listar um usuario
def show_user_by_id(user_id: int): # cursor dict
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["dict_cursor"]
        if connection != None:
            try:
                query = f"SELECT * FROM `carford_car_shop_database`.`users` WHERE `user_id` = {user_id}"
                cursor.execute(query)
                result = cursor.fetchall()
                user_info = result[0]
                Connect_with_db.close_connection(connection)
                return {
                    "status":"200", 
                    "message":"Dados retornados com sucesso.", 
                    "value": user_info
                    }
            except Exception as e:
                Connect_with_db.close_connection(connection)
                return {
                    "status":"404", 
                    "message":"O usuario nao existe.", 
                    "value": None
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "value": None
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "value": None
            }

# gerar token
def get_token(user_name: str, user_password: str):
    try:
        database = Connect_with_db.create_connection()
        connection = database["connection"]
        cursor = database["dict_cursor"]
        if connection != None:
            try:
                query = f"SELECT * FROM `carford_car_shop_database`.`users` WHERE `username` = '{user_name}'"
                cursor.execute(query)
                result = cursor.fetchall()
                user_info = result[0]
                if decrypt_str(user_info["password"])["text"].decode() == user_password:
                    Connect_with_db.close_connection(connection)
                    return {
                        "status":"200", 
                        "message":"Usuario autenticado com sucesso.", 
                        "value": user_info
                        }
            except Exception as e:
                Connect_with_db.close_connection(connection)
                return {
                    "status":"404", 
                    "message":"O usuario nao autenticado.", 
                    "value": None
                    }
        else:
            print(f"Error at {database}")
            Connect_with_db.close_connection(connection)
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão com o banco.", 
                "value": None
                }
    except Exception as e:
        print(f"Error at {e}")
        Connect_with_db.close_connection(connection)
        return {
            "status":"500", 
            "message":"Erro desconhecido", 
            "value": None
            }
