import pytest
import random
from ff_main_game import FFgame
from ff_game_objects import GameObj


@pytest.fixture
def my_game():
    # Ensures that "random" numbers are the same each time the test is run.
    random.seed(10)
    return FFgame()


@pytest.fixture
def my_character(my_game):
    return my_game.pcs[0]


class TestFFgame:
    def test_open_floor_plan(self):
        fp = FFgame.open_floor_plan("floor_plan.csv")
        assert fp[7].pos == [7, 0]
        assert fp[7].name == "F"
        assert fp[20].pos == [4, 1]
        assert fp[20].name == "D"

    def test_get_obj_in_loc(self, my_game, my_character):
        dwarf = my_game.get_obj_in_loc(my_game.pcs, [7, 15])[0]
        assert dwarf == my_character
        dragon = my_game.get_obj_in_loc(my_game.game_objects, [3, 8])[0]
        assert dragon == my_game.npcs[1]

    def test_get_floor(self, my_game):
        assert my_game.get_floor([4, 1]).name == "D"
        assert my_game.get_floor([1, 4]).name == "W"
        assert my_game.get_floor((6, 12)).name == "D"

    def test_find_adjacent(self, my_game):
        assert (my_game.find_adjacent([0, 0]) ==
                {(0, 1), (1, 1), (1, 0)})
        assert (my_game.find_adjacent([5, 5]) ==
                {(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)})
        assert (my_game.find_adjacent([15, 14]) ==
                {(14, 13), (14, 14), (14, 15), (15, 13), (15, 15)})

    def test_next_player(self, my_game):
        my_game.next_player()
        assert my_game.current_pc.name == "Knight"
        my_game.next_player()
        assert my_game.current_pc.name == "Dwarf"

    def test_interact(self, my_game, my_character, capfd):
        my_game.interact(my_character, [3, 8])
        out, err = capfd.readouterr()
        assert out == "Dwarf has met a Dragon\n"
        my_game.interact(my_character, [8, 15])
        out, err = capfd.readouterr()
        assert out == "Dwarf has met Knight\n"

    def test_toggle_door(self, my_game):
        fp = my_game.get_obj_in_loc(my_game.floor_plan, [4, 1])[0]
        assert fp.name == "D"
        my_game.toggle_door([4, 1])
        assert fp.name == "O"
        my_game.toggle_door([4, 1])
        assert fp.name == "D"


class TestGameObjects:
    def test_game_obj(self):
        my_obj = GameObj("chest", [3, 3])
        assert my_obj.name == "chest"
        assert my_obj.pos == [3, 3]

    def test_move(self, my_game, my_character):
        my_character.move("n", my_game)
        my_character.move("n", my_game)
        my_character.move("e", my_game)
        my_character.move("e", my_game)
        # Hits wall - no move
        my_character.move("e", my_game)
        assert my_character.pos == [9, 13]
