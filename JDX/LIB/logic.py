registers = {}

def equal(line, reg):
    if line[0] == line[1]:
        x = 1
    else:
        x = 0
    return x, reg

def not_equal(line, reg):
    if line[0] == line[1]:
        x = 1
    else:
        x = 0
    return x, reg

def more_than(line, reg):
    if line[0] == line[1]:
        x = 1
    else:
        x = 0
    return x, reg

def less_than(line, reg):
    if line[0] == line[1]:
        x = 1
    else:
        x = 0
    return x, reg

def more_than_or_equal(line, reg):
    if line[0] == line[1]:
        x = 1
    else:
        x = 0
    return x, reg

def less_than_or_equal(line, reg):
    if line[0] == line[1]:
        x = 1
    else:
        x = 0
    return x, reg

def load_func(lst):
    lst.append(equal)
    lst.append(not_equal)
    lst.append(more_than)
    lst.append(less_than)
    lst.append(more_than_or_equal)
    lst.append(less_than_or_equal)
    return lst