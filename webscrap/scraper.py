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

ultima_pagina_index  = len(uls) - 2
print(uls[ultima_pagina_index])

# Pegar link de todos os produtos 
lista_Links = []
for i in range(1, int(uls[ultima_pagina_index])+1):
    url_pagina = f'https://www.piscaled.com.br/eletronica?pagina={i}#'
    site = requests.get(url_pagina, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    lista_produtos = soup.find_all('li', class_='span3')
    index = 0
    for prod in lista_produtos:
        links = lista_produtos[index].find_all("a", class_='produto-sobrepor')
        for link in links:
          x = link.get("href")
          lista_Links.append(x)
        index = index + 1


index = 380
for lin in lista_Links:
    url_pagina = lista_Links[index]
    site = requests.get(url_pagina, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    nome = soup.find('h1').get_text()
    value = soup.find(class_='preco-promocional cor-principal titulo').get_text().strip()
    preco = value[3:]
    estoque = soup.find(class_='qtde_estoque').get_text().strip() # Tratar exeption
    lista_Links_img = soup.find(class_='miniaturas slides')
    img_link = soup.find_all('data-imagem-grande')
    for tag in soup():
      if 'data-imagem-grande' in tag.attrs:
        ix = tag.get("data-imagem-grande")
        print(ix)
    index = index + 1


#nomes = lista_produtos[0].find('a', class_='nome-produto cor-secundaria').get_text().strip()
#nome = nomes.find('a', class_='nome-produto cor-secundaria').get_text().strip()

#print(lista_produtos[4].find("a", class_='produto-sobrepor').get("href"), ' ', lista_produtos[4].find('a', class_='nome-produto cor-secundaria').get_text().strip())

#nome = soup.find_all('a', class_='nome-produto cor-secundaria').get_text().strip()

#links = lista_produtos[0].find_all("a", class_='produto-sobrepor') 
#for link in links:
#  print("Link:", link.get("href"), "Text:", link.string)