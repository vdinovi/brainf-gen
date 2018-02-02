class InvalidSymbol(Exception):
    def __init__(self, msg):
        self.msg =  msg
MIN_LEN = 5
MAX_LEN = 10
CROSS_WEIGHT = 0.4
LANGUAGE = ('>', '<', '+', '-')

def interpet(program, array):
    index = 0
    for op in program:
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


def evaluate_fitness(prog, target):
    raise StandardError("NYI")



if __name__ == "__main__":
    progX = create_simple_program([1,2,3])
    progY = create_simple_program([1,2,3])
    cross = crossover(progX, progY)
    print(str((progX, progY)) + ' -> ' + str(cross))
