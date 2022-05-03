import unittest

from ant import Environment, adjacent_positions


class EnvTest(unittest.TestCase):
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


class PositionTest(unittest.TestCase):
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
        positions = adjacent_positions((1, 1, 1))
        # 9 cells above the original position
        # 8 at the same y-coordinate as the original position
        # 9 cells under the original position
        self.assertEqual(len(list(positions)), 9 + 8 + 9)

    def test_total_adjacent_list_increment_value(self):
        positions = adjacent_positions((1, 1, 1), 2)
        # 25 * 2 cells above the original position
        # 24 at the same y-coordinate as the original position
        # 25 * 2 cells under the original position
        self.assertEqual(len(list(positions)), 25 * 2 + 24 + 25 * 2)


if __name__ == "__main__":
    unittest.main()
