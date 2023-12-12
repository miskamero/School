import pygame

screen_width = 1280
screen_height = 720
camera_offset = pygame.math.Vector2(0, 0)

cooldown_time = 0.2
round = 2
start_round = False
difficulty = 1
difficulty_curve = 0.6

player_speed = 130
player_health = 100
player_max_health = 5

enemy_speed = 80
enemy_max_health = 5

mouse_x = 0
mouse_y = 0
player_pos = pygame.math.Vector2()
enemy_spawn_offset = 500
FPS = 144
play_area = 10
game_running = False # False when player dies, showing the menu
buy_rounds = [3, 6, 10, 15, 20, 25, 30, 35, 40, 45, 50]
buy_round = False

ammo_max = 20
ammo_max_limit = 100
firerate_max = 0.05
firerate_max_limit = 0.0
reload_time_max = 0
reload_time_max_limit = 1
gun_damage = 30
gun_damage_max_limit = 100

invincibility_time_max = 1
invincibility_time_max_limit = 3
player_health_max_limit = 200
coins = 100000

# Dont change these
firerate = 0
reload_time = reload_time_max
ammo = ammo_max
ticks = 0
cooldown = 0
invincibility_time = 0
start_new_round_in_the_main_menu = False

raka_ase = {
    "MK1": {"Damage": 20, "Fire Rate": 0.5, "Reload Time": 5, "Magazine Size": 10, "Cost": None},
    "MK2": {"Damage": 30, "Fire Rate": 0.4, "Reload Time": 4, "Magazine Size": 20, "Cost": 50},
    "MK3": {"Damage": 40, "Fire Rate": 0.3, "Reload Time": 3, "Magazine Size": 30, "Cost": 100},
    "MK4": {"Damage": 50, "Fire Rate": 0.2, "Reload Time": 2, "Magazine Size": 40, "Cost": 150},
    "MK5": {"Damage": 60, "Fire Rate": 0.1, "Reload Time": 1, "Magazine Size": 50, "Cost": 200},
}

kakku_sinko = {
    "MK1": {"Damage": 50, "Fire Rate": 2.0, "Reload Time": 5, "Magazine Size": 3, "Cost": None},
    "MK2": {"Damage": 60, "Fire Rate": 1.8, "Reload Time": 4.5, "Magazine Size": 4, "Cost": 50},
    "MK3": {"Damage": 70, "Fire Rate": 1.6, "Reload Time": 4, "Magazine Size": 5, "Cost": 100},
    "MK4": {"Damage": 80, "Fire Rate": 1.4, "Reload Time": 3.5, "Magazine Size": 6, "Cost": 150},
    "MK5": {"Damage": 90, "Fire Rate": 1.2, "Reload Time": 3, "Magazine Size": 7, "Cost": 200},
}