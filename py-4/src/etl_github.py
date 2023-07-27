import requests
import pandas as pd
import json


def main():

    with open('config.json', 'r') as arquivo:
        config_data = json.load(arquivo)

    bucket   = config_data["bucket_name"]
    folder   = config_data["target_folder"]
    csv_file = config_data["csv_file_name"]

    # Requisição utilizando a API do GitHub
    url = "https://api.github.com/search/repositories?q=language:rust+language:c+language:assembly&sort:stars"
    request = requests.get(url).json()
    items = request['items']

    # Lista de Projetos
    lista_projetos = []
    for item in items:
        lista_projetos.append([item["full_name"].split("/")[1],
                               item["full_name"].split("/")[0],
                               item["html_url"],
                               item["created_at"],
                               item["updated_at"],
                               item["description"],
                               item["stargazers_count"]])

    # Criação do DataFrame
    projeto_df = pd.DataFrame(lista_projetos, columns=['Projeto', 'Owner', 'Link', 'Criação', 'Atualização',
                                                        'Descrição', 'Estrelas'])
    
    if folder == "" or folder is None:
        projeto_df.sort_values('Estrelas').to_csv(f"gs://{bucket}/{csv_file}")
    else:
        projeto_df.sort_values('Estrelas').to_csv(f"gs://{bucket}/{folder}/{csv_file}")

if __name__=='__main__':
    main()