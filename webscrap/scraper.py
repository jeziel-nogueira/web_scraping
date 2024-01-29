import requests
from bs4 import BeautifulSoup

url = 'https://www.piscaled.com.br/eletronica'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

site = requests.get(url, headers=headers)

soup = BeautifulSoup(site.content, 'html.parser')
produtos = soup.find_all('li', class_='span3')


# Descobrir quantas paginas de produtos na loja
ultima_pagina = soup.find('li', class_='active')
uls = []
for nextSibling in ultima_pagina.find_next_siblings():
    if nextSibling.name == 'h1':
        break
    if nextSibling.name == 'li':
        uls.append(nextSibling.get_text().strip())

#for item in uls:
 #   print(item.text.encode("utf-8"))
ultima_pagina_index  = len(uls) - 2
print(uls[ultima_pagina_index])

lista_produtos = soup.find_all('li', class_='span3')
nomes = lista_produtos[0].find('a', class_='nome-produto cor-secundaria').get_text().strip()
#nome = nomes.find('a', class_='nome-produto cor-secundaria').get_text().strip()

links = lista_produtos[0].find_all("a", class_='produto-sobrepor') 
for link in links:
  print("Link:", link.get("href"), "Text:", link.string)


print('=============')

print(lista_produtos[4].find("a", class_='produto-sobrepor').get("href"), ' ', lista_produtos[4].find('a', class_='nome-produto cor-secundaria').get_text().strip())

