from selenium.webdriver import FirefoxProfile, Firefox, DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver.v2 as Browser_uc
from selenium.webdriver.common.by import By
from typing import Tuple, List
import time, re

# Classes
class FirefoxBrowser(Firefox):
    def __init__(self):
        profile = FirefoxProfile()
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        super().__init__(firefox_profile=profile, desired_capabilities=desired)

ChromeBrowser = Browser_uc.Chrome

# Abstrações
def rolar_pagina(browser: Firefox, valor: int):
    browser.execute_script(f"window.scroll(0, window.pageYOffset + {valor})")

def login(wait: WebDriverWait, email: str, password: str):
    apertar_botao(wait, ".hm-MainHeaderRHSLoggedOutWide_Login ")
    preencher_campo(wait, ".lms-StandardLogin_Username ", email)
    preencher_campo(wait, ".lms-StandardLogin_Password ", password)
    apertar_botao(wait, ".lms-StandardLogin_LoginButton ")

def tirar_notificacoes(browser: Firefox, fast: WebDriverWait, wait: WebDriverWait):
    try:
        browser.switch_to.frame(encontra_elementos(wait, ".lp-UserNotificationsPopup_Frame ")[0])
        apertar_botao(wait, "#remindLater")
        try: 
            for _ in range(2):
                apertar_botao(fast, ".pm-PushTargetedMessageOverlay_CloseButton ")
                break
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
            try: encontra_filhos(aposta, ".bss-NormalBetItem_Remove")[0].click()
            except: pass
    try: apertar_botao(wait, ".bss-DefaultContent_Close ")   
    except: apertar_botao(wait, ".bsm-BetslipStandardModule_Overlay ")

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

def selecionar_info_tabela(opcao: WebElement, info: str, medida: str, 
    minOdd: float, search:str) -> WebElement or bool:
    rowName = (".srb-ParticipantLabelCentered " if search == "table1" 
        else ".srb-ParticipantLabel_Name ")
    row = -1
    for index, linha in enumerate(
        encontra_filhos(opcao, rowName)):
        linha = linha.text.lower().strip()
        if medida.lower() == linha:
            row = index
            break
    if row == -1: return False

    column = 0
    info = re.escape(info).replace("X", "\d").lower()
    for index, coluna in enumerate(
        encontra_filhos(opcao, '.gl-MarketColumnHeader ')):
        coluna = coluna.text.lower()
        if re.search(info, coluna):
            column = index
            break

    columnName = (".gl-ParticipantOddsOnly" if search == "table1" 
        else ".gl-Participant_General ")
    botao =  encontra_filhos(encontra_filhos(
        opcao, ".gl-Market ")[column], columnName)[row]

    texto_btn = botao.text.split()
    if len(texto_btn) == 2: texto_btn = float(texto_btn[1])
    else: texto_btn = float(texto_btn[0])
    if texto_btn > minOdd: return botao

    print(f"Odd inferior ao requerido: {texto_btn} < {minOdd}")
    return False

def selecionar_info_tabela2(opcao: WebElement, info: str, medida: str, 
    minOdd: float) -> WebElement or bool:
    column = 0
    for index, coluna in enumerate(
        encontra_filhos(opcao, '.gl-MarketColumnHeader ')):
        if info.lower() in coluna.text.lower():
            column = index
            break
    
    for index, linha in enumerate(
        encontra_filhos(encontra_filhos(opcao, ".gl-Market "
            )[column], ".gl-ParticipantCentered")):
        texto, odd = linha.text.lower().strip().split()
        if medida.lower() == texto:
            botao = linha
            if float(odd) > minOdd:
                return botao
            else:
                print(f"Odd inferior ao requerido: {float(botao.text)} < {minOdd}")
            break

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

def procura_aposta(opcao: WebElement, info: str or list, 
    minOdd: float, search: str) -> bool:
    if search != "options":
        coluna, medida = info
        if search != "table2":
            botao = selecionar_info_tabela(
                opcao, coluna, medida, minOdd, search)
        else: 
            botao = selecionar_info_tabela2(
                opcao, coluna, medida, minOdd)
    else:
        botao = seleciona_info_botoes(opcao, info, minOdd)
    
    if botao: 
        botao.click()
        return True
    return False

def procura_opcao(wait: WebDriverWait, nome: str) -> WebElement or bool:
    nome = re.escape(nome).replace("X", "\d").lower() + "$"
    opcoes = encontra_elementos(wait, '.sip-MarketGroup ')
    for opcao in opcoes:
        try:
            titulo = encontra_filhos(opcao, '.sip-MarketGroupButton ')[0]
            titulo = titulo.text.strip().lower().replace("º", "°")
            if re.match(nome, titulo):
                print("\nprocura_opcao:", titulo)
                return opcao
        except Exception as e: print(e)
    return False

def adicionar_valor(
    wait: WebDriverWait, fast: WebDriverWait, title:str, valor: float) -> bool:
    atribuiu = False

    if atribuir_valor_single(wait, title, valor): return True

    try:
        time.sleep(2)
        apertar_botao(fast, ".bss-DefaultContent ")
    except Exception as e: print(e)
    
    try:
        time.sleep(2)
        atribuiu = atribuir_valor_multi(wait, title, valor)
    except Exception as e: print(e)

    try:
        apertar_botao(fast, ".bss-DefaultContent_Close ")
    except Exception as e: print(e)

    return atribuiu

def atribuir_valor_multi(wait: WebDriverWait, title:str, valor: float) -> bool:
    jogadas = encontra_elementos(wait, 
        ".bss-NormalBetItem_ContentWrapper ")
    title = re.escape(title).replace("X", "\d").lower().replace("°", "º")
    for jogada in reversed(jogadas):
        print(title, jogada.text.lower().strip())
        if re.search(title, jogada.text.lower().strip()):
            encontra_filhos(jogada, 
                ".bss-StakeBox_StakeValueInput"
            )[0].send_keys(str(valor))
            return True
    return False

def atribuir_valor_single(wait: WebDriverWait, title:str, valor: float) -> bool:    
    try:
        title = re.escape(title).replace("X", "\d").lower().replace("°", "º")
        text_jogada = encontra_elementos(wait, ".qbs-NormalBetItem_Details")[0].text
        if re.search(title, text_jogada.lower().strip()):
            preencher_campo(wait,".qbs-StakeBox_StakeInput ", str(valor))
            return True
    except Exception as e:
        print(type(e), e)
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

def nome_times(wait: WebDriverWait) -> Tuple[str]:
    return encontra_elementos(
        wait, ".ipe-EventHeader_Fixture"
    )[0].text.split(" v ")

def numero_gols(jogo: WebElement) -> List[int]:
    lista_gols = encontra_filhos(jogo,
        ".him-StandardScores_Scores "
    )[0].text.split("\n")
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

def encontra_filhos(element: WebElement, selector: str) -> List[WebElement]:
    return element.find_elements_by_css_selector(selector)

def encontra_elementos(wait: WebDriverWait, selector: str) -> List[WebElement]:
    return wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, selector)))
