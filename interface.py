from datetime import datetime
from bot import BetBot
import eel, json, time

@eel.expose
def handle_login(account):
    with open("accounts.json") as file:
        conta = list(filter(
            lambda x: x['username'] == account['username'],
            json.load(file)))
    if len(conta) == 1 and conta[0]['password'] == account['password']:
        conta = conta[0]
        if conta["license"]['to_date'] < time.time():
            print("Tela de que expirou a licença")
            return False

        conta["license"]['from_date'] = datetime.fromtimestamp(
            conta["license"]['from_date']).strftime('%d/%m/%Y')
        conta["license"]['to_date'] = datetime.fromtimestamp(
            conta["license"]['to_date']).strftime('%d/%m/%Y')
        return conta
    return False

@eel.expose
def operate(account):
    BetBot(account)

eel.init('web')
eel.start('index.html')