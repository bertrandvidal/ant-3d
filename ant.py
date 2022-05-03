from collections import defaultdict


class Environment:
    """Represent the 3d environment in which the agents are evolving. It does not have
    an explicit limit or size. Each "cell" of the environment can contain a variety
    of pheromones, these are handled as a 4th dimension. Since the Environment is
    subscribable we can use: `env[x, y, z, "pheromone"] = 12` but the last dimension
    is optional when accessing the cells:

    env[x, y, z, "pheromone-1"] = 12
    env[x, y, z, "pheromone-2"] = 23
    print(env[x, y, z, "pheromone-1")
    >> 12
    print(env[x, y, z])
    >> {"pheromone-1": 12, "pheromone-2": 23}
    """

    def __init__(self):
        self._cells = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    def __setitem__(self, key, value):
        """Set the value of a pheromone in a cell of the environment.

        :param key: tuple (x, y, z, pheromone)
        :param value: the value of the pheromone in the cell designated by (x,y,z)
        """
        try:
            x, y, z, phero = key
            self._cells[x][y][z][phero] = value
        except ValueError:
            raise TypeError("key should be (x, y, z, phero)")

    def __getitem__(self, key):
        """Get the cell at the given coordinates, the key can be one of (x, y, z,
        phero) or (x, y, z).

        :param key: (x, y, z, phero) or (x, y, z)
        :return: for (x, y, z, phero) returns the value of the pheromone at (x,
        y, z); for (x, y, z) returns a dict of phero: value; None if the cell is empty
        """
        try:
            x, y, z, phero = key
            return self._cells[x][y][z].get(phero)
        except ValueError:
            try:
                x, y, z = key
                return self._cells[x][y][z] or None
            except ValueError:
                raise TypeError("key should be (x, y, z, phero) or (x, y, z)")
