from .gates import  and_
from .basic_components import Decoder, Control, Comparison
from .alu import ALU
from .registers import Registers



"""
Instruction set implemented by class Control
00 = Immediate
01 = operate (add, subtract, and, or)
10 = copy (source, destination)
11 = Edit program counter/ evaluate comparison

IMMEDIATE:
moves the number into reg0, example:
00 000 000 = move 0 into reg0
00 000 001 = move 1 into reg0
notice that the 2 MSB must always be false

OPERATE:
2 LSB determine operation as per alu specs
always operates on reg1 and reg2 and stores in reg3
ALU rules;
    control1 | control2
    0        | 0        = Add
    0        | 1        = Or
    1        | 0        = Subtract
    1        | 1        = And

COPY:
3 bits determine source register, next 3 bits determine destination register. 
110 refers to input or output

10 000 010 = move from reg0 to reg2
10 000 110 = move from reg0 to out 
10 110 000 = move from input to reg0

UPDATE PC:
Update the pc to the value in reg0 if comparison is true
"""


class CPU:     

    class Cycle:
        def __init__(self, cpu, program_instruction_byte):
            self.cpu = cpu
            self.program_instruction_byte = program_instruction_byte
            self.control = Control(self.program_instruction_byte)
            self.decoder1 = Decoder(self.program_instruction_byte[2:5]) # source load
            self.decoder2 = Decoder(self.program_instruction_byte[5:8]) # destination save

            self.execute()

        def execute(self):
            if self.cpu.verbose:
                print('--------------')
                print()
                print('pc:', self.cpu.pc - 1)
                if self.control.output[0]:
                    print('Immediate ', self.program_instruction_byte)
                elif self.control.output[1]:
                    print('Operate ', self.program_instruction_byte)
                elif self.control.output[2]:
                    print('Copy', self.program_instruction_byte)
                elif self.control.output[3]:
                    print('Update ', self.program_instruction_byte)
                print()

            # disable all registers, input, and output from loading and saving
            self.cpu.registers.load = [0] * 6
            self.cpu.registers.save = [0] * 6
            self.cpu.registers.input_load = 0
            self.cpu.registers.output_save = 0

            #immediate
            self.cpu.registers.save[0] = self.control.output[0]
            self.cpu.registers.write(self.program_instruction_byte)

            #operate
            alu = ALU(self.cpu.registers.registers[1], self.cpu.registers.registers[2], self.program_instruction_byte[6], self.program_instruction_byte[7])
            # activate reg3 save signal if operate
            self.cpu.registers.save[3] = self.control.output[1]  
            # ALU should not write to the bus, but only to reg3
            self.cpu.registers.write_to_register(3, alu.out)

            
            #copy
            #bitwise and_ the decoder output and control output[2] to determine if load/save
            self.cpu.registers.load = [and_(self.control.output[2], x) for x in self.decoder1.output[:6]] #source
            self.cpu.registers.save = [and_(self.control.output[2], x) for x in self.decoder2.output[:6]] #destination
            self.cpu.registers.input_load = and_(self.decoder1.output[6], self.control.output[2]) #cpu input
            self.cpu.registers.output_save = and_(self.decoder2.output[6], self.control.output[2]) #cpu output
            # Read from the source registers and write to the destination registers
            data = self.cpu.registers.read()
            self.cpu.registers.write(data)

            #evaluate
            self.cpu.registers.load[3] = self.control.output[3]
            compare = Comparison(control=self.program_instruction_byte, byte=self.cpu.registers.read())
            if and_(self.control.output[3], compare.out):
                """PC has not yet been implemented logically"""
                # get int value of reg0
                reg0 = int(''.join(str(x) for x in self.cpu.registers.registers[0]), 2)
                self.cpu.pc = reg0


            if self.cpu.verbose:
                #for each of 6 reg print value as well as if it is loading or saving
                for i in range(6):
                    print('reg'+str(i)+':', self.cpu.registers.registers[i], 'load:', self.cpu.registers.load[i], 'save:', self.cpu.registers.save[i])
                if self.cpu.registers.input_load:
                    print('input:', self.cpu.registers.input, 'input_load:', self.cpu.registers.input_load)
                if self.cpu.registers.output_save:
                    print('output:', self.cpu.registers.output, 'output_save:', self.cpu.registers.output_save)

    
    def __init__(self, program, verbose=True):
        self.registers = Registers()
        self.program = program
        self.pc = 0  # Program Counter not yet implemented logically
        self.verbose = verbose


    def run(self, write_to_input:callable=None, read_from_output:callable=None):
        """You can pass in a function to write to input and read from output.
        Read from output must take an argument that will be the cpu's output"""
        while self.pc < len(self.program):

            #each cycle clear old i/o
            self.registers.input = [0] * 8
            self.registers.output = [0] * 8
            # increment program counter This is done now so as not to interfere when updated by the program
            self.pc += 1 
            # check if we need to write to input
            if write_to_input:
                self.registers.input = write_to_input()
            # execute the cycle
            self.Cycle(self, self.program[self.pc - 1])
            # check if we need to read from output
            if read_from_output:
                read_from_output(self.registers.output)
            print()
            print('pc:', self.pc)
