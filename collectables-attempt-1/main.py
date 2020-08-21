import pygame
from sprites import *
from settings import *

vec = pygame.math.Vector2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Collectables attempt")
        self.clock = pygame.time.Clock()
        self.load()

    def load(self):
        self.map = TiledMap('resources/level6.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.Group()
        self.player_img = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (64, 64))
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(ITEM_IMAGES[item]).convert_alpha()

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name in ['coin']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)

        self.rect = self.player.get_rect()


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()

    def update(self):
        pass

    def draw(self):
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.left()
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
