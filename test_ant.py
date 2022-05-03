import unittest

from ant import Environment


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


if __name__ == "__main__":
    unittest.main()
