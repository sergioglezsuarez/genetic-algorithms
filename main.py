import random
from deap import base, creator, tools, algorithms
import numpy
import matplotlib.pyplot as plt


class Train:
    def __init__(self, wagons, op, licence_plate):
        self.wagons = wagons
        self.op = op
        self.licence_plate = licence_plate

    def __str__(self):
        return "Número de vagones:" + str(self.wagons)
        + "\n" + "Muelle de operaciones:" + str(self.op)
        + "\n" + "Matrícula:" + str(self.licence_plate)


def random_trains_generation(n):
    train_list = []

    for i in range(n):
        wagons = random.randint(10, 30)  # Cada tren puede arrastrar entre 10 y 30 vagones
        op = random.choice(["op1", "op2", "op3"])  # A cada tren se le asigna un tipo de carga
        train_list.append(Train(wagons, op, i))

    # print(len(train_list))
    return train_list


incoming_trains = random_trains_generation(50)


def create_queue():
    aux = incoming_trains[:]
    random.shuffle(aux)
    return aux


class Trains(list):
    def __init__(self):
        list.extend(self, create_queue())


def evaluation(individual):
    dock_op_counters = {"op1": 0, "op2": 0, "op3": 0}
    time = 0

    for train in individual:
        next_delay = train.wagons
        if dock_op_counters[train.op] == 0:
            dock_op_counters[train.op] = next_delay
        else:
            current_delay = dock_op_counters[train.op]
            for k, v in dock_op_counters.items():
                dock_op_counters[k] = max(0, v - current_delay)
            dock_op_counters[train.op] = next_delay
            time += current_delay

    time += max(dock_op_counters.values())
    return time,


def cruce(ind1, ind2):
    i = random.randint(1, len(ind1) - 1)

    ind3 = ind1[:i]
    ind4 = ind2[:i]
    set1 = set(ind3)
    set2 = set(ind2)

    diff = set2 - set1

    for train in ind2:
        if train in diff:
            ind3.append(train)

    set1 = set(ind4)
    set2 = set(ind1)

    diff = set2 - set1

    for train in ind1:
        if train in diff:
            ind4.append(train)

    ind1[:] = ind3
    ind2[:] = ind4

    return ind1, ind2


def mutacion(individual):
    i1 = random.randint(0, len(individual) - 1)
    i2 = random.randint(0, len(individual) - 1)
    individual[i1], individual[i2] = individual[i2], individual[i1]
    return individual,


def main():
    NGEN = 100
    MU = 25
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)

    return pop, stats, hof, logbook


##################### DEAP

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", Trains, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluation)
toolbox.register("mate", cruce)
toolbox.register("mutate", mutacion)
toolbox.register("select", tools.selBest)

pop, stats, hof, logbook = main()

contador = {"op1": 0, "op2": 0, "op3": 0}
for t in hof[0]:
    contador[t.op] += t.wagons
print(contador)

print(len(hof[0]), len(set(hof[0])))

gen, avg = logbook.select("gen", "avg")
plt.plot(gen, avg, label="average")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(loc="lower right")
plt.show()

licence_plates = set()
for t in hof[0]:
    licence_plates.add(t.licence_plate)

print(len(licence_plates))  # debe darnos tantos como trenes tengan los individuos
print(sorted(list(licence_plates)))
