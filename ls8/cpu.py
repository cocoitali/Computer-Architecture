"""CPU functionality."""

import sys

HLT = 0b00000001  # listed alphabetically
LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes, index == 1 byte
        self.reg = [0] * 8  # index is register
        self.pc = 0  # program counter
        self.hlt = False
        # SP points at the value at the top of the stack (most recently pushed), or address `F4` if the stack is empty
        self.sp = 0xF4
        self.ops = {  # branch table
            HLT: self.op_hlt,
            LDI: self.op_ldi,
            MUL: self.op_mul,
            PRN: self.op_prn,
            PUSH: self.op_push,
            POP: self.op_pop
        }

    def op_hlt(self, operand_a, operand_b):
        self.hlt = True

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def op_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def op_push(self, operand_a, operand_b):
        operand_a = self.ram_read(self.pc + 1)
        # not done yet

    def op_pop(self, operand_a, operand_b):
        operand_a = self.ram_read(self.pc + 1)
        # not done yet

    def op_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def ram_read(self, address):
        # getting something from this address and accessing the value
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 ---->when split--['100000010', LDI RO,8, '/n']
        #     0b00000000,                             ['00000000', '/n']
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(filename) as file:
            for line in file:
                # get each line in file, split based on #
                comment_split = line.split('#')
                instruction = comment_split[0]

                if instruction == '':  # if there's a blank line, skip
                    continue

                first_bit = instruction[0]  # get the first bit

                if first_bit == '0' or first_bit == '1':  # check if 0 or 1
                    # only need first 8 values, covert to binary (base 2)
                    self.ram[address] = int(instruction[:8], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":  # add multiply instruction
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while not self.hlt:
            # command = self.ram[self.pc]
            command = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            op_size = command >> 6  # how many operands included in this instruction
            op_set = ((command >> 4) & 0b1) == 1

            # if command == HLT:
            #     running = False

            # if command == LDI:
            #     self.reg[operand_a] = operand_b
            #     # self.pc += 3

            # if command == PRN:
            #     print(self.reg[operand_a])
            #     # self.pc += 2

            if command in self.ops:
                self.ops[command](operand_a, operand_b)

            if not op_set:
                self.pc += op_size + 1

            # else:
            #     print(f"Unknown instruction: {command}")
            #     sys.exit()
