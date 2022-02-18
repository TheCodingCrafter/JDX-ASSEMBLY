registers = {}
import random

def rand(line, reg):
    return random.randint(int(line[0]), int(line[1])), reg



def load_func(lst):
    lst.append(rand)
    return lst