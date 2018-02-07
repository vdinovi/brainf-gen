# Name:         Vittorio Dinovi
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Biogimmickry
# Term:         Winter 2018

import random
import pdb
import math


SIMPLE_LANGUAGE = ('>', '<', '+', '-')
LANGUAGE = ('>', '<', '+', '-', '[', ']')
NUM_GENERATIONS = 500


def prog_buffer(length):
    return [0] * length

def jump_forward(prog, pc):
    count = 1
    i = pc + 1
    while count:
        if prog[i] == '[':
            count += 1
        elif prog[i] == ']':
            count -= 1
        i += 1
    return i - 1

def jump_backward(prog, pc):
    count = 1
    i = pc - 1
    while count:
        if prog[i] == ']':
            count += 1
        elif prog[i] == '[':
            count -= 1
        i -= 1
    return i + 1


def interpret(prog, array):
    dp = 0
    pc = 0
    while pc < len(prog):
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
                pc = jump_forward(prog, pc)
        elif prog[pc] == ']':
            if array[dp]:
                pc = jump_backward(prog, pc)
        pc += 1
    return array


def random_simple_progam(length):
    return {
        'program': ''.join([random.choice(SIMPLE_LANGUAGE) for _ in range(0, length)]),
        'fitness': -1
    }


def select_random(population):
    pos = random.randint(0, len(population) - 1)
    return population.pop(pos)


def normalize_population(population):
    total_fitness = sum([m['fitness'] for m in population])
    for m in population:
        m['score'] = total_fitness - m['fitness']


def generate_population(size):
    population = []
    min_len = 5
    max_len = 30
    for i in range(0, size):
        length = random.randint(min_len, max_len)
        population.append(random_simple_progam(length))
    return population


def calculate_fitness(population, target, interpreter):
    for member in population:
        member['fitness'] = evaluate_fitness(
            member['program'], target, interpreter
        )


def natural_select_pair(A, B):
    return min([A, B], key=lambda x: x['fitness'])


def natural_select_pop(population):
    orig_size = len(population)
    for _ in range(0, int(0.25*len(population))):
        selected = max(population, key=lambda x: x['fitness'])
        population.remove(selected)
    while len(population) < orig_size:
        clone = random.choice(population)
        population.append(clone)


def select_crossover(population, target, interpreter):
    progX = select_random(population)
    progY = select_random(population)
    cProgX, cProgY = crossover(progX['program'], progY['program'])
    childX = {
        'program': cProgX,
        'fitness': evaluate_fitness(cProgX, target, interpreter)
    } 
    childY = {
        'program': cProgY,
        'fitness': evaluate_fitness(cProgY, target, interpreter)
    } 
    return childX, childY

def substitute_mutation(prog):
    pos = random.randint(0, len(prog) - 1)
    prog = list(prog)
    prog[pos] = random.choice(SIMPLE_LANGUAGE)
    return ''.join(prog)


def select_point_mutation(population, target, interpreter):
    child = select_random(population)
    cProg = substitute_mutation(child['program'])
    return {
        'program': cProg,
        'fitness': evaluate_fitness(cProg, target, interpreter)
    }

def avg_fitness(population):
    total = 0
    for m in population:
        total += m['fitness']
    return total / len(population)

def create_simple_program(target, interpreter):
    population = generate_population(2**8)
    calculate_fitness(population, target, interpreter)
    #normalize_population(population)
    #natural_select_pop(population)
    gen = 0
    while gen < NUM_GENERATIONS:
        #print("Gen {} ({}) avg fitness: {}".format(gen, len(population), avg_fitness(population)))
        num_crossovers = int(0.1 * len(population))
        # run crossover mutations
        while num_crossovers > 0:
            c1, c2 = select_crossover(population, target, interpreter)
            population.append(c1)
            population.append(c2)
            num_crossovers -= 1
        num_point_mutations = int(0.25 * len(population))
        # run point mutations (sub)
        while num_point_mutations > 0:
            child = select_point_mutation(population, target, interpreter)
            population.append(child)
            num_point_mutations -= 1
        natural_select_pop(population)
        gen += 1
    winner = population[0]
    #print("After {} iterations, selected: {}({}) -> {}".format(
    #    gen, winner['program'], winner['fitness'], interpreter(winner['program'],
    #    prog_buffer(len(target)))))
    return winner['program']


def crossover(program_x, program_y):
    childX = list(program_x)
    childY = list(program_y)
    if len(childX) < 3 or len(childY) < 3:
        #raise Exception("Programs too short to crossover: {}, {}".format(len(childX), len(childY)))
        return program_x, program_y 
    maxPos = min(len(program_x), len(program_y))-2
    crossIndex = int(random.uniform(2, maxPos))
    swap = childX[0 : crossIndex]
    childX[0 : crossIndex] = program_y[0 : crossIndex]
    childY[0 : crossIndex] = swap
    childX = ''.join(childX)
    childY = ''.join(childY)
    #print("{} -> {} ({})".format(program_x, childX, crossIndex))
    #print("{} -> {} ({})".format(program_y, childY, crossIndex))
    return childX, childY

def evaluate_fitness(prog, target, interpreter):
    result = interpreter(prog, prog_buffer(len(target)))
    fitness = 0
    for i in range(0, len(target)):
        fitness += abs(result[i] - target[i])
    return fitness



"""
from sys import argv
if __name__ == "__main__":
    winner = create_simple_program([7,7,7], interpret)
""
