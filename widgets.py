from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time, re

# Classes

class Browser(Chrome):
    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--start-maximized")
        
        super().__init__(options = options)

        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """

        Object.defineProperty(navigator, 'webdriver', {

        get: () => undefined

        })

        """
        })

        self.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
        })

# Abstrações
def rolar_pagina(browser, valor):
    browser.execute_script(f"window.scroll(0, window.pageYOffset + {valor})")

def login(wait: WebDriverWait, email: str, password: str):
    apertar_botao(wait, ".hm-MainHeaderRHSLoggedOutWide_Login ")
    preencher_campo(wait, ".lms-StandardLogin_Username ", email)
    preencher_campo(wait, ".lms-StandardLogin_Password ", password)
    apertar_botao(wait, ".lms-StandardLogin_LoginButton ")

def tirar_notificacoes(browser: Chrome, wait: WebDriverWait):
    try:
        browser.switch_to.frame(encontra_elementos(wait, ".lp-UserNotificationsPopup_Frame ")[0])
        apertar_botao(wait, "#remindLater")
        for i in range(2):
            try: apertar_botao(wait, 
                ".pm-PushTargetedMessageOverlay_CloseButton ")
            except: pass
    except: pass

def devolve_jogos(wait: WebDriverWait) -> list:
    return encontra_filhos(encontra_elementos(
        wait, ".him-Classification ")[0], ".him-DetailsTwoWay ")

def filtra_tempo(jogo: WebElement, maximo: int) -> bool:
    try:
        hora_min = encontra_filhos(
            jogo, ".him-InPlayTimer "
        )[0].text
    except: return False

    tempo = int(hora_min.split(":")[0])
    if tempo > maximo:
        print("Passou do tempo requisitado:", maximo)
        return False
    return True

def tirar_aposta(wait: WebDriverWait):
    try: apertar_botao(wait, ".bss-BetslipStandardModule_Minimised .bss-DefaultContent ")
    except: pass
    try:
        apostas = encontra_elementos(wait, ".bss-NormalBetItem_DeleteContainer ")
    except: return
    for aposta in reversed(apostas):
        if encontra_filhos(aposta, ".bss-StakeBox_StakeValue-empty ") != []:
            encontra_filhos(aposta, ".bss-NormalBetItem_Remove")[0].click()
    apertar_botao(wait, ".bss-DefaultContent_Close ")   

def abrir_opcoes(wait: WebDriverWait):
    time.sleep(6)
    terminou = False
    tentativas = 0
    while not terminou and tentativas < 5:
        terminou = True
        botoes = encontra_elementos(wait, '[class="sip-MarketGroupButton "]')
        for botao in botoes:
            try: botao.click()
            except: 
                tirar_aposta(wait)
                terminou = False
                tentativas += 1
                break

def selecionar_info_tabela(opcao: WebElement, info: str, medida: float, 
    minOdd: float, predefined:bool = False) -> WebElement or bool:
    columnName = ".srb-ParticipantLabelCentered " if not predefined else ".srb-ParticipantLabel_Name "
    row = -1
    for index, linha in enumerate(
        encontra_filhos(opcao, columnName)):
        linha = linha.text.lower().strip()
        if medida.lower() == linha:
            # print("Linha encontrada:", medida, linha)
            row = index
    if row == -1: return False

    column = 0
    for index, coluna in enumerate(
        encontra_filhos(opcao, '.gl-MarketColumnHeader ')):
        if index != 0 and info.lower() in coluna.text.lower():
            column = index

    botao =  encontra_filhos(encontra_filhos(
        opcao, ".gl-Market ")[column], ".gl-ParticipantOddsOnly")[row]
    if float(botao.text) > minOdd:
        return botao
    print(f"Odd inferior ao requerido: {float(botao.text)} < {minOdd}")
    return False

def seleciona_info_botoes(
    opcao: WebElement, info: str, minOdd: float) -> WebElement or bool:
    info = re.escape(info).replace("X", "\d").lower()
    for coluna in encontra_filhos(opcao, ".gl-Participant_General "):
        informacao, odd = coluna.text.split("\n")
        if re.match(info, informacao.lower()):
            if float(odd) > minOdd: return coluna
            else:
                print(f"Odd inferior ao requerido: {odd} < {minOdd}")
                break
    return False

def procura_aposta(
    opcao: WebElement, info: str or tuple, minOdd: float) -> bool:
    if type(info) == list:
        coluna, medida = info
        botao = selecionar_info_tabela(opcao, coluna, medida, minOdd)
    elif type(info) == tuple:
        coluna, medida, _ = info
        botao = selecionar_info_tabela(opcao, coluna, medida, minOdd, True)
    else:
        botao = seleciona_info_botoes(opcao, info, minOdd)
    
    if botao: 
        botao.click()
        return True
    return False

def procura_opcao(wait: WebDriverWait, nome: str) -> WebElement or bool:
    nome = re.escape(nome).replace("X", "\d").lower()
    opcoes = encontra_elementos(wait, '.sip-MarketGroup ')
    for opcao in opcoes:
        titulo = encontra_filhos(opcao, '.sip-MarketGroupButton ')[0]
        if re.match(nome, titulo.text.lower()):
            return opcao
    print()
    return False

def adicionar_valor(
    wait: WebDriverWait, fast: WebDriverWait, title:str, valor: float) -> bool:
    atribuiu = False
    try:
        time.sleep(2)
        apertar_botao(fast, ".bss-DefaultContent ")
    except Exception as e: print(e)
    
    try:
        time.sleep(2)
        atribuiu = atribuir_valor(wait, title, valor)
    except Exception as e: print(e)

    try:
        apertar_botao(fast, ".bss-DefaultContent_Close ")
    except Exception as e: print(e)

    return atribuiu

def atribuir_valor(wait: WebDriverWait, title:str, valor: float) -> bool:
    jogadas = encontra_elementos(wait, 
        ".bss-NormalBetItem_ContentWrapper ")
    print(jogadas)
    title = re.escape(title).replace("X", "\d").lower()
    for jogada in reversed(jogadas):
        print(jogada.text.lower())
        if re.match(title, jogada.text.lower()):
            print("Atribuindo valor")
            encontra_filhos(jogada, 
                ".bss-StakeBox_StakeValueInput"
            )[0].send_keys(valor)
            return True
    return False

    entradas = encontra_elementos(wait, ".bss-StakeBox_StakeValueInput")
    for entrada in entradas:
        if entrada.get_attribute("value") == "Valor de Aposta":
            entrada.send_keys(str(valor))
            return True
    return False

# Informações

def abrir_escanteios(wait: WebDriverWait) -> bool:
    for opcao in encontra_elementos(wait, ".ipe-GridHeaderTabLink "):  
        if "Escanteios" in opcao.text: 
            opcao.click()
            return True
    return False

def banca(wait: WebElement) -> float:
    texto_banca = encontra_elementos(
        wait, ".hm-Balance ")[0].text
    print("Banca:", texto_banca)
    return float(texto_banca.strip("R$").replace(",", "."))

def nome_times(wait: WebDriverWait) -> tuple[str]:
    return encontra_elementos(
        wait, ".ipe-EventHeader_Fixture"
    )[0].text.split(" v ")

def numero_gols(jogo: WebElement) -> list[int]:
    lista_gols = encontra_filhos(jogo,
        ".him-StandardScores_Scores "
    )[0].text.split("\n")
    # print("Gols:", " x ".join(lista_gols))
    return list(map(int, lista_gols))

def numero_escanteios(wait: WebDriverWait) -> int:
    texto_escanteios = encontra_elementos(wait, 
        ".sip-MarketGroup_Info ")[0].text
    print(texto_escanteios)
    return int(texto_escanteios.split()[-1])


# Base

def apertar_botao(wait: WebDriverWait, selector: str):
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, selector)
    )).click()

def esperar_sumir(wait: WebDriverWait, selector: str):
    wait.until(EC.invisibility_of_element(
        (By.CSS_SELECTOR, selector)))

def preencher_campo(wait: WebDriverWait, selector: str, valor: str):
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, selector))
    ).send_keys(valor)

def encontra_filhos(element: WebElement, selector: str) -> list[WebElement]:
    return element.find_elements_by_css_selector(selector)

def encontra_elementos(wait: WebDriverWait, selector: str) -> list[WebElement]:
    return wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, selector)))
