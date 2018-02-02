import pdb


class InvalidSymbol(Exception):
    def __init__(self, msg):
        self.msg =  msg

MIN_LEN = 5
MAX_LEN = 10
CROSS_WEIGHT = 0.4
LANGUAGE = ('>', '<', '+', '-')
BUFFER_SIZE = 20

def prog_buffer(length):
    return [0]*length

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


from random import choices, randint
def create_simple_program(target):
    length = randint(MIN_LEN, MAX_LEN)
    result = choices(LANGUAGE, k=length)
    return ''.join(result)

def crossover(progX, progY):
    childX = list(progX)
    childY = list(progY)
    length = min(len(progX), len(progY))
    crossIndex = int(length * CROSS_WEIGHT)
    swap = childX[0 : crossIndex]
    childX[0 : crossIndex] = progY[0 : crossIndex]
    childY[0 : crossIndex] = swap
    return (''.join(childX), ''.join(childY), crossIndex)


def evaluate_fitness(result, target):
    fitness = 0
    for i, v in enumerate(target):
        if i < len(result):
            fitness += abs(result[i] - target[i])
    return fitness


"""
def empty_target(length):
    return [0]*length

def print_prog(name, prog, target):
    result = interpret(prog, prog_buffer(BUFFER_SIZE))
    print (
        name,
        prog,
        str(result),
        evaluate_fitness(result, target)
    )



if __name__ == "__main__":
    progX = create_simple_program([1,2,3])
    print_prog('ProgX', progX, empty_target(BUFFER_SIZE))
    progY = create_simple_program([1,2,3])
    print_prog('ProgY', progX, empty_target(BUFFER_SIZE))
    childX, childY, crossIndex = crossover(progX, progY)
    print_prog('ChildX', childX, empty_target(BUFFER_SIZE))
    print_prog('ChildY', childY, empty_target(BUFFER_SIZE))
"""
