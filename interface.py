import eel, json, time, threading
from datetime import datetime
from database import MongoDB
from bot import BetBot

class Updater:
    def __init__(self):
        self.MongoDB = MongoDB
        self.account = {}

    def update_balance(self, balance):
        self.account["license"]['actual_value'] = balance
        self.MongoDB.modifica_usuario(self.account)
        eel.updateBalance(balance)
    def session_gain(balance):
        eel.sessionGain(balance)
    def expire_warning():
        eel.expireWarning()

@eel.expose
def handle_login(account):
    conta = MongoDB.login(account["username"], account["password"])
    if conta:
        if conta["license"]['to_date'] < time.time():
            Updater.expire_warning()
            return False

        conta["license"]['from_date'] = datetime.fromtimestamp(
            conta["license"]['from_date']).strftime('%d/%m/%Y')
        conta["license"]['to_date'] = datetime.fromtimestamp(
            conta["license"]['to_date']).strftime('%d/%m/%Y')
        return conta
    return False

@eel.expose
def operate(account):
    bot = BetBot(account, Updater)
    Updater.account = account
    threading.Thread(target=bot.start,
        daemon = True).start()

eel.init('web')
eel.start('index.html')