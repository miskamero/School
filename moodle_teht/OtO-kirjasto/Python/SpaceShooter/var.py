import pygame

screen_width = 1280
screen_height = 720
camera_offset = pygame.math.Vector2(0, 0)

cooldown_time = 5
round = 0
start_round = False
difficulty = 10
difficulty_curve = 0.95

player_speed = 300
player_health = 1
player_max_health = 5

enemy_speed = 100
enemy_health = 1
enemy_max_health = 5

mouse_x = 0
mouse_y = 0
player_pos = pygame.math.Vector2()
enemy_spawn_offset = 100

ammo_max = 50
firerate_max = 0.1
reload_time_max = 2

coins = 0

# Dont change these
firerate = 0
reload_time = reload_time_max
ammo = ammo_max
ticks = 0
cooldown = 0
