import PySimpleGUI as sg
import os, sys
import pandas as pd
from PIL import Image, ImageTk
import scraper
import glob

root_path = 'C:/Users/ADM/Documents/Loja/'

#scraper.load_data()
def get_price_estoque():
    for prod_ in os.listdir(root_path + 'produtos/'):
        
        #prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        #print('Nome: ', prod['Nome'][0])
        prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
        estoque = scraper.get_prod_estoque(prod['Link'][0])
        preco = scraper.get_prod_preco(prod['Link'][0])

        current_path = root_path + 'produtos/' + prod_ + '/'
        scraper.update_estoque(current_path, estoque)
        scraper.update_preco(current_path, preco)
        print(prod['Nome'][0],': ', preco, ' | ', estoque)

def download_imgs():
    for prod_ in os.listdir(root_path + 'produtos/'):

        aux = 0
        for img in os.listdir(root_path + "produtos/" + prod_ + '/images/'):
            aux = aux + 1
        if aux == 0:
            prod = pd.read_csv(root_path + "produtos/" + prod_ + '/' + prod_ , sep=";", encoding="utf-8")
            scraper.prod_images(prod['Link'][0], prod_)