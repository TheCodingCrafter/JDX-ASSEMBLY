import os
registers = {}

def cmd(line, reg):
    return os.system(line[0]), reg

def getuser(line, reg):
    return os.getlogin(), reg

def getpid(line, reg):
    return os.getpid(), reg

def get_exec_path(line, reg):
    return os.get_exec_path(), reg

def get_current_working_directory(line, reg):
    return os.getcwd(), reg

def load_func(lst):
    lst.append(cmd)
    lst.append(getuser)
    lst.append(getpid)
    lst.append(get_exec_path)
    lst.append(get_current_working_directory)
    return lst
