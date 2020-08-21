import pygame

# Background color
BACKGROUND = (20, 20, 100)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Tiled map layer of tiles that you collide with
MAP_COLLISION_LAYER = 1

WHITE = (255,255,255)



TILESIZE = 64

PLAYER_LAYER = 3
ITEMS_LAYER = 2

PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)

ITEM_IMAGES = {'coin': 'resources/coin.png'}

PLAYER_IMG = 'resources/player.png'

COIN_ITEM = 'resources/coin.png'

# https://www.youtube.com/watch?v=IZgSacaiFXU&feature=youtu.be