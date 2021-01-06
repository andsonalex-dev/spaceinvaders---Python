"""
# Classe para atribuir os pontos do jogador

"""
import pygame.font
from pygame.sprite import Group
from nave import Nave



class Scoreboard():
    def __init__(self, ai_settings, screen, status):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = status
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("fonts/space.ttf", 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_naves()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        # nível do jogador
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_naves(self):
        # Exibe a quantidade de 'vidas' restante da nave
        self.naves = Group()
        for nave_number in range(self.stats.naves_left):
            nave = Nave(self.ai_settings, self.screen)
            nave.rect.x = 10 + nave_number * nave.rect.width
            nave.rect.y = 10
            self.naves.add(nave)

    def show_score(self):
        # Desenha a pontuação na tela.
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.naves.draw(self.screen)
