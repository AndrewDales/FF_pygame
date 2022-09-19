import pygame
from pygame.sprite import Sprite

from ff_main_game import FFgame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_n,
    K_c,
    K_o,
    KEYDOWN,
    QUIT,
)

WIDTH = 512
HEIGHT = 512
SQ_SIZE = 32

image_files = {'Dwarf': 'images/dwarf_new.png',
               'Knight': 'images/knight.png',
               'Goblin': 'images/goblin_old.png',
               'Dragon': 'images/dragon.png',
               'W': 'images/wall.png',
               'F': 'images/floor.png',
               'D': 'images/closed_door.png',
               'O': 'images/open_door.png'}


class GameSprite(Sprite):
    def __init__(self, game_obj):
        super().__init__()
        self.image = pygame.image.load(image_files[game_obj.name])
        self.screen_pos = [SQ_SIZE * x + SQ_SIZE // 2 for x in game_obj.pos]
        self.rect = self.image.get_rect(center=self.screen_pos)

    def update(self, game_obj):
        self.image = pygame.image.load(image_files[game_obj.name])
        self.rect.center = [SQ_SIZE * x + SQ_SIZE // 2 for x in game_obj.pos]


class CharSprite(GameSprite):
    def __init__(self, char):
        super().__init__(char)
        self.char = char

    def __call__(self):
        self.rect.center = [SQ_SIZE * x + SQ_SIZE // 2 for x in self.char.pos]


def setup_char_sprites(char_group):
    character_sprites = pygame.sprite.Group()
    for char in char_group.values():
        char_sprite = GameSprite(char)
        # Sets pc_sprite as an observer of pc - the sprite __call__ function will be triggered if the pc moves
        char.attach(char_sprite)
        character_sprites.add(char_sprite)
    return character_sprites


def setup_sprites(floor_plan):
    background_sprites = pygame.sprite.Group()
    for bg_obj in floor_plan:
        bg_sprite = GameSprite(bg_obj)
        bg_obj.attach(bg_sprite)
        background_sprites.add(bg_sprite)
    return background_sprites


def main():
    game = FFgame()
    current_pc = game.current_pc

    pc_sprites = setup_sprites(game.pcs)
    npc_sprites = setup_sprites(game.npcs)
    background_sprites = setup_sprites(game.floor_plan)

    move_keys = {K_UP: 'n', K_DOWN: 's', K_LEFT: 'w', K_RIGHT: 'e'}
    pygame.init()
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Fighting Fantasy")
    clock = pygame.time.Clock()

    # Game loop - checks for keypress events and runs the appropriate game method
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key in move_keys.keys():
                    # Move the current_pc
                    current_pc.move(move_keys[event.key], game)

                elif event.key == K_c:
                    current_pc.close_doors(game)

                elif event.key == K_o:
                    current_pc.open_doors(game)

                elif event.key == K_n:
                    # Change the current player to the next pc
                    game.next_player()
                    current_pc = game.current_pc

                elif event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

        # Fill in the background - covers up sprite images that are no longer current
        game_display.fill((55, 55, 55))

        # Draw the background
        background_sprites.draw(game_display)

        # Draw the character sprites
        npc_sprites.draw(game_display)
        pc_sprites.draw(game_display)

        # Update the display
        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    main()
