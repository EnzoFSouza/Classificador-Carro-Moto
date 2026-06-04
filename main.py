import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import gradio as gr
import numpy as np

MODEL_PATH = "modelo_carro_moto.keras"

modelo_carregado = tf.keras.models.load_model(MODEL_PATH)

IMG_HEIGHT = 180
IMG_WIDTH = 180

#Função de predição
def classificar_imagem(imagem_pil):
    if imagem_pil is None:
        return "Por favor, envie uma imagem."

    #Pré-processamento
    #Converte a imagem do Gradio para array e redimensiona
    img = tf.keras.preprocessing.image.img_to_array(imagem_pil)
    img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])

    #Adiciona a dimensão do Batch (de [180, 180, 3] para [1, 180, 180, 3])
    #Redes neurais de visão computacional não aceitam imagem isolada; elas esperam um lote de imagens.
    #tf.expand_dims(img, 0) transforma a imagem de formato 180x180x3 em um lote de tamanho 1x180x180x3 para que o Keras consiga processar.
    img_batch = tf.expand_dims(img, 0)

    #Executa a Predição
    predicao = modelo_carregado.predict(img_batch)[0][0]  #Retorna a probabilidade da classe Carro

    #Pós-processamento para exibição amigável
    #Como a saída é Sigmoid, calculamos a confiança de cada classe
    probabilidade_carro = float(predicao)
    probabilidade_moto = 1.0 - probabilidade_carro

    # Retorna um dicionário com os formatos de exibição em barras do Gradio
    return {
        "Carro": probabilidade_carro,
        "Moto": probabilidade_moto,
    }

#Construção da interface
interface = gr.Interface(
    fn=classificar_imagem,
    #Entrada de imagem
    inputs=gr.Image(type="pil", label="Envie a foto de um Carro ou Moto"),
    #Saída com barras de probabilidade
    outputs=gr.Label(num_top_classes=2, label="Resultado do Modelo"),
    title="Carro vs Moto - Classificador de Veículos",
    description="Faça o upload de uma imagem e veja a rede neural decidir se é um carro ou uma moto.",
    theme="soft",
    flagging_mode="never",
)

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False)