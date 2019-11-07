PRINT_TIM = 0b01
HALT = 0b10
PRINT_NUM = 0b11
NUM_TO_PRINT = 0b01

memory = [
    PRINT_TIM,
    PRINT_NUM,
    0b01,
    PRINT_TIM,
    PRINT_TIM,
    HALT,
]

running = True
pc = 0

while running: 
    command = memory[pc]

    if command == PRINT_TIM:
        print('TIM')
        pc += 1

    elif command == PRINT_NUM:
        number_to_print = memory[pc + 1]
        print(number_to_print)
        pc += 2


    elif command == HALT:
        running = False

    else: 
        print("I don't know what's going on")
        running = False