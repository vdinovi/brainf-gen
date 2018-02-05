# Name:         Vittorio Dinovi
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Biogimmickry
# Term:         Winter 2018

import random
import pdb
import math


class InvalidSymbol(Exception):

    def __init__(self, msg):
        self.msg =  msg


MIN_LEN = 5
MAX_LEN = 10
CROSS_WEIGHT = 0.4
LANGUAGE = ('>', '<', '+', '-')
BUFFER_SIZE = 20
STARTING_POP = 10
ITERATIONS = 20


def prog_buffer(length):
    return [0] * length


def interpret(prog, array):
    index = 0
    for op in prog:
        if   op == '>':
            index += 1
        elif op == '<':
            index -= 1
        elif op == '+':
            array[index] += 1
        elif op == '-':
            array[index] -= 1
        else:
            raise InvalidSymbol(op)
    return array


def random_progam(length):
    # O(1)
    return {
        'program': ''.join([random.choice(LANGUAGE) for _ in range(0, length)]),
        'fitness': -1
    }


def select(population):
    # O(n)
    cutoff = random.uniform(0, 1)
    total = 0
    for i, member in enumerate(population):
        total += member['fitness']
        if total > cutoff:
            return population.pop(i)

def normalize_population(population):
    # O(2n)
    total_fitness = 0
    for m in population:
        total_fitness += m['fitness']
    for m in population:
        m['score'] = total_fitness - m['fitness']

def generate_population(size):
    # O(n)
    population = []
    for i in range(0, size):
        length = random.randint(MIN_LEN, MAX_LEN)
        population.append(random_progam(length))
    return population


def calculate_fitness(population, target, interpreter):
    # O(n)
    for member in population:
        member['fitness'] = evaluate_fitness(
            member['program'], target, interpreter
        )

def naturalSelectPair(A, B):
    # O(1)
    return min([A, B], key=lambda x: x['fitness'])


# Remove 1/2 of the least 'fittest' from population
def naturalSelectPop(population):
    for _ in range(0, int(len(population)/2)):
        selected = min(population, key=lambda x: x['score'])
        population.remove(selected)

def selectCrossover(population, target, interpreter):
    progX = select(population)
    progY = select(population)
    cProgX, cProgY = \
        crossover(progX['program'], progY['program'])
    childX = {
        'program': cProgX,
        'fitness': evaluate_fitness(cProgX, target, interpreter)
    } 
    childY = {
        'program': cProgY,
        'fitness': evaluate_fitness(cProgY, target, interpreter)
    } 
    return naturalSelectPair(childX, childY)


def create_simple_program(target, interpreter):
    population = generate_population(2**10)
    calculate_fitness(population, target, interpreter)
    normalize_population(population)
    naturalSelectPop(population)
    gen = 0
    while len(population) > 1:
        numCrossovers = math.sqrt(len(population))
        while len(population) > 1 and numCrossovers > 0:
            population.append(selectCrossover(population, target, interpreter))
            if len(population) == 1:
                break
            numCrossovers -= 1
        normalize_population(population)
        naturalSelectPop(population)
        gen += 1
    winner = population[0]
    #print("After {} iterations, selected: {}({}) -> {}".format(
    #    gen, winner['program'], winner['fitness'], interpreter(winner['program'],
    #    prog_buffer(BUFFER_SIZE))))
    return winner['program']



def crossover(progX, progY):
    childX = list(progX)
    childY = list(progY)
    length = min(len(progX), len(progY))
    crossIndex = int(length * CROSS_WEIGHT)
    swap = childX[0 : crossIndex]
    childX[0 : crossIndex] = progY[0 : crossIndex]
    childY[0 : crossIndex] = swap
    childX = ''.join(childX)
    childY = ''.join(childY)
    return childX, childY

def evaluate_fitness(prog, target, interpreter):
    buf = prog_buffer(BUFFER_SIZE)
    result = interpreter(prog, buf)

    fitness = 0
    for i, v in enumerate(target):
        if i < len(result):
            fitness += abs(result[i] - target[i])
    return fitness


def empty_target(length):
    return [0] * length

def print_prog(name, prog, target):
    result = interpret(prog, prog_buffer(BUFFER_SIZE))
    print (
        name,
        prog,
        str(result),
        evaluate_fitness(result, target)
    )



if __name__ == "__main__":
    winner = create_simple_program([1,2,3,4,5,6,7,8,9,10], interpret)



"""
    progX = create_simple_program([1,2,3])
    print_prog('ProgX', progX, empty_target(BUFFER_SIZE))
    progY = create_simple_program([1,2,3])
    print_prog('ProgY', progX, empty_target(BUFFER_SIZE))
    childX, childY, crossIndex = crossover(progX, progY)
    print_prog('ChildX', childX, empty_target(BUFFER_SIZE))
    print_prog('ChildY', childY, empty_target(BUFFER_SIZE))
"""
