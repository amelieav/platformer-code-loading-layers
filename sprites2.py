# imports
import pygame
import pytmx
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load the spritesheet of frames for this player
        self.sprites = SpriteSheet("resources/player.png")


        # List of frames for each animation

        self.stillRight = self.sprites.image_at((0, 0, 64, 64))
        self.stillLeft = self.sprites.image_at((0, 0, 64, 64))

        # List of frames for each animation

        self.runningRight = (self.sprites.image_at((128, 0, 64, 64)),
                            self.sprites.image_at((128, 0, 64, 64)),
                            self.sprites.image_at((64, 0, 64, 64)),
                             self.sprites.image_at((64, 0, 64, 64)),
                             self.sprites.image_at((64, 0, 64, 64)))

        self.runningLeft = (self.sprites.image_at((128, 128, 64, 64)),
                            self.sprites.image_at((128, 128, 64, 64)),
                            self.sprites.image_at((64, 128, 64, 64)),
                             self.sprites.image_at((64, 128, 64, 64)),
                             self.sprites.image_at((64, 128, 64, 64)))

        self.jumpingRight = (self.sprites.image_at((0, 64, 64, 64)),
                            self.sprites.image_at((64, 64, 64, 64)),
                            self.sprites.image_at((128, 64, 64, 64)))

        self.jumpingLeft = (self.sprites.image_at((0, 64, 64, 64)),
                            self.sprites.image_at((64, 64, 64, 64)),
                            self.sprites.image_at((128, 64, 64, 64)))

        """self.runningRight = (self.sprites.image_at((0, 61, 30, 30)),
                             self.sprites.image_at((32, 61, 30, 30)),
                             self.sprites.image_at((65, 61, 30, 30)),
                             self.sprites.image_at((95, 61, 30, 30)))

        self.runningLeft = (self.sprites.image_at((0, 127, 30, 30)),
                             self.sprites.image_at((32, 127, 30, 30)),
                             self.sprites.image_at((65, 127, 30, 30)),
                             self.sprites.image_at((95, 127, 30, 30)))

        self.jumpingRight = (self.sprites.image_at((0, 32, 30, 30)),
                             self.sprites.image_at((65, 0, 30, 30)),
                             self.sprites.image_at((0, 32, 30, 30)))

        self.jumpingLeft = (self.sprites.image_at((30, 42, 30, 42)),
                            self.sprites.image_at((60, 42, 30, 42)),
                            self.sprites.image_at((90, 42, 30, 42)))"""



        self.image = self.stillRight

        # Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"

        # Boolean to check if player is running, current running frame, and time since last frame change
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # Players current level, set after object initialized in game constructor
        self.currentLevel = None

    def update(self):
        # Update player position by change
        self.rect.x += self.changeX

        # Get tiles in collision layer that player is now touching
        hitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # Move player to correct side of that block
        for tile in hitList:
            if self.changeX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right

        # Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - 400:
            difference = self.rect.right - (SCREEN_WIDTH - 400)
            self.rect.right = SCREEN_WIDTH - 400
            self.currentLevel.shiftLevel(-difference)

        # Move screen is player reaches screen bounds
        if self.rect.left <= 400:
            difference = 400 - self.rect.left
            self.rect.left = 400
            self.currentLevel.shiftLevel(difference)

        # Update player position by change
        self.rect.y += self.changeY

        # Get tiles in collision layer that player is now touching
        hitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # If there are tiles in that list
        if len(hitList) > 0:
            # Move player to correct side of that tile, update player frame
            for tile in hitList:
                if self.changeY > 0:
                    self.rect.bottom = tile.rect.top
                    self.changeY = 1

                    if self.direction == "right":
                        self.image = self.stillRight
                    else:
                        self.image = self.stillLeft
                else:
                    self.rect.top = tile.rect.bottom
                    self.changeY = 0
        # If there are not tiles in that list
        else:
            # Update player change for jumping/falling and player frame
            self.changeY += 0.2
            if self.changeY > 0:
                if self.direction == "right":
                    self.image = self.jumpingRight[1]
                else:
                    self.image = self.jumpingLeft[1]

        # If player is on ground and running, update running animation
        if self.running and self.changeY == 1:
            if self.direction == "right":
                self.image = self.runningRight[self.runningFrame]
            else:
                self.image = self.runningLeft[self.runningFrame]

        # When correct amount of time has passed, go to next frame
        if pygame.time.get_ticks() - self.runningTime > 130:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 3:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

    # Make player jump
    def jump(self):
        # Check if player is on ground
        self.rect.y += 2
        hitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(hitList) > 0:
            if self.direction == "right":
                self.image = self.jumpingRight[0]
            else:
                self.image = self.jumpingLeft[0]
            """
            change value for Y for a jump boost
            """
            self.changeY = -9

    # Move right
    def goRight(self):
        self.direction = "right"
        self.running = True
        self.changeX = 3

    """
    change the values for x for a speed boost
    """


    # Move left
    def goLeft(self):
        self.direction = "left"
        self.running = True
        self.changeX = -3

    # Stop moving
    def stop(self):
        self.running = False
        self.changeX = 0

    # Draw player
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Sprite sheet class to load sprites from player spritesheet

class SpriteSheet(object):
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName).convert()
        self.sheet.set_colorkey(WHITE)


    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image


class Level(object):
    def __init__(self, fileName):
        # Create map object from PyTMX
        self.mapObject = pytmx.load_pygame(fileName)

        # Create list of layers for map
        self.layers = []
        self.coin_layer = []
        # Amount of level shift left/right
        self.levelShift = 0

        # Create layers for each layer in tile map
        for layer in range(len(self.mapObject.layers)):
            """if isinstance(layer, pytmx.TiledTileLayer):
                print("Tile layer")
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "coin":
                    for object in layer:
                        self.coin.layer.append(object.x, object.y)"""
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

    # Move layer left/right
    def shiftLevel(self, shiftX):
        self.levelShift += shiftX

        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX

    # Update layer
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)



class Layer(object):
    def __init__(self, index, mapObject):
        # Layer index from tiled map
        self.index = index

        # Create group of tiles for this layer
        self.tiles = pygame.sprite.Group()
        self.coin_tiles = pygame.sprite.Group()

        # Reference map object
        self.mapObject = mapObject

        self.img = pygame.image.load('resources/coin.png').convert()
        self.img = pygame.transform.scale(self.img, (64,64))
        # Create tiles in the right position for each layer

        for layer in mapObject.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    if tile:
                        self.tiles.add(Tile(image=self.img, x=(x * self.mapObject.tilewidth), y=(y * self.mapObject.tileheight)))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer == "coin":
                    for x, y, tile in layer.tiles():
                        if tile:
                            self.coin_tiles.add(Tile(image=self.img, x=(object.x), y=(object.y)))




    # Draw layer
    def draw(self, screen):
        self.tiles.draw(screen)
        self.coin_tiles.draw(screen)


# Tile class with an image, x and y
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y