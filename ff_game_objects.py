from random import randint


class GameObj:
    def __init__(self, name, pos=None):
        self._observers = []
        self._name = name
        self._pos = pos

    def __str__(self):
        return self.name

    # Allows _observers (graphic sprites) to be attached to a GameObj
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    # Set name and pos as properties which, if changed, will allow the _observers, which will be sprites
    # referencing the GameObj to be updated.
    @property
    def name(self):
        return self._name

    # Code is run when the .name property of GameObj is changed
    @name.setter
    def name(self, value):
        self._name = value
        self._update_observers()

    @property
    def pos(self):
        return self._pos

    # Code is run when the .setter property of GameObj is changed
    @pos.setter
    def pos(self, value):
        self._pos = value
        self._update_observers()

    def _update_observers(self):
        for observer in self._observers:
            observer.update(self)


class Character(GameObj):
    directions = {"n": (0, -1), "e": (1, 0), "s": (0, 1), "w": (-1, 0)}

    def __init__(self, skill, stamina, name, pos=None):
        super().__init__(name, pos)
        self.skill = skill
        self.stamina = stamina

    def __str__(self):
        return f'{self.name}\nSkill: {self.skill}\nStamina: {self.stamina}'

    def move(self, move_dir: str, game):
        """
        param move_dir: string
        type game: FFGame
        """
        move_vec = self.directions[move_dir]
        # Add the move_vec to the current position
        new_pos = [sum(coords) for coords in zip(self.pos, move_vec)]

        # Check for game objects at the new location
        if game.get_obj_in_loc(game.game_objects, new_pos):
            game.interact(self, new_pos)

        else:
            floor_type = game.get_floor(new_pos)
            # if the floor type is a wall (W), don't move, if it is a closed door (D), open the door, else allow the
            # move.
            if not floor_type or floor_type.name == "W":
                pass
            elif floor_type and floor_type.name == "D":
                game.toggle_door(new_pos)
            else:
                self.pos = new_pos
        return self.pos


class PChar(Character):
    def __init__(self, name, pos=None):
        skill = 6 + randint(1, 6)
        stamina = 12 + randint(1, 6) + randint(1, 6)
        super().__init__(skill, stamina, name, pos)
        self.color = [255, 0, 0]

    def open_doors(self, game):
        adj_cells = game.find_adjacent(self.pos)
        for cell in adj_cells:
            fp = game.get_floor(cell)
            if fp.name == "D":
                game.toggle_door(fp.pos)

    def close_doors(self, game, ):
        adj_cells = game.find_adjacent(self.pos)
        for cell in adj_cells:
            fp = game.get_floor(cell)
            if fp and fp.name == "O":
                game.toggle_door(fp.pos)


class NPChar(Character):
    def __init__(self, skill, stamina, name, pos=None):
        super().__init__(skill, stamina, name, pos)
        self.color = [0, 255, 0]
