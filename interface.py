import eel, json

@eel.expose
def handle_login(account):
    with open("accounts.json") as file:
        conta = list(filter(
            lambda x: x['username'] == account['username'],
            json.load(file)))
    if len(conta) == 1 and conta[0]['password'] == account['password']:
        return conta[0]
    return False

eel.init('web')
eel.start('index.html')