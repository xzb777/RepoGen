
def get_labels(file)->dict:
    """Finds the positions of each label relative to the pc"""
    pc = 0
    labels = {}
    for line in file:
        #check line not empty
        if  line.strip():
            # check that pc is not greater than 63
            if pc > 63:
                raise ValueError('Program too long, label must be within 64 lines')
            line = line.strip()
            if line.startswith('#'):
                continue
            elif line.startswith('label'):
                # get the name of the label
                label = line.split(' ')[1]
                # make sure the label is not an int
                if label.isdigit():
                    raise ValueError(f'Invalid label: {label} is an int')
                # make sure the label is not already in the dictionary
                if label in labels:
                    raise ValueError(f'Duplicate label definition: {label}')
                # add the label to the dictionary
                labels[label] = pc
            else:
                pc += 1
    return labels


def immediate_values(line,labels):
    """For each line determine if it is an immediate value"""
    # check if the line is a comment
    line = line.split('#')[0].strip()
    # check if the line is empty
    if not line:
        return None
    # check if the line is a label
    if line.startswith('label'):
        return None
    # check if the line is in labels dict
    if line in labels:
        value = labels[line]
        # convert the value to binary
        byte_value = [int(bit) for bit in format(value, '08b')]
        return byte_value
    # check if the line is an immediate value
    if line.isdigit():
        value = int(line)
        if value < 0 or value > 63:
            raise ValueError(f'Invalid immediate value: {value}')
        # convert the value to binary
        byte_value = [int(bit) for bit in format(value, '08b')]
        return byte_value


def copy_instructions(line):
    """For each line determine if it is a copy instruction"""
    line = line.split('#')[0].strip()
    if not line:
        return None
    if line.startswith('label'):
        return None
    if line.startswith('copy'):
        cp = [1, 0]
        parts = line.split(' ')
        src = [int(bit) for bit in format(int(parts[1]), '03b')]
        dst = [int(bit) for bit in format(int(parts[2]), '03b')]
        return cp + src + dst


def operate_instructions(line):
    """For each line determine if it is an operate instruction"""
    line = line.split('#')[0].strip()
    if not line:
        return None
    if line.startswith('label'):
        return None
    if line in ['add', 'or', 'sub', 'and']:
        if line == 'add':
            return [0, 1, 0, 0, 0, 0, 0, 0]
        elif line == 'or':
            return [0, 1, 0, 0, 0, 0, 0, 1]
        elif line == 'sub':
            return [0, 1, 0, 0, 0, 0, 1, 0]
        elif line == 'and':
            return [0, 1, 0, 0, 0, 0, 1, 1]


def jump_instructions(line):
    """For each line determine if it is a jump instruction"""
    line = line.split('#')[0].strip()
    if not line:
        return None
    if line.startswith('label'):
        return None
    # if line starts with eval
    if line.startswith('eval'):
        # create a varible for the symbol
        symbol = line.split(' ')[1]
        if symbol == 'never':
            value = 0
        elif symbol == '=':
            value = 1
        elif symbol == '<':
            value = 2
        elif symbol == '<=':
            value = 3
        elif symbol == 'always':
            value = 4
        elif symbol == '!=':
            value = 5
        elif symbol == '>=':
            value = 6
        elif symbol == '>':
            value = 7   
        else:
            raise ValueError(f'Unknown opcode: {symbol}')
        return [1, 1, 0, 0, 0] + [int(bit) for bit in format(value, '03b')]
        

def assemble_binary(filename:str):
    """takes in an assembly file and returns binary program"""
    program = []
    with open(filename, 'r') as f:
        """start by finding all the labels"""
        labels = get_labels(f)
        f.close()
    with open(filename, 'r') as f:
        # for each line in the file
        for line in f:
            a =immediate_values(line,labels)
            b = copy_instructions(line)
            c = operate_instructions(line)
            d = jump_instructions(line)
            # add the line to the program
            if a:
                program.append(a)
            elif b:
                program.append(b)
            elif c:
                program.append(c)
            elif d:
                program.append(d)
        f.close()
    return program




