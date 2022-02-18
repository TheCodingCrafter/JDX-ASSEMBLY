import time
registers = {}

def wait(line, reg):
    timez = int(line[0])
    if line[1] == 's':
        timez = timez
    elif line[1] == 'ns':
        timez = timez/1000000000
    elif line[1] == 'ms':
        timez = timez/1000000
    time.sleep(timez)

def timenow(line, reg):
    return time.time(), reg

def load_func(lst):
    lst.append(wait)
    return lst