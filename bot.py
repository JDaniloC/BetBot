from selenium.webdriver.support.ui import WebDriverWait
from widgets import *

class BetBot:
    def __init__(self, config):
        self.config = config
        self.browser = Browser()
        self.fast = WebDriverWait(self.browser, 5)
        self.wait = WebDriverWait(self.browser, 30)

        # Carregar
        self.browser.get("https://www.bet365.com/")
        esperar_sumir(self.wait, ".bl-Preloader_MainHeader")

        # Login
        login(self.wait, config["username"], config["password"])
        tirar_notificacoes(self.browser, self.wait)

        self.banca_inicial = banca(self.fast)
        self.saldo = 0
        self.minOdd = self.config["filters"]["minOdd"]
        self.golsFilter = (self.config["filters"]['golsFilter'][1] 
            if self.config["filters"]['golsFilter'][0] else False)
        self.maxBet = self.config["settings"]['maxBet']
        self.num_apostas = 0

    def start(self):
        try:
            while self.num_apostas < self.maxBet and not self.bateu_stop():
                self.percorrer_jogos()
                time.sleep(600)
                apertar_botao(self.fast, ".hm-MainHeaderLogoWide_Bet365LogoImage ")
        except KeyboardInterrupt:
            pass
        print("Fim da operação")

    def bateu_stop(self):
        if (self.saldo > self.config["settings"]["stopWin"] or
            self.saldo > self.config["settings"]["stopLoss"]):
            return True
        return False

    def percorrer_jogos(self):
        def apostar():
            apertar_botao(self.fast, ".bss-DefaultContent ")
            apertar_botao(self.fast, ".bs-AcceptButton ")
            apertar_botao(self.fast, ".bss-PlaceBetButton_Wrapper ")
            apertar_botao(self.fast, ".bs-ReceiptContent_Done ")

        def replace_team_names(column, casa, fora):
            replaces = lambda x: x.replace("casa", casa).replace("fora", fora)
            if type(column) == list:
                column = [replaces(x) for x in column]
            else: column = replaces(column)
            return column

        jogos = [0]
        i = 0
        selecionadas = 0
        while i < len(jogos) and selecionadas < self.maxBet:
            jogos = devolve_jogos(self.wait)
            if i >= len(jogos): continue
            jogo = jogos[i]
            i += 1
            
            if filtra_tempo(jogo, self.config["filters"]['maxTime']):
                if self.golsFilter and self.golsFilter != numero_gols(jogo):
                    print("Pulando por número de Gols")
                    continue
                
                try: jogo.click()
                except Exception as e: 
                    print(e)
                    rolar_pagina(self.browser, 300)
                    jogo.click()
                
                try: abrir_opcoes(self.fast)
                except Exception as e: 
                    continue
                
                casa, fora = nome_times(self.fast)
                for aposta in self.config['search']:
                    title, column, valor = aposta
                    title = replace_team_names(title, casa, fora)
                    column = replace_team_names(column, casa, fora)
                    if len(column) == 3: column = tuple(column)
                    opcao = procura_opcao(self.fast, title)
                    if not opcao:
                        continue
                    if procura_aposta(opcao, column, self.minOdd):
                        adicionar_valor(self.wait, self.fast, title, valor)
                        tirar_aposta(self.fast)
                        selecionadas += 1
                        if selecionadas >= self.maxBet:
                            break
                    time.sleep(7)
                apertar_botao(self.fast, ".hm-MainHeaderLogoWide_Bet365LogoImage ")
        if selecionadas > 0:
            self.num_apostas += selecionadas
            apostar()
        print("Fim")