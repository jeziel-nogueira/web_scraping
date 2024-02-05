import PySimpleGUI as sg
import os, sys
import pandas as pd
from PIL import Image, ImageTk
import scraper
import glob

root_path = 'C:/Users/ADM/Documents/Loja/'

#scraper.load_data()
def get_current_estoque():
    aux = 0
    total = 0
    for prod_ in os.listdir(root_path + 'produtos/'):
        total = total + 1
        #prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        #print('Nome: ', prod['Nome'][0])
        prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        estoque = scraper.get_prod_estoque(prod['Link'][0])

        if str(prod['Estoque'][0]) != str(estoque):
            print(prod['Nome'][0] + ': ' + str(prod['Estoque'][0]) + ' > ' + estoque)
    
        #current_path = root_path + 'produtos/' + prod_ + '/'
        #scraper.update_estoque(current_path, estoque)
def get_current_price():
    for prod_ in os.listdir(root_path + 'produtos/'):
        
        #prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        #print('Nome: ', prod['Nome'][0])
        prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        preco = scraper.get_prod_preco(prod['Link'][0])

        current_path = root_path + 'produtos/' + prod_ + '/'
        scraper.update_preco(current_path, preco)

def download_imgs():
    for prod_ in os.listdir(root_path + 'produtos/'):

        aux = 0
        for img in os.listdir(root_path + "produtos/" + prod_ + '/images/'):
            aux = aux + 1
        if aux == 0:
            prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
            scraper.prod_images(prod['Link'][0], prod_)
def calcular_val_venda():
    tree_img = img
    for prod_ in os.listdir(root_path + 'produtos/'):
        prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        preco = prod['Preço'][0]  # scraper.get_prod_preco(prod['Link'][0])
        preco = preco.replace(',','.')
        try:
            lucro =float(preco) * 0.15
            if prod['Estoque'][0] != 0:
                sell = (float(preco) + (float(preco) / 2) + (float(preco) * 0.15))/0.8
                if sell >= 10:
                   sell = (float(preco) + 5 + (float(preco) * 0.15))/0.8
                texto = prod['SKU'][0] + ": " + str(prod['Preço'][0]) + ' => ' + str(sell) + ' | Estoque: ' + str(prod['Estoque'][0]) + ' | Lucro: '+ str(lucro)
                sel.append(texto)
            else:
                print("Estoque vazio: " + prod['Nome'][0])
        except:
            print('Erro: ', prod['Nome'][0], ': ', prod['Preço'][0], ' > ', prod['Link'][0], ' Estoque: ', + prod['Estoque'][0])
tree_img = []
layout = [
    [sg.Text("Banco de dados")],
    [sg.Button("Update"), sg.Button("Sair")],
    [sg.Listbox(values= tree_img, size=(100, 30), key='lista')],
    [sg.Image(key='selected', size=(30, 30))],
]

janela = sg.Window("Scrapper", layout)
prod = os.listdir(root_path + 'produtos/')
imgs = []
for prod_ in os.listdir(root_path + 'produtos/'):
        for img in os.listdir(root_path + "produtos/" + prod_ + '/images/'):
            imgs.append(img)

aux = 0
sel = []
while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED:
        break
    if evento == 'Update':
        #calcular_val_venda()
        get_current_estoque()


        janela['lista'].update(sel)
            


        

        
        

janela.close()