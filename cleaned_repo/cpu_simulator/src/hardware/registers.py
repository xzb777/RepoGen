
from .gates import or_

class Registers:
    def __init__(self):
        self.registers = [ [0] * 8 for _ in range(6) ]
        self.save = [0] * 6
        self.load = [0] * 6

        self.input = [0] * 8
        self.input_load = 0
        self.output = [0] * 8
        self.output_save = 0

    def read(self):
        # or_ all the registers if load is high
        return_bytes = [0] * 8
        for i in range(8):
            for j in range(6):
                if self.load[j]:
                    return_bytes[i] = or_(return_bytes[i], self.registers[j][i])
            if self.input_load:
                return_bytes[i] = or_(return_bytes[i], self.input[i])
        return return_bytes

    def write(self, data):
        # Write to the registers if save is high
            for i in range(6):
                if self.save[i]:
                    self.registers[i] = data
            if self.output_save:

                self.output = data
    
    def write_to_register(self, register, data):
        if self.save[register]:
            self.registers[register] = data

