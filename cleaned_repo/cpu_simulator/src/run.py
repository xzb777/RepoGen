
from hardware.cpu import CPU
from assembler import assemble_binary


program = assemble_binary('program2.asm')

# funtions to be passed to the cpu
def write_to_input():
    return [0,0,0,0,0,0,0,1]
def read_from_output(value):
    if value != [0,0,0,0,0,0,0,0]:
        print('--------------')
        print('result:',value)
        print('--------------')

cpu = CPU(program)
cpu.run(write_to_input=write_to_input, read_from_output=read_from_output)
