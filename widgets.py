from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

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
            try: apertar_botao(wait, ".pm-PushTargetedMessageOverlay_CloseButton ")
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

    print("Tempo:", hora_min)
    tempo = int(hora_min.split(":")[0])
    if tempo > maximo:
        print("Passou do tempo requisitado:", maximo)
        return False
    return True

def abrir_opcoes(wait: WebDriverWait):
    time.sleep(6)
    botoes = encontra_elementos(wait, '[class="sip-MarketGroupButton "]')
    for botao in botoes:
        try: botao.click()
        except: pass

def procura_opcao(wait: WebDriverWait, nome: str) -> WebElement or bool:
    opcoes = encontra_elementos(wait, '.sip-MarketGroup ')
    for opcao in opcoes:
        titulo = encontra_filhos(opcao, '.sip-MarketGroupButton ')[0]
        if nome.lower() in titulo.text.lower():
            return opcao
    return False

def selecionar_info_tabela(opcao: WebElement, info: str, medida: float) -> WebElement:
    local = -1
    for index, linha in enumerate(
        encontra_filhos(opcao, ".srb-ParticipantLabelCentered ")):
        linha = linha.text.lower().strip()
        if medida.lower() == linha.strip().lower():
            local = index
    if local == -1: return False

    indice = 0
    for index, coluna in enumerate(
        encontra_filhos(opcao, '.gl-MarketColumnHeader ')):
        if index != 0 and info.lower() in coluna.text.lower():
            indice = index

    return encontra_filhos(
        encontra_filhos(opcao, ".gl-Market ")[indice],
        ".gl-ParticipantOddsOnly")[local]

def seleciona_info_botoes(opcao: WebElement, info: str) -> WebElement or bool:
    for coluna in encontra_filhos(opcao, ".gl-Participant_General "):
        if info == coluna.text.split("\n")[0]:
            return coluna
    return False

def procura_aposta(opcao: WebElement, info: str or tuple) -> bool:
    if type(info) == tuple:
        coluna, medida = info
        botao = selecionar_info_tabela(opcao, coluna, medida)
    else:
        botao = seleciona_info_botoes(opcao, info)
    
    if botao: 
        botao.click()
        return True
    return False

def adicionar_valor(wait: WebDriverWait, fast: WebDriverWait, valor: float) -> bool:
    atribuiu = False
    try:
        time.sleep(2)
        encontra_elementos(
            wait, ".bss-DefaultContent "
        )[0].click()
    except: pass
    
    try:
        time.sleep(2)
        atribuiu = atribuir_valor(wait, valor)
    except: pass

    try:
        apertar_botao(fast, ".bss-DefaultContent_Close ")
    except: pass

    return atribuiu

def atribuir_valor(wait: WebDriverWait, valor: float) -> bool:
    # jogadas = encontra_elementos(wait, 
    #     ".bss-NormalBetItem_ContentWrapper ")
    # for jogada in reversed(jogadas):
    #     if title.lower() in jogada.text.lower():
    #         encontra_filhos(jogada, 
    #             ".bss-StakeBox_StakeValueInput"
    #         )[0].send_keys(valor)
    entradas = encontra_elementos(wait, ".bss-StakeBox_StakeValueInput")
    for entrada in entradas:
        if entrada.get_attribute("value") == "Valor de Aposta":
            entrada.send_keys(valor)
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

def nome_times(wait: WebDriverWait) -> tuple:
    return encontra_elementos(
        wait, ".ipe-EventHeader_Fixture"
    )[0].text.split(" v ")

def numero_gols(jogo: WebElement) -> list:
    lista_gols = encontra_filhos(jogo,
        ".him-StandardScores_Scores "
    )[0].text.split("\n")
    print("Gols:", " x ".join(lista_gols))
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

def encontra_filhos(element: WebElement, selector: str) -> list:
    return element.find_elements_by_css_selector(selector)

def encontra_elementos(wait: WebDriverWait, selector: str) -> list:
    return wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, selector)))
