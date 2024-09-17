
def and_(*args:bool)->int:
    return int(all(args))


def or_(*args:bool)->int:
    return int(any(args))

def not_(*args:bool)->int:
    return int(not all(args))

def nor(*args:bool)->int:
    return int(not_( or_(*args) ))

def nand(*args:bool)->int:
    return int(not_( and_(*args) ))

def xor(a:bool, b:bool)->int:
    return int(a ^ b)

def xnor(a:bool, b:bool)->int:
    return int(not xor(a, b))

