import os
import tempfile
import unittest

from ant import Ant, Environment, adjacent_positions, direct_neighbors


class EnvTest(unittest.TestCase):
    def test_pheromone_override(self):
        env = Environment()
        env[0, 0, 0, "pheromone-1"] = 12
        env[0, 0, 0, "pheromone-2"] = 23
        self.assertEqual(env[0, 0, 0, "pheromone-2"], 23)
        self.assertEqual(env[0, 0, 0, "pheromone-1"], 12)
        self.assertDictEqual(env[0, 0, 0], {"pheromone-1": 12, "pheromone-2": 23})

    def test_set_get_value(self):
        env = Environment()
        env[0, 0, 0, "pheromone-1"] = 12
        self.assertEqual(env[0, 0, 0, "pheromone-1"], 12)
        self.assertEqual(len(env._cells), 1)

    def test_get_empty_cell(self):
        env = Environment()
        self.assertEqual(len(env._cells), 0)
        self.assertIsNone(env[0, 0, 0, "pheromone-1"])
        self.assertIsNone(env[0, 0, 0])

    def test_get_pheromone(self):
        env = Environment()
        env[0, 0, 0, "pheromone-1"] = 12
        self.assertIsNone(env[0, 0, 0, "pheromone-2"])
        self.assertDictEqual(env[0, 0, 0], {"pheromone-1": 12})

    def test_get_with_bad_key(self):
        env = Environment()
        with self.assertRaises(TypeError):
            _ = env[1]

        with self.assertRaises(TypeError):
            _ = env[1, 2]

        with self.assertRaises(TypeError):
            _ = env[1, 2, 3, 4, 5]

    def test_set_with_bad_key(self):
        env = Environment()
        with self.assertRaises(TypeError):
            env[0] = 12

        with self.assertRaises(TypeError):
            env[0, 1] = 12

        with self.assertRaises(TypeError):
            env[0, 1, 2] = 12

        with self.assertRaises(TypeError):
            env[0, 1, 2, 3, 4] = 12

    def test_evaporate(self):
        env = Environment()
        env[0, 0, 0, "pheromone-1"] = 1
        env[0, 0, 0, "pheromone-2"] = 1
        env[1, 0, 0, "pheromone-1"] = 1
        env.evaporate()
        self.assertAlmostEqual(env[0, 0, 0, "pheromone-1"], 0.95)
        self.assertAlmostEqual(env[0, 0, 0, "pheromone-2"], 0.95)
        self.assertAlmostEqual(env[1, 0, 0, "pheromone-1"], 0.95)

    def test_evaporate_zero_capped(self):
        env = Environment()
        env[0, 0, 0, "pheromone-1"] = 1
        env[0, 0, 0, "pheromone-2"] = 1
        env[1, 0, 0, "pheromone-1"] = 1
        env.evaporate(value=2)
        self.assertEqual(env[0, 0, 0, "pheromone-1"], 0)
        self.assertEqual(env[0, 0, 0, "pheromone-2"], 0)
        self.assertEqual(env[1, 0, 0, "pheromone-1"], 0)

    def test_export(self):
        env = Environment()
        env[0, 0, 0, "pheromone-1"] = 1
        env[0, 0, 0, "pheromone-2"] = 1
        env[1, 0, 0, "pheromone-1"] = 1
        env[0, 1, 0, "pheromone-1"] = 1
        env[0, 0, 1, "pheromone-1"] = 1
        path = os.path.join(tempfile.gettempdir(), "test_export.csv")
        try:
            env.export(path)
            with open(path, "r") as f:
                lines = [line.strip("\n") for line in f.readlines()]
            self.assertEqual(len(lines), 4)
            for line in [
                "0,0,0",
                "1,0,0",
                "0,1,0",
                "0,0,1",
            ]:
                self.assertIn(line, lines)
        finally:
            if os.path.isfile(path):
                os.remove(path)


class PositionTest(unittest.TestCase):
    def test_len_direct_neighbors(self):
        self.assertEqual(len(list(direct_neighbors((0, 0, 0)))), 6)

    def test_direct_neighbors(self):
        self.assertListEqual(
            sorted(list(direct_neighbors((2, 2, 2)))),
            sorted(
                [
                    (1, 2, 2),
                    (3, 2, 2),
                    (2, 1, 2),
                    (2, 3, 2),
                    (2, 2, 1),
                    (2, 2, 3),
                ]
            ),
        )

    def test_position_not_in_adjacent_list(self):
        positions = adjacent_positions((1, 1, 1))
        self.assertNotIn((1, 1, 1), positions)

    def test_no_position_below_floor_in_adjacent_list(self):
        self.assertTrue(all(y >= 0 for (_, y, z) in adjacent_positions((0, 0, 0))))

    def test_no_dupe_in_adjacent_list(self):
        self.assertEqual(
            len(list(adjacent_positions((1, 1, 1)))),
            len(set(adjacent_positions((1, 1, 1)))),
        )

    def test_total_adjacent_list(self):
        positions = list(adjacent_positions((0, 1, 0)))
        # 9 cells above the original position
        # 8 at the same y-coordinate as the original position
        # 9 cells under the original position
        self.assertEqual(len(positions), 9 + 8 + 9)
        self.assertListEqual(
            sorted(positions),
            sorted(
                [
                    (-1, 0, -1),
                    (-1, 0, 0),
                    (-1, 0, 1),
                    (-1, 1, -1),
                    (-1, 1, 0),
                    (-1, 1, 1),
                    (-1, 2, -1),
                    (-1, 2, 0),
                    (-1, 2, 1),
                    (0, 0, -1),
                    (0, 0, 0),
                    (0, 0, 1),
                    (0, 1, -1),
                    (0, 1, 1),
                    (0, 2, -1),
                    (0, 2, 0),
                    (0, 2, 1),
                    (1, 0, -1),
                    (1, 0, 0),
                    (1, 0, 1),
                    (1, 1, -1),
                    (1, 1, 0),
                    (1, 1, 1),
                    (1, 2, -1),
                    (1, 2, 0),
                    (1, 2, 1),
                ]
            ),
        )

    def test_total_adjacent_list_increment_value(self):
        positions = adjacent_positions((2, 2, 2), 2)
        # 25 * 2 cells above the original position
        # 24 at the same y-coordinate as the original position
        # 25 * 2 cells under the original position
        self.assertEqual(len(list(positions)), 25 * 2 + 24 + 25 * 2)


class AntTest(unittest.TestCase):
    def test_move_changes_position(self):
        ant = Ant((0, 0, 0), alpha=0)
        environment = Environment()
        environment[1, 0, 0, "move"] = 12
        self.assertEqual(ant._position, (0, 0, 0))
        ant.act(environment)
        self.assertNotEqual(ant._position, (0, 0, 0))

    def test_filter_adjacent_positions_has_floor_position(self):
        ant = Ant((0, 0, 0))
        valid_positions = list(
            ant._filter_adjacent_positions(
                adjacent_positions(ant._position), Environment()
            )
        )
        self.assertTrue(len(valid_positions) != 0)
        self.assertTrue(all(y == 0 for (_, y, z) in valid_positions))

    def test_filter_adjacent_positions_no_overlap_with_cubes(self):
        ant = Ant((1, 0, 0))
        environment = Environment()
        environment[0, 0, 0, "pheromone-1"] = 12
        valid_positions = list(
            ant._filter_adjacent_positions(
                adjacent_positions(ant._position), environment
            )
        )
        self.assertTrue(len(valid_positions) != 0)
        self.assertNotIn((0, 0, 0), valid_positions)

    def test_filter_adjacent_positions_above_cube_position(self):
        ant = Ant((0, 0, 0))
        environment = Environment()
        environment[1, 0, 0, "pheromone-1"] = 12
        valid_positions = list(
            ant._filter_adjacent_positions(
                adjacent_positions(ant._position), environment
            )
        )
        self.assertIn((1, 1, 0), valid_positions)

    def test_successive_moves(self):
        ant = Ant((0, 0, 0))
        env = Environment()
        env[1, 0, 0, "move"] = 1
        env[1, 0, 0, "build"] = 2
        max_movement = 10
        for _ in range(max_movement):
            ant.act(env)
        self.assertTrue(
            (max_movement, max_movement, max_movement)
            > ant._position
            > (-max_movement, -max_movement, -max_movement)
        )

    def test_position_changed_when_no_possible_positions(self):
        # being in y = 2 in an empty env makes it impossible to move
        ant = Ant((0, 2, 0), pheromones=["move"])
        env = Environment()
        ant.act(env)
        self.assertNotEqual(ant._position, (0, 1, 0))

    def test_get_most_attractive_position(self):
        ant = Ant((0, 0, 0))
        positions_pheromone = {
            (1, 0, 0): {"move": 1, "build": 1},
            (0, 1, 0): {"move": 2, "build": 1},
            (0, 0, 1): {"move": 0, "build": 1},
        }
        (
            most_attractive_position,
            highest_pheromone,
            phero_value,
        ) = ant._get_most_attractive_position(positions_pheromone)
        self.assertEqual(most_attractive_position, (0, 1, 0))
        self.assertEqual(highest_pheromone, "move")
        self.assertEqual(phero_value, 2)

    def test_get_random_most_attractive_position(self):
        ant = Ant((0, 0, 0))
        positions_pheromone = {
            (1, 0, 0): {"move": 1, "build": 1},
            (0, 1, 0): {"move": 2, "build": 1},
            (0, 0, 1): {"move": 2, "build": 1},
        }
        (
            most_attractive_position,
            highest_pheromone,
            phero_value,
        ) = ant._get_most_attractive_position(positions_pheromone)
        self.assertIn(most_attractive_position, [(0, 1, 0), (0, 0, 1)])
        self.assertEqual(highest_pheromone, "move")
        self.assertEqual(phero_value, 2)

    def test_ant_only_interact_with_move_build_pheromones(self):
        ant = Ant((0, 0, 0), pheromones=["unknown-phero"])
        environment = Environment()
        environment[1, 1, 1, "unknown-phero"] = 1
        ant.act(environment)
        self.assertEqual(ant._position, (0, 0, 0))

    def test_ant_no_build_on_zero_phero(self):
        ant = Ant((0, 0, 0))
        environment = Environment()
        for _ in range(10):
            ant.act(environment)
        self.assertNotIn("build", ant._actions)

    def test_ant_build_and_move(self):
        ant = Ant((0, 0, 0))
        environment = Environment()
        environment[1, 0, 0, "move"] = 1
        environment[1, 0, 0, "build"] = 1
        for _ in range(25):
            ant.act(environment)
        self.assertIn("build", ant._actions)
        self.assertIn("move", ant._actions)


if __name__ == "__main__":
    unittest.main()
