"""
# Criando os botões para o jogo, play, placar, vidas etc
#
"""
import pygame.font


class Button():
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # definindo as propriedades do botão
        self.width, self.height = 300, 70
        self.button_color = (104, 29, 41)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("fonts/space.ttf", 48)

        # construindo o botão centralizado
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # texto do botão
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # transforma o texto em imagem e centraliza no botão
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # desenha o botão e a mensagem
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
