import pygame, pytmx
from sprites2 import *
import sprites2
from settings import *


class Game(object):
    def __init__(self):
        # Set up a level to load
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName="resources/level6.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]

        # Create a player object and set the level it is in
        self.player = Player(x=300, y=100)
        self.player.currentLevel = self.currentLevel


        """self.background = pygame.image.load("resources/background.png")"""

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # Get keyboard input and move player accordingly
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.goLeft()
                elif event.key == pygame.K_RIGHT:
                    self.player.goRight()
                elif event.key == pygame.K_UP:
                    self.player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.changeX < 0:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT and self.player.changeX > 0:
                    self.player.stop()

        return False

    def update(self):
        # Update player movement and collision logic
        self.player.update()

    # Draw level, player, overlay
    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()

def main():
    pygame.init()

    """screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)"""
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Base code")
    clock = pygame.time.Clock()
    done = False
    game = Game()

    while not done:
        done = game.events()
        game.update()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()


main()