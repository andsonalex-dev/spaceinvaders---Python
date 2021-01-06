"""
# Criando um joguinho simples, testando bibliotecas
# importando sys e pygame
# Baseado no clássico Space Invaders
"""
import sys
import pygame  # biblioteca pygame
import game_functions as gf  # importando as funções
from settings import Settings  # importando as configurações
from game_status import GameStatus  # importando os status do jogo
from nave import Nave  # importando a nave
from button import Button  # importando o botão do play
from scoreboard import Scoreboard  # importando o score
from pygame.sprite import Group  # sprite nativo


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))  # definindo resolução ou tamanho da janela
    pygame.display.set_caption("Space Invaders By Andson de Oliveira")  # titulo
    # chamando a pontuação
    status = GameStatus(ai_settings)
    sb = Scoreboard(ai_settings, screen, status)
    # criando o botão e atribuindo o texto
    play_button = Button(ai_settings, screen, "Iniciar")
    # cria a nave
    nave = Nave(ai_settings, screen)
    # cria as balas
    bullets = Group()
    aliens = Group()
    # cria o alien
    # alien = Alien(ai_settings, screen)
    # cria uma linha de aliens
    gf.create_fleet(ai_settings, screen, nave, aliens)

    # iniciando o laço principal
    while True:
        gf.check_events(ai_settings, screen, status, sb, play_button, nave, aliens, bullets)
        gf.update_screen(ai_settings, screen, status, sb, nave, aliens, bullets, play_button)
        if status.game_active:
            nave.update()
            gf.update_bullets(ai_settings, screen, status, sb, nave, aliens, bullets)
            gf.update_aliens(ai_settings, screen, status, sb, nave, aliens, bullets)


# iniciando o jogo
run_game()
