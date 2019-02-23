# -*- coding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_actors(src):
    url = "https://baike.baidu.com"+src
    # 请求头部
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text.encode('ISO-8859-1'),'lxml')
    names = soup.find_all('dt', class_="basicInfo-item name")
    values = soup.find_all('dd', class_="basicInfo-item value")

    actors = []
    for name, value in zip(names, values):
        # print(name.text)
        if '主' in name.text and '演' in name.text:
            # print(name.text.replace('    ', ''), value.text)
            actors = value.text.strip().split('，')
            actors = [actor.strip().replace('\xa0', '').replace('\n[6]', '') for actor in actors if actor]
    # print(actors)
    return '，'.join(actors)

df = pd.read_csv('./movies.csv')

actors_list = []
for name, src in zip(list(df['name']), list(df['src'])):

    actors = get_actors(src)
    # print(name, actors)
    actors_list.append(actors)

new_df = pd.DataFrame({'actors': actors_list})
new_df['name'] = df['name']
# print(new_df)
new_df.to_csv(r'./actors.csv', index=False)
