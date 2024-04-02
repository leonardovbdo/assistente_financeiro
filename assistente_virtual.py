# imports necessarios para o funcionamento do assistente
import speech_recognition as sr
from nltk import word_tokenize, corpus
from threading import Thread
import json

from lampada import *
from tocador import *

# configuracoes do assistente
IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"
TEMPO_DE_ESCUTA = 4

ATUADORES = [
    {
        "nome": "lâmpada",
        "iniciar": iniciar_lampada,
        "parametro_de_atuacao": None,
        "atuar": atuar_sobre_a_lampada
    },
    {
        "nome": "tocador",
        "iniciar": iniciar_tocador,
        "parametro_de_atuacao": None,
        "atuar": atuar_sobre_tocador
    }
]

# 1. transcricao da fala para uma string

# realiza a configuracao inicial do assistente
def iniciar():
    iniciado, reconhecedor, palavras_de_parada, nome_do_assistente, acoes = False, None, None, None, None

    try:
        reconhecedor = sr.Recognizer()

        palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

        with open(CAMINHO_CONFIGURACAO, "r", encoding="utf-8") as arquivo:
            configuracao = json.load(arquivo)

            nome_do_assistente = configuracao["nome"]
            acoes = configuracao["acoes"]

            arquivo.close()

        for atuador in ATUADORES:
            parametro_de_atuacao = atuador["iniciar"]()
            atuador["parametro_de_atuacao"] = parametro_de_atuacao

        iniciado = True
    except Exception as e:
        print(f"erro iniciando o assistente: {str(e)}")

    return iniciado, reconhecedor, palavras_de_parada, nome_do_assistente, acoes

# realiza a captura da fala do usuario
def escutar_fala(reconhecedor):
    tem_fala, fala = False, None

    with sr.Microphone() as fonte_de_audio:
        try:
            reconhecedor.adjust_for_ambient_noise(fonte_de_audio)

            print("fale alguma coisa...")
            fala = reconhecedor.listen(fonte_de_audio, timeout = TEMPO_DE_ESCUTA, phrase_time_limit = TEMPO_DE_ESCUTA)

            tem_fala = True
        except Exception as e:
            print(f"erro escutando fala: {str(e)}")

    return tem_fala, fala

# traduz o audio da fala para uma string
def transcrever_fala(reconhecedor, fala):
    tem_transcricao, transcricao = False, None

    try:
        transcricao = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        transcricao = transcricao.lower()
        
        tem_transcricao = True
    except Exception as e:
        print(f"erro transcrevendo fala: {str(e)}")

    return tem_transcricao, transcricao

# 2. realiza o processamento de linguagem natural

# obtem tokens a partir da transcricao da fala
def obter_tokens(transcricao):
    return word_tokenize(transcricao)

# elimina as palavras de parada
def eliminar_palavras_de_parada(tokens, palavras_de_parada):
    tokens_filtrados = []

    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)

    return tokens_filtrados

# 3. validacao e execucao de comando do assistente

# valida o comando de acordo com o especificado no arquivo de configuracao
def validar_comando(tokens, nome_do_assistente, acoes):
    valido, acao, objeto = False, None, None

    # exemplo: joana ligar lampada
    if len(tokens) >= 3:
        if tokens[0] == nome_do_assistente:
            acao = tokens[1]
            objeto = tokens[2]

            for acao_prevista in acoes:
                if acao == acao_prevista["nome"]:
                    if objeto in acao_prevista["objetos"]:
                        valido = True

                        break

    return valido, acao, objeto

# executa o comando validado
def executar_comando(acao, objeto):
    print(f"executando a ação {acao} sobre {objeto}")

    for atuador in ATUADORES:
        parametro_de_atuacao = atuador["parametro_de_atuacao"]
        atuacao = atuador["atuar"]

        processo = Thread(target=atuacao, args=[acao, objeto, parametro_de_atuacao])
        processo.start()


# executando todos os passos em conjunto
if __name__ == "__main__":
    iniciado, reconhecedor, palavras_de_parada, nome_do_assistente, acoes = iniciar()

    if iniciado:
        while True:
            tem_fala, fala = escutar_fala(reconhecedor)
            if tem_fala:
                tem_transcricao, transcricao = transcrever_fala(reconhecedor, fala)
                if tem_transcricao:
                    print(f"usuário falou: {transcricao}")

                    tokens = obter_tokens(transcricao)
                    tokens = eliminar_palavras_de_parada(tokens, palavras_de_parada)

                    valido, acao, objeto = validar_comando(tokens, nome_do_assistente, acoes)
                    if valido:
                        executar_comando(acao, objeto)
                    else:
                        print("comando inválido, por favor, repita")