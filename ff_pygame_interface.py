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
               'Cyclops': 'images/cyclops_new.png',
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


# Add sprites to a sprite group. Add the sprite as an observer to the underlying
# game object
def setup_sprites(game_obj_list):
    sprite_group = pygame.sprite.Group()
    for obj in game_obj_list:
        sprite = GameSprite(obj)
        obj.attach(sprite)
        sprite_group.add(sprite)
    return sprite_group


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
    # Then redraw all the sprites taking into account any changes
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key in move_keys.keys():
                    # Move the current_pc
                    current_pc.move(move_keys[event.key], game)
                    # Show how many moves remain
                    print(f"You have {game.current_pc.moves_remaining} moves remaining")

                elif event.key == K_c:
                    current_pc.close_doors(game)

                elif event.key == K_o:
                    current_pc.open_doors(game)

                elif event.key == K_n:
                    # Change the current player to the next pc
                    game.next_player()
                    current_pc = game.current_pc
                    # Show how many moves remain
                    print(f"{current_pc.name}'s turn")
                    print(f"You have {current_pc.moves_remaining} moves remaining")

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
