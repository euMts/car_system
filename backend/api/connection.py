import mysql.connector

class Connect_with_db:
    @staticmethod
    def create_connection():
        try:
            connection = mysql.connector.connect(
                host= "localhost",
                user= "root", 
                password= "toor", 
                database= "carford_car_shop_database",
                port="3306"
                )
            return {
                "status":"200", 
                "message":"Conexão iniciada", 
                "connection":connection, 
                "cursor": connection.cursor(), 
                "dict_cursor": connection.cursor(dictionary=True)
                }
        except Exception as e:
            print(f"Error at {e}")
            return {
                "status":"500", 
                "message":"Erro ao iniciar conexão", 
                "connection": None, 
                "cursor": None,
                "dict_cursor": None
                }

    @staticmethod
    def close_connection(connection):
        try:
            connection.close()
            return {
                "status":"200", 
                "message":"Conexão finalizada."
                }
        except Exception as e:
            print(f"Error at {e}")
            return {
                "status":"500", 
                "message":"Erro ao finalizar conexão"
                }