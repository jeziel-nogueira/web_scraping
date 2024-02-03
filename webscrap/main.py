import PySimpleGUI as sg
import os, sys
import pandas as pd
from PIL import Image
import scraper
import glob

root_path = 'C:/Users/ADM/Documents/Loja/'

prod = pd.read_csv(root_path + "produtos/PL-513/PL-513", sep=";", encoding="utf-8")
print('Data 0: ', prod['Data'][0], 'Link: ', prod['Link'][0])

desc = ''
with open(root_path + 'produtos/PL-513/PL-513_desc', encoding='UTF-8') as f:
    desc = f.readlines()

for lines in desc:
    print(lines)

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button('load'),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)
while True:
    

    evento, valores = window.read()
    if evento == "Sair" or evento == sg.WIN_CLOSED:
        break
    if evento == "-FOLDER-":
        folder = valores["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif evento == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                valores["-FOLDER-"], valores["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass
    if evento == 'load':
        path = root_path + 'produtos/PL-513/images/*.jpg'
        print(path)
        for filename in glob.glob(path): #assuming gif
            im=Image.open(filename)
            print(filename)
            # image_list.append(im)

window.close()

