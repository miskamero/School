import pygame
import math, functions, var, roundsys
from enemy import Enemy
from player import Player
# Initialize pygame
pygame.init()
# SETUP PYGAME VARIABLES
clock = pygame.time.Clock()
dt = clock.tick(var.FPS) / 1000

# Set up the display
fullscreen = pygame.FULLSCREEN
screen = pygame.display.set_mode((var.screen_width, var.screen_height), pygame.DOUBLEBUF)
pygame.display.set_caption("PIG Defenders")

# Load SPRITES
enemies = []
bullets = []

# PLAYER
player = Player(var.screen_width / 2,
                       var.screen_height / 2, 300, "img/räkä alus.png", var.player_health)

# BG
bg_image = pygame.image.load("img/bg_space.png").convert()
bg_image = pygame.transform.scale(
    bg_image, (var.screen_width*2.3, var.screen_height*2.3))
bg_rect = bg_image.get_rect()
bg_rect.center = (var.screen_width, var.screen_height)

# Crosshair
crosshair_image = pygame.image.load("img/crosshair.png")
crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))

# ENEMY
def spawn_enemy():
    enemies.append(Enemy(*functions.spawn_enemy(), var.enemy_speed, "img/enemy.png", 100, 1, 10))
def spawn_enemies(num):
    for _ in range(num):
        spawn_enemy()

def draw_health_bar(screen, current_health, max_health):
    bar_width = int((current_health / max_health) * 200)
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (50, 50, bar_width, 20))

def draw_enemy_health_bar(screen, current_health, max_health, enemy):
    offset_x = -30
    offset_y = 80
    width = 25
    height = 5
    bar_width = int((current_health / max_health) * width)
    pygame.draw.rect(screen, (255, 0, 0), (enemy.x - offset_x +
                     var.camera_offset.x, enemy.y + var.camera_offset.y + offset_y, width, height))
    pygame.draw.rect(screen, (0, 255, 0), (enemy.x - offset_x + var.camera_offset.x,
                     enemy.y + offset_y + var.camera_offset.y, bar_width, height))


# Game loopww
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))
    if var.game_running:
        # Draw the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.y > 0: # UP
            player.y -= player.speed * dt
        if keys[pygame.K_s] and player.y < var.screen_height: # DOWN
            player.y += player.speed * dt
        if keys[pygame.K_a] and player.x > 0: # LEFT
            player.x -= player.speed * dt
        if keys[pygame.K_d] and player.x < var.screen_width: # RIGHT
            player.x += player.speed * dt
        if keys[pygame.K_r] and var.ammo != var.ammo_max:
            var.ammo = 0
        if keys[pygame.K_o]:
            healthed = player.get_health() - 1
            player.set_health(healthed)
        if keys[pygame.K_1]:
            # set bullets to mk5
            for bullet in bullets:
                bullet.set_upgrade("raka_ase", "MK1")
            
        if keys[pygame.K_2]:
            # set bullets to mk5
            for bullet in bullets:
                bullet.set_upgrade("raka_ase", "MK2")
        # Get mouse position
        var.mouse_x, var.mouse_y = pygame.mouse.get_pos()

        # rotate the player to face the mouse
        player_to_mouse_x = var.mouse_x - player.x
        player_to_mouse_y = var.mouse_y - player.y
        angle = math.atan2(player_to_mouse_y, player_to_mouse_x)
        angle = math.degrees(angle)
        rotated_player = pygame.transform.rotate(player.image, -angle)
        player.rect = rotated_player.get_rect(center=(player.x, player.y))
        
        # SHOOT
        if pygame.mouse.get_pressed()[0] and not var.buy_round:
            if var.firerate <= 0 and var.ammo > 0:
                var.firerate = var.firerate_max
                var.ammo -= 1
                bullets.append(player.shoot(angle))
                             
        # CAMERA OFFSET
        var.camera_offset = pygame.math.Vector2(
            var.screen_width // var.play_area - player.x, var.screen_height // var.play_area - player.y)
        
        # DRAW SPRITES
        screen.blit(bg_image, (bg_rect.x + var.camera_offset.x, bg_rect.y + var.camera_offset.y))

        for bullet in bullets:
            bullet.draw(screen)
            bullet.update(dt)

            for _enemy_ in enemies:
                # if bullet plus camera_offset collides with enemy, remove bullet and enemy
                bullet_rect = bullet.get_rect()
                enemy_rect = _enemy_.get_rect()
                if bullet_rect.colliderect(enemy_rect):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if _enemy_.hitted(bullet.get_damage()):
                        enemies.remove(_enemy_)
                    break


        # detect collision between player and enemy
        for _enemy_ in enemies:
            # if enemy plus camera_offset is near player_pos, remove enemy
            enemy_y = _enemy_.get_y()
            enemy_x = _enemy_.get_x()
            player_y = var.player_pos.y
            player_x = var.player_pos.x
            if math.sqrt((enemy_x - player_x)**2 + (enemy_y - player_y)**2) < 90 and var.invincibility_time <= 0:
                enemies.remove(_enemy_)
                if player.hitted(_enemy_.get_damage()):
                    var.game_running = False
                    print("GAME OVER")
        
        if player.is_dead():
            var.game_running = False
            print("GAME OVER")
            
        # FOREGROUND
        draw_health_bar(screen, player.get_health(), player.get_max_health())
        for _enemy_ in enemies:
            # update and draw, but make sure that enemys cannot overlap with each other
            _enemy_.update(dt, enemies)
            _enemy_.draw(screen)
            draw_enemy_health_bar(screen, _enemy_.get_health(), _enemy_.get_max_health(), _enemy_)
                
        if var.invincibility_time > 0:
            # flash the player
            if var.invincibility_time % 0.1 < 0.05:
                player.draw(screen, player.rect, rotated_player)
        else:
            player.draw(screen, player.rect, rotated_player)

        # BUY ROUND
        if var.buy_round:       
            functions.buy_menu(screen)            
        else:
            pygame.mouse.set_visible(False)
            screen.blit(crosshair_image, (var.mouse_x - crosshair_image.get_width() / 2, var.mouse_y - crosshair_image.get_height() / 2))
        
        # # DEBUG
        # # draw rect around player
        # pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
        # # draw players center
        # pygame.draw.circle(screen, (255, 0, 0), player.get_center(), 2)
        # # draw rect around enemy
        # for _enemy_ in enemies:
        #     pygame.draw.rect(screen, (255, 0, 0), _enemy_.rect, 2)

        # # draw rect around bullet
        # for bullet in bullets:
        #     pygame.draw.rect(screen, (255, 0, 0), bullet.rect, 2)
        #     pygame.draw.circle(screen, (255, 0, 0), bullet.get_center(), 2)

        # INVICIBILITY
        if var.invincibility_time > 0:
            var.invincibility_time -= dt
        
            
        # FIRERATE
        var.firerate -= dt
        # RELOAD
        if var.ammo <= 0:
            var.reload_time -= dt
            if var.reload_time <= 0:
                var.ammo = var.ammo_max
                var.reload_time = var.reload_time_max

        # ROUND SYSTEM
        if var.start_round and not var.buy_round:
            if var.ticks >= var.cooldown + var.cooldown_time:
                prev_ticks = var.ticks
                var.start_round = False
                roundsys.calculate_difficulty()
                roundsys.calculate_enemy_spawn_amount()
                spawn_enemies(roundsys.calculate_enemy_spawn_amount())
                print("\nRound: ", var.round, " >> Difficulty: ", var.difficulty, " >> Enemy Spawn Amount: ", roundsys.calculate_enemy_spawn_amount())

        # Update the display
        dt = clock.tick(var.FPS) / 1000
        var.ticks += 1 / var.FPS
        pygame.display.set_caption("PIG Defenders - Ticks: " + 
                                   str(round(var.ticks))+ " FPS: " + 
                                   str(round(clock.get_fps())) + " Invincibility: " + 
                                   str(round(var.invincibility_time, 2)) + " Round: " + 
                                   str(var.round) + " Difficulty: " + str(var.difficulty) + 
                                   " Enemy Spawn Amount: " + str(roundsys.calculate_enemy_spawn_amount()) + 
                                   " Health: " + str(player.get_health()) + " Ammo: " + str(var.ammo) + 
                                   " Firerate: " + str(var.firerate_max) + " Reload Time: " +
                                   str(round(var.reload_time)) + " Coins: " + str(var.coins))
        roundsys.check_round(enemies)
    else:
        pygame.mouse.set_visible(True)
        # DRAW MENU
        screen.fill((34, 0, 0))
        functions.buy_menu(screen, player, enemies, bullets)
        
        
    pygame.display.flip()

# Quit the game
pygame.quit()
