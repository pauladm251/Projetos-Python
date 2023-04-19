import snscrape.modules.twitter as snscrape
import sqlite3

lista_tweets = []
contagem = 0
maximo = 1000

for tweet in snscrape.TwitterSearchScraper('SPFC since:2023-04-10 until:2023-04-18').get_items():

   if contagem <= maximo:
      lista_tweets.append([tweet.date, tweet.id, tweet.user.username, tweet.url, tweet.rawContent])
      contagem += 1
   else:
      break


con = sqlite3.connect('scrape-tw.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tweets(
               Data TEXT, 
               Id TEXT, 
               Nome TEXT, 
               URL TEXT, 
               Conteudo TEXT,
               Primary Key(Data, Id, Nome))"""
         )

for tweet in lista_tweets:
    cur.execute('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)', tweet)

con.commit()
con.close()