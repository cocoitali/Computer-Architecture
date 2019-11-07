import sys
​
PRINT_TIM      = 0b01
HALT           = 0b10
PRINT_NUM      = 0b11
SAVE           = 0b100
ADD            = 0b101
PRINT_REGISTER = 0b110
PUSH           = 0b111
POP            = 0b1000
CALL           = 0b1001
RET            = 0b1010
​
call_ret_program_in_words = [
    SAVE,
    2,
    8,
    PRINT_TIM,
    CALL,
    2,
    PRINT_TIM,
    HALT,
    PRINT_TIM,
    RET,
    ]
​
call_ret_program_in_binary_remember_to_remove_the_commas = [
    0b100,
    0b10,
    0b1000,
    0b01,
    0b1001,
    0b10,
    0b01,
    0b10,
    0b01,
    0b1010,
]
​
memory = [0] * 255
​
if len(sys.argv) < 2:
    print('hey tell me what file to read in')
try:
    address = 0
    with open(sys.argv[1]) as file:
        for line in file:
            split_line = line.split('#')
            maybe_command = split_line[0]
            if len(maybe_command) > 0:
                maybe_command = maybe_command.strip()
                if maybe_command == '':
                    pass
                else:
                    command = int(maybe_command, 2)
                    memory[address] = command
                    address += 1
​
except FileNotFoundError:
    print("hey that file doesn't exist")
​
registers = [0] * 8
​
registers[7] = 0xF4
​
running = True
pc = 0
​
while running:
    command = memory[pc]
​
    if command == PRINT_TIM:
        print('TIM!')
        pc += 1
​
    elif command == PRINT_NUM:
        number_to_print = memory[pc + 1]
        print(number_to_print)
​
        pc += 2
​
    elif command == SAVE:
        register = memory[pc + 1]
        num = memory[pc + 2]
        registers[register] = num
        pc += 3
​
    elif command == ADD:
        first_register_address = memory[pc + 1]
        second_register_address = memory[pc + 2]
​
        first_num = registers[first_register_address]
        second_num = registers[second_register_address]
​
        total = first_num + second_num
​
        registers[first_register_address] = total
​
        pc += 3
​
    elif command == PRINT_REGISTER:
        register_address = memory[pc + 1]
​
        value_to_print = registers[register_address]
​
        print(value_to_print)
​
        pc += 2
​
    elif command == PUSH:
        # decrement the stack pointer
        registers[7] -= 1
​
        # get what is in the register
        register_address = memory[pc + 1]
        value = registers[register_address]
​
        # store it at that point in the stack
        SP = registers[7]
        memory[SP] = value
​
        pc += 2
​
    elif command == POP:
        # Copy the value from the address pointed to by SP to the given register.
        SP = registers[7]
        value = memory[SP]
        target_register_address = memory[pc + 1]
        registers[target_register_address] = value
​
        # Increment SP
        registers[7] += 1
​
        pc += 2
​
    elif command == CALL:
        # store the next command on the stack
        return_address = pc + 2
        registers[7] -= 1
        SP = registers[7]
        memory[SP] = return_address
​
        # get the subroutine_location out of the register
        # where it was previously stored
        register_address = memory[pc + 1]
        subroutine_location = registers[register_address]
​
        # set the program counter to the location we're jumping to
        pc = subroutine_location
​
    elif command == RET:
        # run the same logic as pop
        # get the stack pointer
        SP = registers[7]
        # get the value there
        return_address = memory[SP]
        # move the stack pointer back up
        registers[7] += 1
​
        # set the pc to the return address
        pc = return_address
​
    elif command == HALT:
        running = False
​
    else:
        print("I don't know what's going on")
        running = False