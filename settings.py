"""
Classe para armazenar as configurações
"""


class Settings():
    def __init__(self):
        # Configurações da tela
        self.screen_width = 1600
        self.screen_height = 1000
        self.bg_color = (73, 41, 163)  # rgb
        # Configração da Nave
        # self.nave_speed_factor = 3  # velocidade de deslocamento, 1,5 pixels
        self.nave_limit = 3
        # Configurações dos projéteis
        # self.bullet_speed_factor = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255  # rgb
        self.bullets_allowed = 2  # limitando os disparos
        # Configurações dos alienígenas
        # self.alien_speed_factor = 3
        self.fleet_drop_speed = 10
        # fleet_direction igual a 1 representa a direita; -1 representa a esquerda
        # self.fleet_direction = 1
        # nova forma de controlar a velocidade
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.nave_speed_factor = 1.8
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.nave_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
