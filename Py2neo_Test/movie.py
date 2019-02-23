# -*- coding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E7%94%B5%E5%BD%B1%E7%A5%A8%E6%88%BF/4101787"
# 请求头部
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text.encode('ISO-8859-1'),'lxml')
table = soup.find('table')('tr')

movies = []
for line in table[1:]:
    movie = {'rank': int(line('td')[0].text),
                  'src': line('td')[1]('a')[0]['href'],
                  'name': line('td')[1].text,
                  'box_office': line('td')[2].text,
                  'avg_price': int(line('td')[3].text),
                  'avg_people': int(line('td')[4].text),
                  'begin_date': line('td')[5].text.strip(),
                  }
    # print(movie)
    movies.append(movie)

# print(movies)

df = pd.DataFrame({'rank': [movie['rank'] for movie in movies],
                   'src': [movie['src'] for movie in movies],
                   'name': [movie['name'] for movie in movies],
                   'box_office': [movie['box_office'] for movie in movies],
                   'avg_price': [movie['avg_price'] for movie in movies],
                   'avg_people': [movie['avg_people'] for movie in movies],
                   'begin_date': [movie['begin_date'] for movie in movies]
                   })
# print(df.head())
df.to_csv(r'./movies.csv', index=False)
