"""
Clase da nave, inicializa ela e define sua posição
"""
import pygame
from pygame.sprite import Sprite


class Nave(Sprite):
    def __init__(self, ai_settings, screen):
        super(Nave, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # carregando a imagem
        self.image = pygame.image.load('images/nave.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # carregando o som inicial
        pygame.mixer.music.load('sounds/musica-fundo.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        # inicia a nave na parte central da tela
        self.rect.centerx = self.screen_rect.centerx
        # self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom

        # valor decimal para o centro da nave

        self.center = float(self.rect.centerx)
        # self.centery = float(self.rect.centery)

        # movimento
        self.moving_right = False
        self.moving_left = False
        # self.moving_top = False
        # self.moving_bottom = False

    def update(self):
        # Atualiza o valor do centro da nave
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.nave_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.nave_speed_factor
        #  if self.moving_top and self.rect.top > 0:
        #    self.centery -= self.ai_settings.nave_speed_factor
        #  if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
        #    self.centery += self.ai_settings.nave_speed_factor

        # Atualiza o objeto rect de acordo com self.center
        self.rect.centerx = self.center
        # self.rect.centery = self.centery

    def blitme(self):
        # desenha a nave na posição atual
        self.screen.blit(self.image, self.rect)

    def center_nave(self):
        self.center = self.screen_rect.centerx
