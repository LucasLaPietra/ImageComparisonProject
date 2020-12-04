import psycopg2
from img2vec_pytorch import Img2Vec
import os, sys
from PIL import Image
import numpy as np

def convertArray(numpyArray):
    newArray = []
    for elem in numpyArray:
        newArray.append(elem)
    return newArray


def extraerVector(imagen):
    img2vec = Img2Vec(cuda=False)
    vec = img2vec.get_vec(imagen, tensor=True)
    return vec


def resizeImagen(imagen):
    final_size = 224
    size = imagen.size
    ratio = float(final_size) / max(size)
    new_image_size = tuple([int(x * ratio) for x in size])
    imagen = imagen.resize(new_image_size, Image.ANTIALIAS)

    new_im = Image.new("RGB", (final_size, final_size))
    new_im.paste(imagen, ((final_size - new_image_size[0]) // 2, (final_size - new_image_size[1]) // 2))

    return new_im


def tensorToString(embeddingsVector):
    numpyVector = np.array(embeddingsVector.unsqueeze(0).tolist())

    stringVector = str(convertArray(numpyVector.flatten()))

    stringVector = '{' + stringVector[1:]
    stringVector = stringVector[:-1] + '}'

    return stringVector

def conectarAPostgres():
    conn = psycopg2.connect(
        host="localhost",
        database="proyectoGad",
        user="postgres",
        password="luxlp1996")
    return conn


def agregarImagenesaBD(path):
    conn=conectarAPostgres()
    cr = conn.cursor()
    dirs = os.listdir(path)
    for directorio in dirs:
        subpath = f'{path}\{directorio}'
        subdirectorio = os.listdir(subpath)
        for item in subdirectorio:
            if item.endswith('.jpg') or item.endswith('.png'):
                pathimg = f'{subpath}\{item}'
                imagen = Image.open(pathimg)
                embeddingsVector = extraerVector(resizeImagen(imagen))
                stringVector = tensorToString(embeddingsVector)
                cr.execute('INSERT INTO imagenes (nombre,vector) VALUES (%s,%s);', [directorio, stringVector])
        print(f'Vectores para {directorio} cargados con exito')
    conn.commit()

def agregarPokemonaBD(path):
    conn = conectarAPostgres()
    cr = conn.cursor()
    dirs = os.listdir(path)
    for directorio in dirs:
        subpath = f'{path}\{directorio}'
        subdirectorio = os.listdir(subpath)
        for item in subdirectorio:
            pathimg = f'{subpath}\{item}'
            cr.execute('INSERT INTO pokemon (nombre,pathimagen) VALUES (%s,%s);', [directorio, pathimg])
    conn.commit()

pathimagenes=f'C:\PokemonImagen'
pathdatos=f'C:\PokemonData'
agregarImagenesaBD(pathdatos)
#agregarPokemonaBD(pathimagenes)