from selenium.webdriver.support.ui import WebDriverWait
from widgets import *

class BetBot:
    def __init__(self, config):
        self.config = config
        self.browser = Browser()
        self.fast = WebDriverWait(self.browser, 5)
        self.wait = WebDriverWait(self.browser, 40)

        # Carregar
        self.browser.get("https://www.bet365.com/")
        esperar_sumir(self.wait, ".bl-Preloader_MainHeader")

        # Login
        login(self.wait, config["username"], config["password"])
        tirar_notificacoes(self.browser, self.wait)

        self.banca_inicial = banca(self.fast)
        self.minOdd = self.config["filters"]["minOdd"]
        self.golsFilter = (self.config["filters"]['golsFilter'][1] 
            if self.config["filters"]['golsFilter'][0] else False)
        self.maxBet = self.config["settings"]['maxBet']
        self.percorrer_jogos()

    # def aceitar_aposta():
    #     apertar_botao(self.wait, ".bs-AcceptButton_Text ")

    def percorrer_jogos(self):
        def replace_column(column, casa, fora):
            replaces = lambda x: x.replace("casa", casa).replace("fora", fora)
            if type(column) == list:
                column = [replaces(x) for x in column]
            else: column = replaces(column)
            return column

        jogos = [0]
        num_apostas = 0
        i = 0
        while i < len(jogos) and num_apostas < self.maxBet:
            jogos = devolve_jogos(self.wait)
            jogo = jogos[i]
            i += 1
            
            if filtra_tempo(jogo, self.config["filters"]['maxTime']):
                if self.golsFilter and self.golsFilter != numero_gols(jogo):
                    print("Pulando por número de Gols")
                    continue
                
                try: jogo.click()
                except: 
                    rolar_pagina(self.browser, 300)
                    jogo.click()
                
                try: abrir_opcoes(self.fast)
                except: 
                    self.browser.back()
                    continue
                
                casa, fora = nome_times(self.fast)
                for aposta in self.config['search']:
                    title, column, valor = aposta
                    column = replace_column(column, casa, fora)
                    opcao = procura_opcao(self.fast, title)
                    if not opcao:
                        continue
                    if procura_aposta(opcao, column, self.minOdd):
                        adicionar_valor(self.wait, self.fast, valor)
                        num_apostas += 1
                        if num_apostas > self.maxBet:
                            break
                    time.sleep(7)
                self.browser.back()
        else: 
            print(len(jogos), num_apostas, self.maxBet)
        print("Fim da procura")
