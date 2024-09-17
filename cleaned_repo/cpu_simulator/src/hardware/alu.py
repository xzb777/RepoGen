
from .gates import and_, or_, not_
from .basic_components import AddSub, Mux8Bit


class ALU:
    """"
ALU rules;
    control1 | control2
    0        | 0        = Add
    0        | 1        = Or
    1        | 0        = Subtract
    1        | 1        = And

    input1 - input2 = output   
    zero() = True if all the output is False
    negative() = True if the number is negative
    overflow() = True if the number is overflowed when doing addition
    carry_out() = True if the number is overflowed when doing subtraction (in2 > in1) 
        """
    def __init__(self, input1: list[bool], input2: list[bool], control1:bool, control2:bool):
        if len(input1) != 8 or len(input2) != 8:
            raise ValueError("Both inputs must be 8 bits long.")
        self.input1 = input1
        self.input2 = input2
        self.control1 = control1
        self.control2 = control2
    
        # create add sub
        add_sub = AddSub(self.input1, self.input2, self.control1)
        add_sub_out = add_sub.output() # if control1 == True then subtract else add
        
        self.add_sub_overflow = add_sub.overflow() # used when doing addition
        self.add_sub_borrow_out = add_sub.borrow_out() # used when doing subtraction (in2 > in1)


        #create bitwise operations
        and_out = [and_(in1, in2) for in1, in2 in zip(self.input1, self.input2)]
        or_out = [or_(in1, in2) for in1, in2 in zip(self.input1, self.input2)]

        #pass and or output to mux
        and_or_mux = Mux8Bit(and_out, or_out, self.control1)
        and_or_mux_out = and_or_mux.output()

        #pass and or mux out + add sub out to mux
        self.and_or_add_sub_mux = Mux8Bit(and_or_mux_out, add_sub_out, self.control2)

    @property
    def out(self):
        """returns the output of the ALU"""
        return self.and_or_add_sub_mux.output()

    def zero(self):
        """returns True if all the output is False"""
        # or_ all the output then invert, this or gate will be true if any of the output is true
        #unpack the list of out() and pass it to or_
        # then not_ the or_ output
        return not_( or_(*self.out()))   

    def negative(self):
        """returns True if the number is negative"""
        return self.out()[0]

    def overflow(self):
        """returns True if the number is overflowed when doing addition"""
        return self.add_sub_overflow

    def carry_out(self):
        """"returns True if the number is overflowed when doing subtraction (in2 > in1)"""
        return self.add_sub_borrow_out
    


