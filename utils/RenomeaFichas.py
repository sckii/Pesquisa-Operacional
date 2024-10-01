import pandas as pd
from os import listdir
from os.path import isfile, join
import os

# Specify the directory containing the files
folder_path = '/home/arhur/Documents/Trab PO/T2/Pesquisa-Operacional/dados/fichas'
nome_arquivos = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


# for filename in nome_arquivos:
#     new_name = filename.replace("Ficha Formatada - ", "")

#     old_file = os.path.join(folder_path, filename)
#     new_file = os.path.join(folder_path, new_name)

#     os.rename(old_file, new_file)


nome_arquivos = sorted(nome_arquivos)

i = 0
for filename in nome_arquivos:
    new_name = str(i) + " " + filename
    print(filename + " -> " + new_name)

    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_name)

    os.rename(old_file, new_file)
    i += 1;
    
print("Files renamed successfully!")