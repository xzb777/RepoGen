from games.maze import Robot
from hardware.cpu import CPU
from assembler import assemble_binary

delay = 0.0
robot = Robot(delay=delay)
program = assemble_binary('robot.asm')
cpu = CPU(program)
cpu.run(write_to_input=robot.get_front_cell_bit,read_from_output=robot.move)


