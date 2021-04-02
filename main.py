import eel, time, threading
from datetime import datetime
from src.database import MongoDB
from src.bot import BetBot

class Updater:
    def __init__(self, account:dict):
        self.MongoDB = MongoDB
        self.account = account

    def update_balance(self, balance:float):
        self.account["license"]['actual_value'] = balance
        if self.account["license"]['original_value'] == -1:
            self.account["license"]['original_value'] = balance
        self.MongoDB.modifica_usuario(self.account, self.account['username'])
        eel.updateBalance(balance)
    def session_gain(balance:float):
        eel.sessionGain(balance)
    def expire_warning():
        eel.expireWarning()

@eel.expose
def handle_login(account:dict):
    conta = MongoDB.login(
        account["username"], account["password"])
    if conta:
        if conta["license"]['to_date'] < time.time():
            Updater.expire_warning()
            return False
        conta['password'] = account["password"]
        conta["license"]['from_date'] = datetime.fromtimestamp(
            conta["license"]['from_date']).strftime('%d/%m/%Y')
        conta["license"]['to_date'] = datetime.fromtimestamp(
            conta["license"]['to_date']).strftime('%d/%m/%Y')
        return conta
    return False

@eel.expose
def operate(account:dict):
    atualizador = Updater(account)
    bot = BetBot(account, atualizador)
    threading.Thread(target=bot.start,
        daemon = True).start()

eel.init('src/web')
eel.start('index.html')