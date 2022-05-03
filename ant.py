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


def adjacent_positions(position, increment=1):
    """Yield all 3d positions that are 'increment' unit around the given position

    :param position: the original (x, y, z) position
    :param increment: how many units around the original position to use
    :return: list of 3d positions that are "around" the given position that are not
    under the ground (y >=0) and are not the original position
    """
    x, y, z = position
    for x_increment in range(x - increment, x + increment + 1):
        for y_increment in range(y - increment, y + increment + 1):
            for z_increment in range(z - increment, z + increment + 1):
                if (x + x_increment, y + y_increment, z + z_increment) != position and (
                    y + y_increment
                ) >= 0:
                    yield x + x_increment, y + y_increment, z + z_increment
