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
SIMPLE_LANGUAGE = ('>', '<', '+', '-')
LANGUAGE = ('>', '<', '+', '-', '[', ']')
BUFFER_SIZE = 10
STARTING_POP = 10
ITERATIONS = 20


def prog_buffer(length):
    return [0] * length


def interpret(prog, array):
    dp = 0
    pc = 0
    while pc < len(prog):
        #pdb.set_trace()
        if prog[pc] == '>' and dp < len(array) - 1:
            dp += 1
        elif prog[pc] == '<' and dp > 0:
            dp -= 1
        elif prog[pc] == '+':
            array[dp] += 1
        elif prog[pc] == '-':
            array[dp] -= 1
        elif prog[dp] == '[':
            if not array[dp]:
                while prog[pc] != ']':
                    pc += 1
        elif prog[pc] == ']':
            if array[dp]:
                while prog[pc] != '[':
                    pc -= 1
        pc += 1
    return array


def random_simple_progam(length):
    # O(1)
    return {
        'program': ''.join([random.choice(SIMPLE_LANGUAGE) for _ in range(0, length)]),
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
    total_fitness = sum([m['fitness'] for m in population])
    for m in population:
        m['score'] = total_fitness - m['fitness']

def generate_population(size):
    # O(n)
    population = []
    for i in range(0, size):
        length = random.randint(MIN_LEN, MAX_LEN)
        population.append(random_simple_progam(length))
    return population


def calculate_fitness(population, target, interpreter):
    # O(n)
    for member in population:
        member['fitness'] = evaluate_fitness(
            member['program'], target, interpreter
        )

def natural_select_pair(A, B):
    # O(1)
    return min([A, B], key=lambda x: x['fitness'])


# Remove 1/2 of the least 'fittest' from population
def natural_select_pop(population):
    for _ in range(0, int(len(population)/2)):
        selected = max(population, key=lambda x: x['fitness'])
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
    return childX, childY


def create_simple_program(target, interpreter):
    population = generate_population(2**8)
    calculate_fitness(population, target, interpreter)
    #normalize_population(population)
    natural_select_pop(population)
    gen = 0
    while len(population) > 1:
        numCrossovers = math.sqrt(len(population))
        while numCrossovers > 0:
            c1, c2 = selectCrossover(population, target, interpreter)
            population.append(c1)
            population.append(c2)
            numCrossovers -= 1
        #normalize_population(population)
        natural_select_pop(population)
        gen += 1
    winner = population[0]
    print("After {} iterations, selected: {}({}) -> {}".format(
        gen, winner['program'], winner['fitness'], interpreter(winner['program'],
        prog_buffer(BUFFER_SIZE))))
    return winner['program']



def crossover(program_x, program_y):
    childX = list(program_x)
    childY = list(program_y)
    a = ''.join(childX)
    b = ''.join(childY)
    if len(childX) < 3 or len(childY) < 3:
        raise Exception("Programs too short to crossover: {}, {}".format(len(childX), len(childY)))
    maxPos = min(len(program_x), len(program_y))-2
    crossIndex = int(random.uniform(2, maxPos))
    swap = childX[0 : crossIndex]
    childX[0 : crossIndex] = program_y[0 : crossIndex]
    childY[0 : crossIndex] = swap
    childX = ''.join(childX)
    childY = ''.join(childY)
    #print("{} -> {} ({})".format(a, childX, crossIndex))
    #print("{} -> {} ({})".format(b, childY, crossIndex))
    #print()
    return childX, childY

def evaluate_fitness(prog, target, interpreter):
    buf = prog_buffer(BUFFER_SIZE)
    result = interpreter(prog, buf)

    fitness = 0
    for i in range(0, max(len(target), len(result))):
        if i < len(result) and i < len(target):
            fitness += abs(result[i] - target[i])
        elif i < len(result):
            fitness += abs(result[i])
        else:
            fitness += abs(target[i])
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



"""
from sys import argv
if __name__ == "__main__":
    #winner = create_simple_program([1,2,3,4,5,6,7,8,9,10], interpret)
    buf = prog_buffer(BUFFER_SIZE)
    result = interpret(argv[1], buf)
    print(result)
"""



"""
    progX = create_simple_program([1,2,3])
    print_prog('ProgX', progX, empty_target(BUFFER_SIZE))
    progY = create_simple_program([1,2,3])
    print_prog('ProgY', progX, empty_target(BUFFER_SIZE))
    childX, childY, crossIndex = crossover(progX, progY)
    print_prog('ChildX', childX, empty_target(BUFFER_SIZE))
    print_prog('ChildY', childY, empty_target(BUFFER_SIZE))
"""
