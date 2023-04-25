import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

import pandas as pd
import snscrape.modules.twitter as snscrape
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def remove_palavras(texto):
    palavras_separadas = word_tokenize(texto)
    palavras_remove    = stopwords.words('portuguese') + list(['de', 'que','paulo', 'nao', 'tão', 'lá', 
                                                               'ai', 'tô' , 'ta', 'né', 'tá', 'tbm', 'aí', 'tá',  
                                                               'pro', 't', 'co', 'q', 'p', 'n', 'pq', 'vc', 'ter', 
                                                               "'m", '3', '1', '2', "''", '``', '..', '...', 
                                                               ',', '.', ':','’', ';', '`', '(', ')', 
                                                               '!', '/', '|', '-', '#', '@', '?', 'https'])
    
    return ' '.join([palavra for palavra in palavras_separadas if palavra.casefold() not in palavras_remove])

def main():
   
    lista_tweets = []
    contagem = 0
    maximo = 10000

    # Raspagem (scrapte) dos Tweets
    for tweet in snscrape.TwitterSearchScraper('SPFC since:2023-04-10 until:2023-04-18').get_items():

       if contagem <= maximo:
          lista_tweets.append([tweet.date, tweet.id, tweet.user.username, tweet.url, tweet.rawContent])
          contagem += 1
       else:
          break

    #Criação do DataFrame
    tweets_df = pd.DataFrame(lista_tweets, columns=['Data', 'Id', 'Usuario', 'Url', 'Conteudo'])
    conteudo_tweets_df = tweets_df['Conteudo'].apply(lambda x: remove_palavras(x))

    #Contagem de Palavras
    string_tweets = ' '.join(conteudo_tweets_df.str.lower())
    pd.Series(string_tweets.split()).value_counts()[:100].to_csv('Contagem.csv')

    #Criação da Nuvem de Palavras
    wordcloud = WordCloud(
        width=700, 
        height=500,
        background_color="black",
        max_font_size=100,
        max_words=100,
        collocations=True
    ).generate(string_tweets)

    plt.figure(figsize=[15, 15])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wordcount.png')

if __name__ == '__main__':
   main()