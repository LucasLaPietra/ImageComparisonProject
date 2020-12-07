from img2vec_pytorch import Img2Vec
import torch
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import psycopg2
import scipy.spatial.distance as dist

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
    head, tail = imagen.split(',')
    imagen=Image.open(BytesIO(base64.b64decode(tail, '-_')))
    final_size = 224
    size = imagen.size
    ratio = float(final_size) / max(size)
    new_image_size = tuple([int(x * ratio) for x in size])
    imagen = imagen.resize(new_image_size, Image.ANTIALIAS)

    new_im = Image.new("RGB", (final_size, final_size))
    new_im.paste(imagen, ((final_size - new_image_size[0]) // 2, (final_size - new_image_size[1]) // 2))

    return new_im

def conectarAPostgres():
    conn = psycopg2.connect(
        host="localhost",
        database="proyectoGad",
        user="postgres",
        password="luxlp1996")
    return conn

def tensorToString(embeddingsVector):
    numpyVector = np.array(embeddingsVector.unsqueeze(0).tolist())

    stringVector = str(convertArray(numpyVector.flatten()))

    stringVector = '{' + stringVector[1:]
    stringVector = stringVector[:-1] + '}'

    return stringVector

def obtenerPokemonSimil(imagen):
    conn=conectarAPostgres()
    listasimilaridades=[]
    cr = conn.cursor()
    embeddingsVector = extraerVector(resizeImagen(imagen))
    stringVector = tensorToString(embeddingsVector)
    cr.execute('Select * from imagenes;')
    listaimagenes = cr.fetchall()
    for i in listaimagenes:
        distancia = dist.euclidean(embeddingsVector, i[2])
        listasimilaridades.append(distancia)
    minima = listaimagenes[listasimilaridades.index(min(listasimilaridades))]
    minimadistancia = min(listasimilaridades)
    cr.execute('Select * from pokemon where pokemon.nombre = %s;', [minima[1]])
    resultado = cr.fetchall()
    return (minimadistancia,resultado[0][1],resultado[0][2])