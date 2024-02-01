import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

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

def criar_pasta(nome):
   pasta_main = 'produtos/'
   if(not os.path.exists(pasta_main)):
      os.mkdir(pasta_main)
   if(not os.path.exists('produtos/{nome}/')):
      try:
         os.mkdir(os.path.join(pasta_main, nome))
         img_path = 'produtos/' + nome
         os.mkdir(os.path.join(img_path, 'images'))
      except:
         print('Folder alreade exist')

def save_data(data_, prod_path):
      path = ''
      with open (prod_path, 'a', newline='', encoding='UTF-8') as f:
       f.write(data_)
 
   
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

#percorrer lista de links de produtos e coletar dados
index = 0
for lin in lista_Links:
    url_pagina = lista_Links[index]
    site = requests.get(url_pagina, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')


    prod_name = soup.find('h1').get_text().strip()
    prod_code = soup.find(attrs={'itemprop':'sku'}).get_text().strip()
    prod_price = 0
    prod_estoque = 0
    
    prod_folder = prod_code + '/'
    criar_pasta(prod_folder)
    try:
       estoque = soup.find(class_='qtde_estoque').get_text().strip()
       prod_estoque = estoque
       price = soup.find(class_='preco-promocional cor-principal titulo').get_text().strip()
       prod_price = price[3:]
    except:
       prod_price = 'nd'
       prod_estoque = 0

    prd_data = prod_name + ';' + prod_code + ';' + prod_price + ';' + str(prod_estoque) + ';' + lista_Links[index] + '\n'
    prod_path = 'produtos/' + prod_code + '/' + prod_code
    save_data(prd_data, prod_path)

    aux = 1
    for tag in soup():
      if 'data-imagem-grande' in tag.attrs:
        image_url = tag.get("data-imagem-grande")
        #img.save('/absolute/path/to/myphoto.jpg', 'JPEG')
        img = Image.open(requests.get(image_url, stream = True).raw)
        img_name = tag.get("title") + '.jpg'
        img_path = 'produtos/' + prod_code + '/images/' + prod_code + str(aux) + '.jpg'
        try:
           if(not os.path.exists(img_path)):
            img.save(img_path, 'JPEG')
        except:
           print('Error on save img: ', img_name)
           print('Error details: ', prd_data)
        aux = aux + 1
        

    index = index + 50