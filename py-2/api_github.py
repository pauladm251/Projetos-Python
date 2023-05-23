import requests
import pandas as pd
import plotly.express as px


def main():

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
    
    projeto_df.sort_values('Estrelas').to_csv("projetos.csv")

    # Gráfico com os projetos
    fig = px.bar(projeto_df, x='Projeto', y='Estrelas', title="<b>Projetos do GitHub</b>")
    fig.update_layout(

        #Título
        title_font_color="gray",
        title_font_size=25,
        title_x=0.5,

        #Eixos
        font_color="black",
        yaxis=dict(titlefont = dict(size=16), 
               tickfont  = dict(size=16)),
        xaxis=dict(titlefont = dict(size=16),
               tickfont = dict(size=14))
    )

    # Salvando Gráfico
    fig.write_html("projetos.html")

if __name__=='__main__':
    main()