from selenium.webdriver.support.ui import WebDriverWait
from src.widgets import *

class BetBot:
    def __init__(self, config: dict, Updater: object):
        self.config = config
        self.browser = ChromeBrowser()
        self.fast = WebDriverWait(self.browser, 5)
        self.wait = WebDriverWait(self.browser, 30)

        # Carregar
        self.browser.get("https://www.bet365.com/")
        esperar_sumir(self.wait, ".bl-Preloader_MainHeader")

        # Login
        login(self.wait, config["username"], config["password"])
        time.sleep(2)
        del config["password"]
        
        try: self.pegar_banca()
        except: self.pegar_banca()
        # Updater.update_balance(self.banca_inicial)

        self.saldo = 0
        self.minOdd = self.config["filters"]["minOdd"]
        self.golsFilter = (self.config["filters"]['golsFilter'][1] 
            if self.config["filters"]['golsFilter'][0] else False)
        self.maxBet = self.config["settings"]['maxBet']
        self.num_apostas = 0
        print("Vou começar a percorrer")
        self.start()

    def pegar_banca(self):
        tirar_notificacoes(self.browser, self.fast, self.wait)
        self.banca_inicial = banca(self.fast)

    def start(self):
        while self.num_apostas < self.maxBet and not self.bateu_stop():
            try:
                self.percorrer_jogos()
            except KeyboardInterrupt: pass
            time.sleep(600)
            apertar_botao(self.fast, ".hm-MainHeaderLogoWide_Bet365LogoImage ")

    def bateu_stop(self) -> bool:
        if (self.saldo > self.config["settings"]["stopWin"] or
            self.saldo > self.config["settings"]["stopLoss"]):
            return True
        return False

    def percorrer_jogos(self):
        def apostar():
            apertar_botao(self.fast, ".bss-DefaultContent ")
            efetuado, encontrou = 0, []
            while efetuado < 3 and encontrou == []:
                encontrou = self.browser.find_elements_by_css_selector(
                    ".bss-PlaceBetButton_Wrapper ")
                efetuado += 1
                try: 
                    apertar_botao(self.fast, ".bs-AcceptButton ")
                    apertar_botao(self.fast, ".bss-PlaceBetButton_Wrapper ")
                    efetuado = 3
                except: pass
                if encontrou == []: time.sleep(0.1)
            apertar_botao(self.fast, ".bss-ReceiptContent_Done ")

        def replace_team_names(column: list or str, casa: str, fora: str) -> str or list:
            replaces = lambda x: x.replace("casa", casa).replace("fora", fora)
            if type(column) == list:
                column = [replaces(x) for x in column]
            else: column = replaces(column)
            return column

        def tradutor(title:str, opcao:str) -> str:
            if re.search(re.escape("Hora do Xº Gol"), title):
                title = "Momento do Próximo Gol"
            elif re.search(re.escape("Resultado do Jogo"), title):
                title = "Minutos - Resultado"
            elif re.search(re.escape("Próximos 10 Minutos"), title):
                title = (f"10 Minutos - Escanteios" if opcao == "Escanteios" 
                    else "Gols em Dez Minutos")
            elif re.search(re.escape("Handicap"), title):
                title = "Handicap Asiático"
            elif re.search(re.escape("- Golos"), title):
                title = ("Time da Casa - Gols" if title.split()[0] == "casa" 
                    else "Time Visitante - Gols")
            elif title == "Escanteios":
                title = "Próximo Escanteio"
            elif title == "Resultado do Jogo - Tempo":
                title = "Minutos - Resultado"
            elif title == "1ª Parte - Gols +/- (X-X)":
                title = "tempo - gols +/-"
            return title

        jogos, selecionadas, i = [0], 0, 0
        while i < len(jogos) and selecionadas < self.maxBet:
            apertar_botao(self.fast, ".hm-MainHeaderLogoWide_Bet365LogoImage ")
            jogos = devolve_jogos(self.wait)
            if i >= len(jogos): continue
            jogo = jogos[i]
            i += 1
            
            if filtra_tempo(jogo, self.config["filters"]['maxTime']):
                if self.golsFilter and self.golsFilter != numero_gols(jogo):
                    continue
                
                try: jogo.click()
                except Exception as e: 
                    print(type(e), e)
                    rolar_pagina(self.browser, 300)
                    jogo.click()
                
                try: abrir_opcoes(self.fast)
                except Exception as e: 
                    continue
                
                casa, fora = nome_times(self.fast)
                for aposta in self.config['search']:
                    title, column, value, search = aposta
                    titleT = replace_team_names(title, casa, fora)
                    column = replace_team_names(column, casa, fora)

                    opcao = procura_opcao(self.fast, titleT)
                    if not opcao:
                        continue
                    try:
                        aposta = procura_aposta(
                        opcao, column, self.minOdd, search)
                    except: continue
                    if aposta:
                        title = tradutor(title, column[1])
                        adicionar_valor(
                            self.wait, self.fast, title, value)
                        tirar_aposta(self.fast)
                        selecionadas += 1
                        if selecionadas >= self.maxBet:
                            break
                    time.sleep(7)
                if selecionadas > 0: time.sleep(15)
        tirar_aposta(self.fast)
        if selecionadas > 0:
            self.num_apostas += selecionadas
            if selecionadas == 1:
                apertar_botao(self.fast, ".qbs-AcceptButton ")
            else: apostar()
            apertar_botao(self.fast, ".hm-HeaderMenuItemMyBets ")
        print("Fim do programa")