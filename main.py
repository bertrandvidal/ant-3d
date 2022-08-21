from collections import defaultdict

from ant import Ant, Environment

if __name__ == "__main__":
    env = Environment()
    env[1, 0, 0, "move"] = 1
    env[1, 0, 0, "build"] = 1

    for i in range(25):
        env[1, i, 0, "build"] = 1
        env[1, i, 0, "move"] = 1

    ants = [Ant((0, 0, 0)) for _ in range(10)]

    for _ in range(75):
        for ant in ants:
            ant.act(env)
        env.evaporate()

    actions = defaultdict(int)
    for ant in ants:
        for action in ant._actions:
            actions[action] += 1

    print(actions)

    env.export("./export.csv", pheromone="build")
