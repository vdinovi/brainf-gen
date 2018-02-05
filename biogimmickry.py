# Name:         Vittorio Dinovi
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Biogimmickry
# Term:         Winter 2018

import random
import pdb


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
    return {
        'program': ''.join([random.choice(LANGUAGE) for _ in range(0, length)]),
        'fitness': -1
    }


def select(population):
    cutoff = random.uniform(0, 1)
    total = 0
    for i, member in enumerate(population):
        total += member['fitness']
        if total > cutoff:
            return population.pop(i)

def normalize_population(population):
    max_fitness = max(population, key=lambda m: m['fitness'])['fitness']
    for m in population:
        m['fitness'] /= max_fitness

def generate_population(size):
    population = []
    for i in range(0, size):
        length = random.randint(MIN_LEN, MAX_LEN)
        population.append(random_progam(length))
    return population


def calculate_fitness(population, target, interpreter):
    for member in population:
        member['fitness'] = evaluate_fitness(
            member['program'], target, interpreter
        )


def naturalSelect(A, B):
    if A['fitness'] <= B['fitness']:
        return A
    else:
        return B


def create_simple_program(target, interpreter):
    population = generate_population(2**5)
    calculate_fitness(population, target, interpreter)
    gen = 0
    while len(population) > 1:
        normalize_population(population)
        new_pop = []
        while population:
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
            child = naturalSelect(childX, childY)
            new_pop.append(child)
        population = new_pop
        gen += 1
    winner = population[0]
    print("After {} iterations, selected: {}({}) -> {}",
        gen, winner['program'], winner['fitness'], interpreter(winner['program'],
        prog_buffer(BUFFER_SIZE)))
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
