registers = {}
import math

def sqrt(line, reg):
    return math.sqrt(line[0]), reg

def tan(line, reg):
    return math.degrees(math.tan(line[0])), reg
def atan(line, reg):
    return math.degrees(math.atan(line[0])), reg

def cos(line, reg):
    return math.degrees(math.cos(line[0])), reg
def acos(line, reg):
    return math.degrees(math.acos(line[0])), reg

def sin(line, reg):
    return math.degrees(math.sin(line[0])), reg
def asin(line, reg):
    return math.degrees(math.asin(line[0])), reg


def load_func(lst):
    lst.append(sqrt)
    lst.append(tan)
    lst.append(atan)
    lst.append(cos)
    lst.append(acos)
    lst.append(sin)
    lst.append(asin)
    return lst