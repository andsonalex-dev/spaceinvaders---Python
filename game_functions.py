import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, status, sb, play_button, nave, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, nave, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, nave)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, status, sb, play_button, nave, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, status, sb, play_button, nave, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not status.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        status.reset_stats()
        status.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_naves()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, nave, aliens)
        nave.center_nave()


def check_keydown_events(event, ai_settings, screen, nave, bullets):  # função ao pressionar a tecla
    if event.key == pygame.K_RIGHT:
        nave.moving_right = True
    elif event.key == pygame.K_LEFT:
        nave.moving_left = True
    # elif event.key == pygame.K_UP:
    #    nave.moving_top = True
    # elif event.key == pygame.K_DOWN:
    #    nave.moving_bottom = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, nave, bullets)  # chamando a função que dispara a bala
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, nave):  # função ao soltar a tecla
    if event.key == pygame.K_RIGHT:
        nave.moving_right = False
    elif event.key == pygame.K_LEFT:
        nave.moving_left = False
    # elif event.key == pygame.K_UP:
    #    nave.moving_top = False
    # elif event.key == pygame.K_DOWN:
    #    nave.moving_bottom = False


def update_screen(ai_settings, screen, status, sb, nave, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    # redesenha os projéteis atras da nave e dos aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    nave.blitme()
    # alien.blitme()  # chamava um alien
    aliens.draw(screen)  # chama vários aliens
    # Desenha o botão Play se o jogo estiver inativo
    sb.show_score()
    if not status.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen, status, sb, nave, aliens, bullets):
    # Atualiza as posições dos projéteis
    bullets.update()
    # apagando as balas que desaparecem da tela
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, status, sb, nave, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, status, sb, nave, aliens, bullets):
    # verificando se a colisão entre a tiro e a nave alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:  # toca um som de explosão quando atingi a nave alien
        for aliens in collisions.values():
            status.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(status, sb)
        explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
        pygame.mixer.Sound.play(explosion_sound)
    if len(aliens) == 0:  # quando acabar a frota, ele cria uma nova
        bullets.empty()
        ai_settings.increase_speed()
        status.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, nave, aliens)


def fire_bullet(ai_settings, screen, nave, bullets):
    # função para disparo das balas
    # Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(bullets) < ai_settings.bullets_allowed:  # verifico se a quantidade de disparos foi atingida
        new_bullet = Bullet(ai_settings, screen, nave)
        bullets.add(new_bullet)


def qtd_aliens_x(ai_settings, alien_width):  # função para fazer o cálculo do numero de alienas
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


#  numero de linhas para cada alien

def get_number_rows(ai_settings, nave_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - nave_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_fleet(ai_settings, screen, nave, aliens):
    #  Cria um alienígena e calcula o número de alienígenas em uma linha
    #  O espaçamento entre os alienígenas é igual à largura de um alienígena
    alien = Alien(ai_settings, screen)
    number_aliens_x = qtd_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, nave.rect.height, alien.rect.height)
    #  laço para criar mais aliens
    for row_number in range(number_rows):
        #  laço para criar a linha
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():  # verifica se atingiu a borda
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():  # faz a frota descer e muda a direção
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, screen, status, sb, nave, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(nave, aliens):
        nave_hit(ai_settings, status, screen, sb, nave, aliens, bullets)  # chamando a função nave_hit
    check_aliens_bottom(ai_settings, status, screen, sb, nave, aliens, bullets)


#  função para detectar nave atingida
#  toda vez que a nave for atingida
#  ele zera as naves inimigas, zera as balas
#  cria uma nova frota de naves
#  reposiciona nossa nave
#  dá uma pausa automática
def nave_hit(ai_settings, status, screen, sb, nave, aliens, bullets):
    if status.naves_left > 0:

        # Decrementa ships_left
        status.naves_left -= 1
        sb.prep_ships()
        # esvazia os aliens e as balas
        aliens.empty()
        bullets.empty()
        # cria nova frota de aliens
        create_fleet(ai_settings, screen, nave, aliens)
        nave.center_nave()
        # faz uma pausa rápida
        sleep(0.5)  # utilizando a função time sleep
    else:
        status.game_active = False
        pygame.mouse.set_visible(True)


# Função para checar se os aliens alcanção a borda inferior
def check_aliens_bottom(ai_settings, status, screen, sb, nave, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            nave_hit(ai_settings, status, screen, sb, nave, aliens, bullets)
            break


# checando se há uma pontuação máximo
def check_high_score(status, sb):
    if status.score > status.high_score:
        status.high_score = status.score
        sb.prep_high_score()
