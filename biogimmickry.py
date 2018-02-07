# Name:         Vittorio Dinovi
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Biogimmickry
# Term:         Winter 2018

import random
import math


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


def random_simple_progam(length):
    lang = ('>', '<', '+', '-')
    return {
        'program': ''.join([random.choice(lang) for _ in range(0, length)]),
        'fitness': -1
    }


def select_random(population):
    pos = random.randint(0, len(population) - 1)
    return population.pop(pos)


def normalize_population(population):
    total_fitness = sum([m['fitness'] for m in population])
    for m in population:
        m['score'] = total_fitness - m['fitness']


def min_length(target):
    count = 0
    for i in range(0, len(target)):
        count += i + target[i]
    return count


def generate_population(size, target):
    max_multiplier = 8
    min_l = min_length(target)
    max_l = min_l * max_multiplier
    population = []
    for i in range(0, size):
        length = random.randint(min_l, max_l)
        population.append(random_simple_progam(length))
    return population


def calculate_fitness(population, target, interpreter):
    for member in population:
        member['fitness'] = evaluate_fitness(
            member['program'], target, interpreter
        )


def natural_select_pair(A, B):
    return min([A, B], key = lambda x: x['fitness'])


def natural_select_pop(population):
    orig_size = len(population)
    lower_percentile = 0.25
    for _ in range(0, int(lower_percentile * len(population))):
        selected = max(population, key = lambda x: x['fitness'])
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
    lang = ('>', '<', '+', '-')
    prog[pos] = random.choice(lang)
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
    pop_size = 256
    population = generate_population(pop_size, target)
    calculate_fitness(population, target, interpreter)
    #normalize_population(population)
    #natural_select_pop(population)
    gen = 0
    num_gens = 250
    while gen < num_gens:
        #print("Gen {} ({}) avg fitness: {}".format(gen, len(population), avg_fitness(population)))
        crossover_prop = 0.1
        num_crossovers = int(crossover_prop * len(population))
        # run crossover mutations
        while num_crossovers > 0:
            c1, c2 = select_crossover(population, target, interpreter)
            population.append(c1)
            population.append(c2)
            num_crossovers -= 1
        point_mut_prop = 0.25
        num_point_mutations = int(point_mut_prop * len(population))
        # run point mutations (sub)
        while num_point_mutations > 0:
            child = select_point_mutation(population, target, interpreter)
            population.append(child)
            num_point_mutations -= 1
        natural_select_pop(population)
        gen += 1
    winner = population[0]
    #result = prog_buffer(len(target))
    #interpreter(winner['program'], result)
    #print("After {} iterations, selected: {}({}) -> {}".format(
    #    gen, winner['program'], winner['fitness'], result))
    return winner['program']


def crossover(program_x, program_y):
    child_x = list(program_x)
    child_y = list(program_y)
    max_pos = min(len(program_x), len(program_y)) - 2
    cross1 = int(random.uniform(2, max_pos))
    cross2 = int(random.uniform(2, max_pos))
    new_child_x = ''.join(child_y[0 : cross2] + child_x[cross1 : len(child_x)])
    new_child_y = ''.join(child_x[0 : cross1] + child_y[cross2 : len(child_y)])
    #print("{} ({})-> {}\n{} ({})-> {}\n".format(program_x, cross1, new_child_x, program_y, cross2, new_child_y))
    return new_child_x, new_child_y


def evaluate_fitness(prog, target, interpreter):
    result = prog_buffer(len(target))
    interpreter(prog, result)
    fitness = 0
    for i in range(0, len(target)):
        fitness += abs(result[i] - target[i])
    return fitness

