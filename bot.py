from selenium.webdriver.support.ui import WebDriverWait
from widgets import *

email = "testlearnbet"
senha = "1231231414"

browser = Browser()
fast = WebDriverWait(browser, 5)
wait = WebDriverWait(browser, 40)

# Carregar
browser.get("https://www.bet365.com/")
esperar_sumir(wait, ".bl-Preloader_MainHeader")

# Login
login(wait, email, senha)
tirar_notificacoes(browser, wait)
banca_inicial = banca(fast)

# def aceitar_aposta():
#     apertar_botao(wait, ".bs-AcceptButton_Text ")

def percorrer_jogos(requerimentos):
    jogos = [0]
    num_apostas = 0
    i = 0
    while i < len(jogos) and num_apostas < requerimentos['maximo']:
        jogos = devolve_jogos(wait)
        jogo = jogos[i]
        i += 1
        
        if filtra_tempo(jogo, requerimentos['tempo']):
            gols = requerimentos['filtro_gols']
            if gols and gols != numero_gols(jogo):
                continue
            
            try: jogo.click()
            except: jogo.click()
            
            try: abrir_opcoes(fast)
            except: 
                browser.back()
                continue

            for aposta in requerimentos['apostas']:
                title, column, valor = aposta
                opcao = procura_opcao(fast, title)
                if not opcao:
                    continue
                if procura_aposta(opcao, column):
                    adicionar_valor(wait, fast, valor)
                    num_apostas += 1
                    if num_apostas > requerimentos['maximo']:
                        break
            browser.back()

requerimentos = {
    "stopwin": 10,
    "stoploss": 10,
    "gales": 2,
    "filtro_gols": [0, 0],
    "tempo": 45,
    "apostas": [
        ["Partida - Gols", ("mais de", "1.5"), 10],
        ["Gols +/-", ("mais de", "2.5"), 5],
        ["Próximos 10 Minutos", ("mais de", "Escanteios"), 3]
    ],
    "maximo": 6 # 20 é o máximo
}

percorrer_jogos(requerimentos)