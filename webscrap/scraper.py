import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from PIL import Image

today = datetime.now()

url = 'https://www.piscaled.com.br/eletronica'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
produtos = soup.find_all('li', class_='span3')

root_path = 'C:/Users/ADM/Documents/Loja/'
lista_Links = []



# Descobrir quantas paginas de produtos na loja
ultima_pagina = soup.find('li', class_='active')
uls = []
for nextSibling in ultima_pagina.find_next_siblings():
    if nextSibling.name == 'h1':
        break
    if nextSibling.name == 'li':
        uls.append(nextSibling.get_text().strip())

ultima_pagina_index  = len(uls) - 2

def buscar_novos_prdutos():
   #descobrir maximo de paginas de produtos
   site = requests.get(url, headers=headers)
   soup = BeautifulSoup(site.content, 'html.parser')
   produtos = soup.find_all('li', class_='span3')
   ultima_pagina = soup.find('li', class_='active')
   uls = []
   for nextSibling in ultima_pagina.find_next_siblings():
      if nextSibling.name == 'h1':
         break
      if nextSibling.name == 'li':
         uls.append(nextSibling.get_text().strip())
   ultima_pagina_index  = len(uls) - 2

   # Pegar link de todos os produtos aind nao salvos
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


def criar_pasta(nome):
   pasta_main = root_path + 'produtos/'
   if(not os.path.exists(pasta_main)):
      os.mkdir(pasta_main)
   if(not os.path.exists(pasta_main + '{nome}/')):
      try:
         os.mkdir(os.path.join(pasta_main, nome))
         img_path = pasta_main + nome
         os.mkdir(os.path.join(img_path, 'images'))
      except:
         print('Folder alreade exist')

def save_data(data_, prod_path, desc, prod_path_desc):
      cabecalho = 'Data;Nome;SKU;Preço;Estoque;Link' + '\n'
      flag_path = prod_path + '_flag'
      flag_title = 'new'
         
      if(not os.path.exists(prod_path)):
         with open (prod_path, 'a', newline='', encoding='UTF-8') as f:
            f.write(cabecalho)
            f.write(data_)
         with open (prod_path_desc, 'a', newline='', encoding='UTF-8') as f:
            f.write(desc)
         with open (flag_path, 'a', newline='', encoding='UTF-8') as f:
            f.write('new' + '\n')
            f.write('true')
      else:
         with open (prod_path, 'a', newline='', encoding='UTF-8') as f:
            f.write(data_)
def update_estoque(prod_path, val):
   path = prod_path + 'estoque_reg'
   if(not os.path.exists(path)):
      with open (path, 'a', newline='', encoding='UTF-8') as f:
         f.write('Estoque' + '\n')
         f.write(str(val))
   else:
      with open (path, 'a', newline='', encoding='UTF-8') as f:
            f.write(str(val))
def update_preco(prod_path, val):
   path = prod_path + 'preco_reg'
   if(not os.path.exists(path)):
      with open (path, 'a', newline='', encoding='UTF-8') as f:
         f.write('Preco' + '\n')
         f.write(str(val))
   else:
      with open (path, 'a', newline='', encoding='UTF-8') as f:
            f.write(str(val))
   
def prod_images(link_, prod_code):
   site = requests.get(link_, headers=headers)
   soup = BeautifulSoup(site.content, 'html.parser')
   img_Index = 1
   for tag in soup():
      if 'data-imagem-grande' in tag.attrs:
        image_url = tag.get("data-imagem-grande")
        img = Image.open(requests.get(image_url, stream = True).raw)
        img_name = tag.get("title") + '.jpg'
        img_path = root_path + 'produtos/' + prod_code + '/images/' + prod_code + str(img_Index) + '.jpg'
        img_error = False
        try:
           if(not os.path.exists(img_path)):
            img.save(img_path, 'JPEG')
        except:
           img_error = True
           print('Error on save img: ', img_name)
        if img_error:
            img_name = tag.get("title") + '.png'
            img_path = root_path + 'produtos/' + prod_code + '/images/' + prod_code + str(img_Index) + '.png'
            try:
               if(not os.path.exists(img_path)):
                  img.save(img_path, 'PNG')
                  print('IMG Save: ', img_path)
            except:
               print('Error on save img PNG: ', img_name)
      img_Index = img_Index + 1
           

def get_prod_estoque(link_):
   val = 0
   site = requests.get(link_, headers=headers)
   soup = BeautifulSoup(site.content, 'html.parser')
   try:
      val = soup.find(class_='qtde_estoque').get_text().strip()
   except:
      val = 0
   return val

def get_prod_preco(link_):
   site = requests.get(link_, headers=headers)
   soup = BeautifulSoup(site.content, 'html.parser')

   val = 0
   try:
      price = soup.find(class_='preco-promocional cor-principal titulo').get_text().strip()
      val = price[3:]
   except:
      val = 'nd'
   return val



#percorrer lista de links de produtos e coletar dados
def load_data():
   buscar_novos_prdutos()
   for lin in lista_Links:
      url_pagina = lin
      site = requests.get(url_pagina, headers=headers)
      soup = BeautifulSoup(site.content, 'html.parser')


      prod_name = soup.find('h1').get_text().strip()
      prod_code = soup.find(attrs={'itemprop':'sku'}).get_text().strip()
      prod_price = get_prod_preco(lin)
      prod_estoque = get_prod_estoque(lin)
      prod_desc = 'ND'

      try:
         prod_desc = soup.find(id='descricao').get_text().strip()
      except:
         prod_desc = 'ND'
      
      prod_folder_name = prod_code + '/'
      criar_pasta(prod_folder_name)

      #salvar dados do produto
      dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
      prd_data = dt_string + ';' + prod_name + ';' + prod_code + ';' + prod_price + ';' + str(prod_estoque) + ';' + lin + '\n'
      prod_path = root_path + 'produtos/' + prod_code + '/' + prod_code
      _desc = prod_code + '_desc'
      prod_path_desc = root_path + 'produtos/' + prod_code + '/' + _desc
      
      save_data(prd_data, prod_path, prod_desc, prod_path_desc)

      # salvar imagens do produto
      prod_images(lin, prod_code)






# Para cada novo prduto criar um arquivo txt flag com booleana para new=true, para poder saber a diferença entre antigos e novos
# Funçao para verificar mudanças em estoque e preço
# Salvar apenas registro de estoque diario, nao salvar informaçoes repetidas como descricao, nome, etc