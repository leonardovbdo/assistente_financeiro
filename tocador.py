import pygame

MUSICA = "la belle de jour.mp3"

def iniciar_tocador(musica=MUSICA):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(musica)

    return None

def atuar_sobre_tocador(acao, objeto, _):
    if acao == "tocar" and objeto == "música":
        print("tocando a música")
        pygame.mixer.music.play()
    elif acao == "parar" and objeto == "música":
        print("parando a música")
        pygame.mixer.music.stop()