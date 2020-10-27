import eel, json, time
from datetime import datetime

@eel.expose
def handle_login(account):
    with open("accounts.json") as file:
        conta = list(filter(
            lambda x: x['username'] == account['username'],
            json.load(file)))
    if len(conta) == 1 and conta[0]['password'] == account['password']:
        conta = conta[0]
        if conta['to_date'] < time.time():
            print("Tela de que expirou a licença")
            return False

        del conta['password']
        conta['from_date'] = datetime.fromtimestamp(conta['from_date']).strftime('%d/%m/%Y')
        conta['to_date'] = datetime.fromtimestamp(conta['to_date']).strftime('%d/%m/%Y')
        return conta
    return False

eel.init('web')
eel.start('index.html')