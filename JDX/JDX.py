# imports
from string import ascii_lowercase
import importlib

# setup
REG = {}
for l in ascii_lowercase:
    REG[l] = None

REG['al'] = ''
REG['pc'] = 0
REG['*'] = None
REG['**'] = None
REG['fc'] = None
REG['-'] = ''


# functions
# https://stackoverflow.com/questions/20256066/python-split-string-by-spaces-except-when-in-quotes-but-keep-the-quotes/20284563#20284563
def SpaceSplit(string) :
  last = 0
  splits = []
  inQuote = None
  for i, letter in enumerate(string):
    if inQuote :
      if (letter == inQuote):
        inQuote = None
    else:
      if (letter == '"' or letter == "'"):
        inQuote = letter

    if not inQuote and letter == ' ':
      splits.append(string[last:i])
      last = i+1

  if last < len(string):
    splits.append(string[last:])

  return splits

def GetLine(n, lst):
    return lst[(n-1)]

def UpdateREG(assem):
    REG['pc'] = assem.ProgramCounter

def Strp(x):
    z = ''
    for i in x:
        if i != '.':
            z += i
    return z

def CharCount(inpt, chr):
    c = 0
    for i in inpt:
        if i == chr:
            c += 1
    return c

def Detect(inpt):
    inpt = str(inpt)
    # detect if string
    if inpt[0] == "'" and inpt[-1] == "'":
        return str

    elif inpt[0] == '"' and inpt[-1] == '"':
        return str
    
    # detect if int
    elif inpt.isdecimal() and CharCount(inpt, '.') == 0:
        return int

    # detect if float
    elif Strp(inpt).isdecimal() and CharCount(inpt, '.') == 1:
        return float
    
    else:
        return str

def LoadLIB(IsDebug, name, funclst):
    if IsDebug:
        print(f'Loading Library: {name}')

    LIB = importlib.import_module(f'LIB.{name}')
    REGDict = LIB.registers
    for key, value in REGDict.items():
        REG[key] = value
    
    return LIB.load_func(funclst)

# classes
class Assembler:
    def __init__(self):
        self.ProgramCounter = 0
        self.ValidInstructions = ['mov','ldt','rd','xrd','str','rpl','spl','add','sub',
        'mul','div','jmp','jnz','invk','require','inpt','fnc','#debug','#admin',
        'end', 'ldt2']

        self.debug = False
        self.FunctionList = []

    def Lexer(self, file):
        with open(file) as f:
            xlist = f.readlines()
            ylist = [SpaceSplit(y) for y in xlist]
            zlist = [[v.strip('\n') for v in x] for x in ylist]
        return zlist
    
    def Loop(self, tokens):
        global REG
        while True:
            self.ProgramCounter += 1
            UpdateREG(self)
            try:
                line = GetLine(self.ProgramCounter, tokens)
            except IndexError:
                print('Program Complete')
                if self.debug:
                    for key, val in REG.items():
                        print(f'{key} - {type(val)} - {val}')
                exit()

            Instruction = line[0]
            if Instruction == '' or Instruction == '\n':
                continue

            if Instruction[0] == ';':
                continue

            if Instruction not in self.ValidInstructions:
                print(f'[WARN] unknown instruction/flag: {Instruction}')
                continue

            match Instruction:
                case '#debug':
                    self.debug = True

                case 'mov':
                    if line[2] == '[\*\]':
                        REG[line[1]] = REG['*']
                    elif line[2] == '[\**\]':
                        REG[line[1]] = REG['**']
                    else:
                        typ = Detect(line[2])
                        REG[line[1]] = typ(line[2].strip('"').strip("'"))

                    if self.debug:
                        print(f'Moved value {line[2]} into register {line[1]} (mov {line[1]} {line[2]})')

                case 'ldt':
                    REG['*'] = REG[line[1]]
                    if self.debug:
                        print(f'Saved value {REG[line[1]]} into register * (ldt {line[1]})')
                
                case 'ldt2':
                    REG['**'] = REG[line[1]]
                    if self.debug:
                        print(f'Saved value {REG[line[1]]} into register ** (ldt2 {line[1]})')

                case 'add':
                    if line[2] == '[\*\]':
                        REG[line[1]] += REG['*']
                    elif line[2] == '[\**\]':
                        REG[line[1]] += REG['**']
                    else:
                        typ = Detect(line[2])
                        REG[line[1]] += typ(line[2])
                        
                    if self.debug:
                        z = REG[line[2].replace('[\*\]', '*')]
                        z = REG[line[2].replace('[\**\]', '**')]
                        print(f'Added {z} to register {line[1]} (add {line[1]} {line[2]})')
                
                case 'sub':
                    if line[2] == '[\*\]':
                        REG[line[1]] -= REG['*']
                    elif line[2] == '[\**\]':
                        REG[line[1]] += REG['**']
                    else:
                        typ = Detect(line[2])
                        REG[line[1]] -= typ(line[2])
                        
                    if self.debug:
                        z = REG[line[2].replace('[\*\]', '*')]
                        z = REG[line[2].replace('[\**\]', '**')]
                        print(f'Subtracted {z} from register {line[1]} (sub {line[1]} {line[2]})')
                
                case 'mul':
                    if line[2] == '[\*\]':
                        REG[line[1]] *= REG['*']
                    elif line[2] == '[\**\]':
                        REG[line[1]] += REG['**']
                    else:
                        typ = Detect(line[2])
                        REG[line[1]] *= typ(line[2])
                        
                    if self.debug:
                        z = REG[line[2].replace('[\*\]', '*')]
                        z = REG[line[2].replace('[\**\]', '**')]
                        print(f'Multiplied register {line[1]} by {z} (mul {line[1]} {line[2]})')
                
                case 'div':
                    if line[2] == '[\*\]':
                        REG[line[1]] /= REG['*']
                    elif line[2] == '[\**\]':
                        REG[line[1]] += REG['**']
                    else:
                        typ = Detect(line[2])
                        REG[line[1]] /= typ(line[2])
                        
                    if self.debug:
                        z = REG[line[2].replace('[\*\]', '*')]
                        z = REG[line[2].replace('[\**\]', '**')]
                        print(f'Divided register {line[1]} by {z} (div {line[1]} {line[2]})')
                
                case 'rd':
                    REG[line[1]] = int(REG[line[1]])
                    if self.debug:
                        print(f'Converted register {line[1]} to integer (rd {line[1]})')
                
                case 'xrd':
                    REG[line[1]] = float(REG[line[1]])
                    if self.debug:
                        print(f'Converted register {line[1]} to floating-point-number (xrd {line[1]})')
                
                case 'str':
                    REG[line[1]] = str(REG[line[1]])
                    if self.debug:
                        print(f'Converted register {line[1]} to string (str {line[1]})')

                case 'invk':
                    if line[1] == 'AL_PRT':
                        print(REG['al'])
                        if self.debug:
                            print('invoked command AL_PRT (invk AL_PRT)')
                
                case 'jmp':
                    self.ProgramCounter = (int(line[1])-1)
                    if self.debug:
                        print(f'Jumped to line {line[1]} (jmp {line[1]})')
                
                case 'jnz':
                    try:
                        if float(REG[line[1]]) != 0.0:
                            self.ProgramCounter = (int(line[2])-1)
                            if self.debug:
                                print(f'Jumped to line {line[2]} (jnz {line[1]} {line[2]})')
                    except:
                        self.ProgramCounter = (int(line[2])-1)
                        if self.debug:
                            print(f'Jumped to line {line[2]} (jnz {line[1]} {line[2]})')
                
                case 'require':
                    self.FunctionList = LoadLIB(self.debug, line[1], self.FunctionList)
                
                case 'fnc':
                    found = False
                    for func in self.FunctionList:
                        if line[1] == func.__name__:
                            found = True
                            ln = []
                            for x in line[2:]:
                                if x == '[\*\]':
                                    ln.append(REG['*'])
                                elif x == '[\**\]':
                                    ln.append(REG['**'])
                                else:
                                    typ = Detect(x)
                                    ln.append(typ(x.strip('"').strip("'")))

                            x, REG = func(ln, REG)
                            REG['fc'] = x
                            if self.debug:
                                print(f'Executed function: {line[1]}')
                            continue
                    if not found:
                        print(f'[WARN] function {line[1]} not found, ignoring')
                
                case 'inpt':
                    REG['-'] = input(line[1][1:-1])
                
                case 'end':
                    print('Program Complete')
                    if self.debug:
                        for key, val in REG.items():
                            print(f'{key} - {type(val)} - {val}')
                    exit()
                    


# execution
if __name__ == '__main__':
    assem = Assembler()
    assem.Loop(assem.Lexer('test.jdx'))
