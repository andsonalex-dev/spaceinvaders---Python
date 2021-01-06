"""
#Classe que vai administrar as balas, projéteis
#space invaders

"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, nave):
        # Cria um objeto para o projétil na posição atual da nave.
        super(Bullet, self).__init__()
        self.screen = screen
        # Cria um retângulo para o projétil em (0, 0) e, em seguida, define a posição correta
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = nave.rect.centerx
        self.rect.top = nave.rect.top
        # Armazena a posição da bala com um valor float
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        # som do disparo
        disparo_sound = pygame.mixer.Sound("sounds/shot.mp3")
        pygame.mixer.Sound.play(disparo_sound)

    def update(self):
        #
        # Atualiza a posição decimal do projétil
        self.y -= self.speed_factor
        # Atualiza a posição de rect
        self.rect.y = self.y

    def draw_bullet(self):
        # Desenha o projétil na tela.
        pygame.draw.rect(self.screen, self.color, self.rect)
