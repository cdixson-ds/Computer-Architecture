"""CPU functionality."""

import sys

SP = 7
LDI = 0b10000010  #load immediate, store a value in register, or 'set this register to this value'
PRN = 0b01000111  #a pseudo-instruction that prints the numeric value stored in a register
HLT = 0b00000001  #halt the CPU and exit the emulator
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  #memory
        self.reg = [0] * 8    #registers
        self.pc = 0           #program counter
        # self.running = True
        

    def ram_read(self, address):    #should accept the address to read and return the value stored there
        if address < len(self.ram):
            return self.ram[address]
        else:
            return None

    def ram_write(self, value, address):    #should accept a value to write and address to write it to
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        

        if len(sys.argv) < 2:
            print('please include a filename in the second argument')
            sys.exit()
        try:
            address = 0
            with open(sys.argv[1]) as filename:
                for line in filename:
                    split_file = line.strip().split('#')
                    val = split_file[0].strip()
                    if val == "":
                        continue

                    instruction = int(val, 2)
                    self.ram[address] = instruction
                    address += 1
                    
        except:
            print("file not found")
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB":
        #     self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        # elif op == PUSH:
        #     self.reg[SP] -= 1
        #     reg_num = self.ram_read(self.pc+1)
        #     val = self.reg[reg_num]
        #     add_top = self.reg[SP]
        #     self.ram[add_top] = val
        #     self.pc += 2

        # elif op == POP:

        #     reg_num = self.ram_read(self.pc + 1)
        #     add_top = self.reg[SP]
        #     val = self.ram_read[add_top]
        #     self.reg[reg_num] = val
        #     self.reg[SP] += 1
        #     self.pc += 2

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
            str_ir = str(ir)

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
                #self.alu(ir, op_a, op_b)
                result = self.reg[op_a] * self.reg[op_b]
                print(result)
                self.pc += 3

            elif ir == PUSH:
                self.reg[SP] -= 1
                reg_num = self.ram_read(self.pc+1)
                value = self.reg[reg_num]
                add_top = self.reg[SP]
                self.ram[add_top] = value
                self.pc += 2

            elif ir == POP:
                reg_num = self.ram_read(self.pc + 1)
                add_top = self.reg[SP]
                value = self.ram_read(add_top)
                self.reg[reg_num] = value
                self.reg[SP] += 1
                self.pc += 2

            else:
                print(f"Invalid entry: {ir}")
                sys.exit()

