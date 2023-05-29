from bs4 import BeautifulSoup
import requests
import pandas as pd

def campeonato_paulista():
    
    URL = "https://pt.wikipedia.org/wiki/Campeonato_Paulista_de_Futebol"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    tabela = soup.find("table", class_="wikitable")

    dict_data = {"Ano": [], 
                 "Organizador": [], 
                 "Campeão": [], 
                 "Vice-Campeão": [], 
                 "Terceiro Colocado": [], 
                 "Quarto Colocado": []}
    
    for linha in tabela.find_all("tr")[1:]:

        colunas = linha.find_all("td")

        if len(colunas) >= 5:
            k = 0

            # Caso "Normal"
            if len(colunas) == 6:
                ano = colunas[0].text.strip()
                k += 1

            # Caso em que há dois campeões devido ao pertencimento de organizações diferentes
            elif len(colunas) == 5:
                ano = dict_data["Ano"][-1]

            dict_data["Ano"].append(ano)
            dict_data["Organizador"].append(colunas[k].text.strip())
            dict_data["Campeão"].append(colunas[k+1].text.strip())
            dict_data["Vice-Campeão"].append(colunas[k+2].text.strip())
            dict_data["Terceiro Colocado"].append(colunas[k+3].text.strip())
            dict_data["Quarto Colocado"].append(colunas[k+4].text.strip())

        elif len(colunas) == 1:

            # Caso em que há dois vice-campeões. Optou-se em repetir os dados anteriores.
            if dict_data["Ano"][-1] != '1973(3)':
                campeao = dict_data["Campeão"][-1]
                vice    = colunas[0].text.strip()

            # Caso particular em que foram declarados dois campeões (1973)
            else:
                campeao = colunas[0].text.strip()
                vice = dict_data["Vice-Campeão"][-1]

            dict_data["Ano"].append(dict_data["Ano"][-1])
            dict_data["Organizador"].append(dict_data["Organizador"][-1])
            dict_data["Campeão"].append(campeao)
            dict_data["Vice-Campeão"].append(vice)
            dict_data["Terceiro Colocado"].append(dict_data["Terceiro Colocado"][-1])
            dict_data["Quarto Colocado"].append(dict_data["Quarto Colocado"][-1])

    
    df = pd.DataFrame(dict_data)

    df = df.replace(to_replace=' \([1-9]+\)|\(INV\)', value='', regex=True)

    return df