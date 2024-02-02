import PySimpleGUI as sg
import os, sys
import pandas as pd
from PIL import Image
import csv

prod = pd.read_csv(r"C:\Users\ADM\Desktop\Shopee\app\produtos\PL-513\PL-513", sep=";", encoding="utf-8")
print('Data 0: ', prod['Data'][0], 'Link: ', prod['Link'][0])

desc = ''
with open(r'C:\Users\ADM\Desktop\Shopee\app\produtos\PL-513\PL-513_desc', encoding='UTF-8') as f:
    desc = f.readlines()

for lines in desc:
    print(lines, '\n')