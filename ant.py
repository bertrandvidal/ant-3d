import abc
from collections import defaultdict
from random import choice, randint


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
                if (x_increment, y_increment, z_increment) != position and (
                    y_increment
                ) >= 0:
                    yield x_increment, y_increment, z_increment


transformations = [
    lambda x, y, z: (x, y + 1, z),
    lambda x, y, z: (x, y - 1, z),
    lambda x, y, z: (x + 1, y, z),
    lambda x, y, z: (x - 1, y, z),
    lambda x, y, z: (x, y, z + 1),
    lambda x, y, z: (x, y, z - 1),
]


def direct_neighbors(position):
    """Return the positions that are direct neighbors, change of one unit in one
    coordinate at a time i.e. no diagonal.

    :param position: position for which we want direct neighbors
    :return: list of direct neighboring positions
    """
    return [transformation(*position) for transformation in transformations]


def pheromone_attractiveness(position, environment, pheromones):
    """Return the attractiveness of the position for the given pheromones.
    Attractiveness is based on the sum of the neighboring positions in the environment.

    :param position: the position to consider
    :param environment: the environment in which to calculate the attractiveness
    :param pheromones: the names of the pheromones to compute attractiveness for
    :return: dict of pheromone:value
    """
    neighbors = direct_neighbors(position)
    return {
        phero: sum(environment[x, y, z, phero] or 0 for x, y, z in neighbors)
        for phero in pheromones
    }


class Agent(abc.ABC):
    def __init__(self, position, action_range=1):
        """
        :param position: (x, y, z) starting position of the Agent
        :param action_range: how far in the Environment can the agent act
        """
        self._position = position
        self._range = action_range

    def act(self, environment):
        possible_positions = self._filter_adjacent_positions(
            adjacent_positions(self._position, self._range), environment
        )
        self._selection_action(environment, possible_positions)

    def _filter_adjacent_positions(self, positions, environment):
        """Apply any filtering to adjacent position to fit how the Agent operate,
        no filtering is done by defaults

        :param positions: all the positions that are reachable by the Agent
        :param environment: the environment in which the Agent evolves
        :return: all the position the Agent can act on
        """
        return positions

    @abc.abstractmethod
    def _selection_action(self, environment, possible_positions):
        pass


class Ant(Agent):
    def __init__(self, position, alpha=0.25, action_range=1, pheromones=None):
        super().__init__(position, action_range)
        self._alpha = alpha
        self._actions = []
        self._pheromones = pheromones or ["move", "build"]

    def _filter_adjacent_positions(self, positions, environment):
        for position in positions:
            x, y, z = position
            # we can't move/build to our own position or a cell that's already occupied
            if position == self._position or environment[x, y, z]:
                continue
            # on the ground
            if y == 0:
                yield position
            # one of direct neighboring cells of 'position' is a cube so we can
            # "attach" to it
            for (xx, yy, zz) in direct_neighbors(position):
                if environment[xx, yy, zz]:
                    yield position

    def _selection_action(self, environment, possible_positions):
        positions_pheromone = {
            pos: pheromone_attractiveness(pos, environment, self._pheromones)
            for pos in possible_positions
        }
        if not positions_pheromone:
            # if there's no available positions, randomly positions the ant on
            # the floor
            self._position = (
                randint(0, self._position[0]),
                0,
                randint(0, self._position[2]),
            )
            return
        # TODO(bvidal): the phero for "build" are always 0

        (
            most_attractive_position,
            highest_pheromone,
            phero_attractiveness,
        ) = self._get_most_attractive_position(positions_pheromone)

        if highest_pheromone == "move":
            print(f"moving to {most_attractive_position}")
            self._position = most_attractive_position
            self._actions.append("move")
        elif highest_pheromone == "build":
            x, y, z = most_attractive_position
            # we cannot build if there are nothing around us/build phero value = 0
            if phero_attractiveness != 0:
                print(f"building to {most_attractive_position}")
                self._actions.append("build")
                for phero in self._pheromones:
                    environment[x, y, z, phero] = 1

    def _get_most_attractive_position(self, positions_pheromone):
        """
        :param positions_pheromone: (position, {phero: value} for all valid position
        the agent can reach/act on
        :return: a randomly chosen position which has the highest pheromone value as
        a tuple (position, highest pheromone, value of pheromone attractiveness)
        """
        most_attractive_positions = sorted(
            positions_pheromone.items(), key=lambda item: max(item[1].values())
        )
        max_phero_value = max(most_attractive_positions[-1][1].values())
        # randomly select any position that has a pheromone value equal to the max
        (most_attractive_position, pheros) = choice(
            [
                (pos, pheros)
                for pos, pheros in most_attractive_positions
                if max(pheros.values()) == max_phero_value
            ]
        )
        # randomly pick the pheromone, at the current position, that has the highest
        # value
        highest_pheromone = choice(
            [k for k, v in pheros.items() if v == max_phero_value]
        )
        return most_attractive_position, highest_pheromone, max_phero_value
