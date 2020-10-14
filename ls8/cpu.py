"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  #memory
        self.reg = [0] * 8    #registers
        self.pc = 0           #program counter
        self.running = True
        

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) < 2:
            print('please include a filename in the second argument')
            sys.exit()
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    split_file = line.split('#')
                    val = split_file[0].strip()
                    if val == "":
                        continue

                    try:
                        instruction = int(val, 2)
                    except ValueError:
                        print(f"Invalid number {n}")
                        sys.exit(1)

                    self.ram[address] = instruction
                    address += 1
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]} / {sys.argv[1]} file not found")
            sys.exit()



        # address = 0
        # #For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
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
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        
        while self.running:
            ir = self.ram_read(self.pc)  
            op_a = self.ram_read(self.pc+1)
            op_b = self.ram_read(self.pc+2)

            if ir == HLT: 
                self.running = False
                self.pc += 1

            elif ir == PRN:
                print(self.reg[op_a])
                self.pc += 2
            
            elif ir == LDI:
                self.reg[op_a] = op_b
                print(op_a)
                self.pc += 3
            
            elif ir == MUL:
                result = self.reg[op_a] + self.reg[op_b]
                print(result)
                self.pc += 3
            else:
                self.running = False
                print(f"Invalid entry: {ir}")

