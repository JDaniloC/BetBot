from pymongo import MongoClient
from env import autenticacao
import time, hashlib

users_schema = {
    "username": "",
    "password": "",
    "license": {
        "from_date": 0,
        "to_date": 0,
        "original_value": 0.0, 
        "actual_value": 0.0
    },
    "settings": {
        "stopWin": 0,
        "stopLoss": 0,
        "maxBet": 1,
        "maxGales": 0
    },
    "filters": {
        "golsFilter": [False, [0, 0]],
        "maxTime": 90,
        "minOdd": 0.0
    },
    "search": []
}
def criptografa(password):
    return hashlib.md5(password.encode("utf-8")).hexdigest()

class Mongo:
    def __init__(self, database, users_collection):
        self.database = database
        self.Users_collection = users_collection

    def cadastrar(self, username, password):
        '''
        Adiciona um novo usuário
        '''
        user = users_schema
        user['username'] = username
        user['password'] = criptografa(password)
        user['license']['from_date'] = time.time()
        user['license']['to_date'] = time.time() + 2592000
        user["_id"] = time.time()
        self.Users_collection.insert_one(user)

    def renovar_licenca(self, username):
        '''
        Aumenta a licença de determinado usuário
        '''
        data = time.time() + 2592000
        self.Users_collection.find_one_and_update(
            {'username':username}, {'$set': {
                'license.to_date': data,
        }})

    def modifica_usuario(self, info, username):
        '''
        Modifica as informações do usuário de determinado usuário
        '''
        user = self.remover_usuario(username)
        user.update(info)
        self.Users_collection.insert_one(user)

    def remover_usuario(self, username):
        '''
        Remove o usuário de determinado username
        Devolve o usuário removido
        '''
        return self.Users_collection.find_one_and_delete(
            {'username': username})

    def login(self, username, password):
        '''
        Devolve as informações do usuário a partir do nome do usuário
        '''
        user = self.Users_collection.find_one({'username': username})
        if user and user['password'] == criptografa(password):
            return user
        return False

    def modificar_banco_users(self, opcao):
        if opcao == "clear":
            self.Users_collection.delete_many({})
        elif opcao == "time":
            data = time.time() + 2592000
            self.Users_collection.update_many(
                {}, {'$set': {'timestamp': data}})

client =  MongoClient(autenticacao)
Database = client.betbot 
Users_collection = Database.users

MongoDB = Mongo(Database, Users_collection)