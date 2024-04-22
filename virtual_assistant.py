# imports necessarios para o funcionamento do assistente
import speech_recognition as sr
from nltk import word_tokenize, corpus
from threading import Thread
import json

from financeiro import *

# configuracoes do assistente
CORPUS_LANGUAGE = "portuguese"
DEFAULT_LANGUAGE = "pt-BR"
CONFIG_FILE_PATH = "config.json"
LITENING_TIME = 5

ACTORS = [
    {
        "name": "financeiro",
        "initiate": create_finance_file,
        "acting_params": None,
        "acting": act_on_finance
    }
]

# configuracao para o assistente virtual iniciar
def initiate():
    deployed, recognizer, stopping_words, assistant_name, actions = False, None, None, None, None

    try:
        recognizer = sr.Recognizer()

        stopping_words = set(corpus.stopwords.words(CORPUS_LANGUAGE))

        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
            settings = json.load(file)

            assistant_name = settings["name"]
            actions = settings["actions"]

            file.close()

        for actor in ACTORS:
            actor_param = actor["initiate"]()
            actor["acting_params"] = actor_param

        deployed = True
    except Exception as e:
        print(f"erro iniciando o assistente: {str(e)}")

    return deployed, recognizer, stopping_words, assistant_name, actions

# realiza a captura da fala do usuario
def listen_line(recognizer):
    is_speaking, line = False, None

    with sr.Microphone() as audio_source:
        try:
            recognizer.adjust_for_ambient_noise(audio_source)

            print("fale alguma coisa...")
            line = recognizer.listen(audio_source, timeout=LITENING_TIME, phrase_time_limit=LITENING_TIME)

            is_speaking = True
        except Exception as e:
            print(f"erro escutando fala: {str(e)}")

    return is_speaking, line

# traduz o audio da fala para uma string
def write_line(recognizer, line):
    is_written, transcription = False, None

    try:
        transcription = recognizer.recognize_google(line, language=DEFAULT_LANGUAGE)
        transcription = transcription.lower()
        
        is_written = True
    except Exception as e:
        print(f"erro transcrevendo fala: {str(e)}")

    return is_written, transcription

# obtem tokens a partir da transcricao da fala
def get_tokens(transcription):
    return word_tokenize(transcription)

# elimina as palavras de parada
def remove_stopping_words(tokens, stopping_words):
    filtered_tokens = []
    for token in tokens:
        # Ignorar os caracteres 'r' e '$'
        if token.lower() not in ['r', '$'] and token not in stopping_words:
            filtered_tokens.append(token)
    return filtered_tokens

# valida o comando de acordo com o especificado no arquivo de configuracao
def validate_command(tokens, assistant_name, actions):
    is_valid, action, params = False, None, []

    if len(tokens) >= 3 and tokens[0] == assistant_name:
        action = tokens[1]
        params = tokens[2:]

        for anticipated_action in actions:
            if action == anticipated_action["name"]:
                parametros_esperados = anticipated_action["params"]

                if params[0] in parametros_esperados:  # Verificar se o primeiro parâmetro está contido nos parâmetros esperados
                    is_valid = True
                    break

    return is_valid, action, params

# executa o comando validado
def run_command(action, params):
    print(f"executando a ação {action} com os parâmetros {params}")

    for actor in ACTORS:
        acting_params = actor["acting_params"]
        acting = actor["acting"]

        process = Thread(target=acting, args=[action, params, acting_params])
        process.start()

# executando todos os passos em conjunto
if __name__ == "__main__":
    deployed, recognizer, stopping_words, assistant_name, actions = initiate()

    if deployed:
        while True:
            is_speaking, line = listen_line(recognizer)
            if is_speaking:
                is_written, transcription = write_line(recognizer, line)
                if is_written:
                    print(f"usuário falou: {transcription}")

                    tokens = get_tokens(transcription)
                    tokens = remove_stopping_words(tokens, stopping_words)
                    
                    valid, action, params = validate_command(tokens, assistant_name, actions)
                    if valid:
                        run_command(action, params)
                    else:
                        print("comando inválido, por favor, repita")