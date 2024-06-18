import random
from csv import reader
from itertools import cycle
from typing import List
from ff_game_objects import GameObj, Character, NPChar, PChar


class FFgame:
    def __init__(self):
        self.pcs: List[Character] = [PChar('Dwarf', pos=[7, 15]), PChar('Knight', pos=[8, 15])]
        self.npcs: List[Character] = [NPChar(6, 6, 'Goblin', pos=[2, 2]),
                                      NPChar(10, 8, 'Dragon', pos=[3, 8]),
                                      NPChar(9, 16, 'Cyclops', pos=[13, 1]),
                                      NPChar(8, 16, 'Cyclops', pos=[12, 1]),
                                      ]
        self.game_objects: List[Character] = self.pcs + self.npcs
        self.pc_cycle = cycle(self.pcs)
        self.current_pc = next(self.pc_cycle)
        self.floor_plan = self.open_floor_plan("floor_plan.csv")
        self.max_pos = self.floor_plan[-1].pos

    @staticmethod
    def open_floor_plan(filename):
        # Reads a csv floor plan into a list of lists - with automatically closes the file on completion.
        with open(filename, 'r') as f:
            floor_plan_reader = reader(f)
            # List comprehension loops through lines in the floor_plan_file and objects in the line
            # and adds a game object with the correct name and position to the floor_plan list
            floor_plan = [GameObj(obj, pos=[i, j])
                          for j, line in enumerate(floor_plan_reader)
                          for i, obj in enumerate(line)]

        return floor_plan

    @staticmethod
    def get_obj_in_loc(obj_list, pos):
        objects_in_pos = [obj for obj in obj_list if obj.pos == pos]
        return objects_in_pos

    def get_floor(self, pos):
        floor = self.get_obj_in_loc(self.floor_plan, list(pos))
        if floor:
            floor = floor[0]
        return floor

    # Finds a list of adjacent positions
    def find_adjacent(self, pos):
        one_away = {(i, j)
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not [i, j] == [0, 0]}
        adj_pos = {(pos[0] + i, pos[1] + j)
                   for i, j in one_away
                   if (0 <= pos[0] + i <= self.max_pos[0]
                   and 0 <= pos[1] + j <= self.max_pos[1])}
        return adj_pos

    # Cycles onto the next player
    def next_player(self):
        self.current_pc = next(self.pc_cycle)
        self.current_pc.moves_remaining = random.randint(1, 6)

    # character interacts with objects in position pos
    def interact(self, character: Character, pos):
        for pc in [pc for pc in self.pcs if pc.pos == pos]:
            print(f"{character.name} has met {pc.name}")
        for npc in [npc for npc in self.npcs if npc.pos == pos]:
            print(f"{character.name} has met a {npc.name}")

    def toggle_door(self, pos):
        floor_obj = self.get_obj_in_loc(self.floor_plan, pos)[0]
        if floor_obj.name == "O":
            floor_obj.name = "D"
        elif floor_obj.name == "D":
            floor_obj.name = "O"


if __name__ == '__main__':
    current_game = FFgame()
