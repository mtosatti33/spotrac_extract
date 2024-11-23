from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

IS_CHROME = False

# Configurar o driver do Chrome
if IS_CHROME:
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
else:
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
'''
    Importador dos tetos Salariais do site spotrac.com 
    Que retorna dados dos 32 times da NFL

    Páginas estão em inglês.
'''
# Lista de Times
teams = ['buffalo-bills', 'miami-dolphins', 'new-england-patriots', 'new-york-jets',
        'baltimore-ravens', 'cincinnati-bengals', 'cleveland-browns', 'pittsburgh-steelers',
        'houston-texans', 'indianapolis-colts', 'jacksonville-jaguars', 'tennessee-titans',
        'denver-broncos', 'kansas-city-chiefs', 'las-vegas-raiders', 'los-angeles-chargers',
        'dallas-cowboys', 'new-york-giants', 'philadelphia-eagles', 'washington-commanders',
        'chicago-bears', 'detroit-lions', 'green-bay-packers', 'minnesota-vikings',
        'atlanta-falcons', 'carolina-panthers',  'new-orleans-saints', 'tampa-bay-buccaneers',
        'arizona-cardinals', 'los-angeles-rams', 'san-francisco-49ers', 'seattle-seahawks'
        ]

# URL Modelo
url_modelo = "https://www.spotrac.com/nfl/{}/overview/_/year/2024"

# Lista de URLs Gerados
urls = [url_modelo.format(team) for team in teams]

# Lista Mestra
list = []

# Iteração de urls
for url in urls:
    # Pega os dados do site
    driver.get(url)

    # aguarda a carga da página em modo implícito (em segundos)
    driver.implicitly_wait(2)

    team = driver.find_element(By.XPATH, "//span[@style='font-weight:bold; text-transform: uppercase;']").text.title()

    # Importação e manipulação das listas
    # Elementos
    elems = driver.find_elements(By.XPATH, "//p[@class='card-text text-center text-black fs-lg pb-2']")

    # Lista de Elementos
    elem_list = [elem.text.replace(',','').replace('$','').split('/')[0] for elem in elems]

    # adiciona a lista em uma Lista mestra
    list.append([team, elem_list[0], elem_list[1], elem_list[2], elem_list[3]])


# Fechar o navegador
driver.quit()

# Criação do DataFrame do Pandas
df = pd.DataFrame(list)

# Adiciona colunas ao DataFrame
df.columns = ['Team','Total Cap','Cap Space','Reserve Lists','Dead Cap']

# Ele vai tentar salvar se o arquivo não estiver em aberto no Excel
try:
    df.to_excel("NFL Cap Space.xlsx", index=False)
except PermissionError:
    # Caso Contrário ele emite esse aviso 
    # quando a exceção PermissionError for chamada
    print("Não foi possível salvar. Permissão Negada")