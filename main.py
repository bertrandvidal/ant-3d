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

    env.export("./export.csv")
