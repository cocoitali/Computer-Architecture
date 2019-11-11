import sys

# instructions
PRINT_BEEJ     = 1 # represented in decimal here
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4
PRINT_REGISTER = 5
ADD            = 6

# memory = [
#     PRINT_BEEJ,
#     SAVE, # SAVE 65 to register 2
#     65,
#     2,
#     SAVE, # SAVE 20 to register 3
#     20,
#     3,
#     ADD, # ADD register 2 + register 3
#     2,
#     3,
#     PRINT_REGISTER, # Print the value in register 2
#     2,
#     HALT
# ]

ram = [0] * 256
register = [0] * 8

pc = 0 # pointer, program counter, index of where we're looking at in memory
running = True

def load_memory():
    address = 0
    try:
        with open(sys.argv[1]) as file:
            for line in file:
                comment_split = line.split('#')
                possible_number = comment_split[0]

                if possible_number == '' or possible_number == '\n':
                    continue
                instruction = int(possible_number)
                ram[address]+= 1
                
    except IOError: #FileNotFoundError
        print('I cannot find that file, check the name')
        sys.exit(2)

while running:
    command = ram[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1 #increment program counter
        

    elif command == PRINT_NUM:
        num = ram[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        num = ram[pc +1]
        reg = ram[pc +2]
        register[reg] = num
        pc += 3

    elif command == PRINT_REGISTER:
        reg = ram[pc + 1]
        print(register[reg])
        pc += 2
    
    elif command == ADD:
        reg_a = ram[pc + 1]
        reg_b = ram[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3

    elif command == HALT:
        running = False

    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)

    