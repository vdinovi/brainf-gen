# Name:         Vittorio Dinovi
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Biogimmickry
# Term:         Winter 2018

# Note: not complete, tried playing around with fitness function
#       to overcome various problems. 
#       Ended up giving up in favor of studying for finals.

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


def interpret(prog, array, max_steps):
    cycles = 0
    dp = 0
    pc = 0
    while pc < len(prog):
        if cycles > max_steps:
            raise RuntimeError
        if prog[pc] == '>' and dp < len(array) - 1:
            dp += 1
        elif prog[pc] == '<' and dp > 0:
            dp -= 1
        elif prog[pc] == '+':
            array[dp] += 1
        elif prog[pc] == '-':
            array[dp] -= 1
        elif prog[pc] == '[':
            if not array[dp]:
                pc = jump_forward(prog, pc)
        elif prog[pc] == ']':
            if array[dp]:
                pc = jump_backward(prog, pc)
        pc += 1
        cycles += 1


def random_progam(length):
    lang = ('>', '<', '+', '-')
    prog = [random.choice(lang) for _ in range(0, length)]
    start = int(random.uniform(0, length - 1))
    end = int(random.uniform(start + 1, length - 1))
    prog[start] = '['
    prog[end] = ']'
    prog.insert(end, random.choice(lang))
    prog.insert(0, '+')
    return {
        'program': ''.join(prog),
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
        count += i + abs(target[i])
    return count


def generate_population(size, target, limit):
    population = []
    for i in range(0, size):
        length = random.randint(2, limit)
        population.append(random_progam(length))
    return population


def calculate_fitness(population, target, interpreter, limit):
    for member in population:
        member['fitness'] = evaluate_fitness(
            member['program'], target, interpreter, limit
        )


def natural_select_pair(A, B):
    return min([A, B], key = lambda x: x['fitness'])


def natural_select_pop(population):
    orig_size = len(population)
    lower_percentile = 0.15
    for _ in range(0, int(lower_percentile * len(population))):
        selected = max(population, key = lambda x: x['fitness'])
        population.remove(selected)
    while len(population) < orig_size:
        clone = random.choice(population)
        population.append(clone)


def select_crossover(population, target, interpreter, limit):
    progX = select_random(population)
    progY = select_random(population)
    cProgX, cProgY = crossover(progX['program'], progY['program'])
    childX = {
        'program': cProgX,
        'fitness': evaluate_fitness(cProgX, target, interpreter, limit)
    } 
    childY = {
        'program': cProgY,
        'fitness': evaluate_fitness(cProgY, target, interpreter, limit)
    } 
    return childX, childY


def substitute_mutation(prog):
    prog = list(prog)
    lang = ('>', '<', '+', '-')
    pos = random.randint(0, len(prog) - 1)
    if prog[pos] == '[' or prog[pos] == ']':
        return ''.join(prog)
    prog[pos] = random.choice(lang)
    return ''.join(prog)


def loop_insert_mutation(prog, limit):
    if len(prog) + 1 > limit:
        return prog
    prog = list(prog)
    lang = ('>', '<', '+', '-')
    start = prog.index('[')
    end = prog.index(']')
    pos = random.choice(range(start + 1, end + 1))
    prog.insert(pos, random.choice(lang))
    return ''.join(prog)


def select_loop_insert_mutation(population, target, interpreter, limit):
    child = select_random(population)
    cProg = loop_insert_mutation(child['program'], limit)
    return {
        'program': cProg,
        'fitness': evaluate_fitness(cProg, target, interpreter, limit)
    }


def select_point_mutation(population, target, interpreter, limit):
    child = select_random(population)
    cProg = substitute_mutation(child['program'])
    return {
        'program': cProg,
        'fitness': evaluate_fitness(cProg, target, interpreter, limit)
    }


def avg_fitness(population):
    total = 0
    for m in population:
        total += m['fitness']
    return total / len(population)


def crossover(program_x, program_y):
    child_x = list(program_x)
    child_y = list(program_y)
    choice = random.choice(['l', 'm', 'r'])
    if choice == 'l':
        segment = (child_x[0 : child_x.index('[')], \
                   child_y[0 : child_y.index('[')])
    elif choice == 'm':
        segment = (child_x[child_x.index('[') + 1 : child_x.index(']') ], \
                   child_y[child_y.index('[') + 1 : child_y.index(']') ])
    else:
        segment = (child_x[child_x.index(']') + 1 : len(child_x) ], \
                   child_y[child_y.index(']') + 1 : len(child_y) ])
    if not segment[0] or not segment[1]:
        return program_x, program_y
    cross1 = int(random.uniform(0, len(segment[0])))
    cross2 = int(random.uniform(0, len(segment[1])))
    new_x = segment[1][0 : cross2] + segment[0][cross1 : len(segment[0])]
    new_y = segment[0][0 : cross1] + segment[1][cross2 : len(segment[1])]
    if choice == 'l':
        child_x = ''.join(new_x + child_x[child_x.index('[') : len(child_x)])
        child_y = ''.join(new_y + child_y[child_y.index('[') : len(child_y)])
    elif choice == 'm':
        child_x = ''.join(child_x[0 : child_x.index('[') + 1] + new_x + \
                          child_x[child_x.index(']') : len(child_x)])
        child_y = ''.join(child_y[0 : child_y.index('[') + 1] + new_y + \
                          child_y[child_y.index(']') : len(child_y)])
    else:
        child_x = ''.join(child_x[0 : child_x.index(']') + 1] + new_x)
        child_y = ''.join(child_y[0 : child_y.index(']') + 1] + new_y)
    #print("({}) {} : {}\n({}) {} : {}".format(cross1, program_x, child_x, cross2, program_y, child_y))
    return child_x, child_y


def evaluate_fitness(prog, target, interpreter, limit):
    result = prog_buffer(len(target))
    fitness = 0
    penalty = 100
    try:
        interpreter(prog, result, limit)
    except RuntimeError:
        fitness += penalty
    if len(prog) > limit:
        fitness += penalty
    for i in range(0, len(target)):
        fitness += abs(result[i] - target[i])
    fitness += len(target)
    #loop_center = int((prog.index('[') + prog.index(']')) / 2)
    #prog_center = int(len(target) / 2)
    # Encourage loop in later part of program
    fitness += len(target) - prog.index('[')
    #fitness += prog.index(']') - prog.index(']') / 2
    #fitness += int((prog.index('[') - 0) / 2)
    #print(prog, ' -> ', fitness)
    return fitness 


def proc_gen(population, crossover_prop, point_mut_prop, loop_insert_mut_prop):
    # run crossover mutations
    num_crossovers = int(crossover_prop * len(population))
    while num_crossovers > 0:
        c1, c2 = select_crossover(population, target, interpreter, limit)
        population.append(c1)
        population.append(c2)
        num_crossovers -= 1
    # run point mutations
    num_point_mutations = int(point_mut_prop * len(population))
    while num_point_mutations > 0:
        child = select_point_mutation(population, target, \
                interpreter, limit)
        population.append(child)
        num_point_mutations -= 1
    # run loop insert mutations
    num_loop_insert_mutations = int(point_mut_prop * len(population))
    while num_loop_insert_mutations > 0:
        child = select_loop_insert_mutation(population, target, \
                interpreter, limit)
        population.append(child)
        num_loop_insert_mutations -= 1
    natural_select_pop(population)


def create_iterative_program(target, interpreter, limit):
    pop_size = 500
    population = generate_population(pop_size, target, limit)
    calculate_fitness(population, target, interpreter, limit)
    gen = 0
    num_gens = 500
    crossover_prop = 0.1
    point_mut_prop = 0.25
    loop_insert_mut_prop = 0.5
    while gen < num_gens:
        proc_gen(population, crossover_prop, point_mut_prop, \
                 loop_insert_mut_prop)
        natural_select_pop(population)
        gen += 1
    winner = population[0]
    result = prog_buffer(len(target))
    interpreter(winner['program'], result, limit)
    return winner['program']

