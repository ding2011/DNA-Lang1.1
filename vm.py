import sys

class DNAVM:
    def __init__(self):
        self.memory = [0] * 256
        self.stack = []
        self.pc = 0
        self.instructions = {
            0b0000: self.nop,
            0b0001: self.push,
            0b0010: self.pop,
            0b0011: self.dup,
            0b0100: self.add,
            0b0101: self.sub,
            0b0110: self.mul,
            0b0111: self.div,
            0b1000: self.jmp,
            0b1001: self.jz,
            0b1010: self.call,
            0b1011: self.ret,
            0b1100: self.load,
            0b1101: self.store,
            0b1110: self.read,
            0b1111: self.write,
        }
    
    def load_binary(self, filename):
        try:
            with open(filename, 'rb') as f:
                code = f.read()
            for i, byte in enumerate(code):
                self.memory[i] = byte
            print(f"Loaded {len(code)} bytes program")
            return True
        except Exception as e:
            print(f"Load error: {e}")
            return False
    
    def run(self):
        self.pc = 0
        while self.pc < len(self.memory) and self.memory[self.pc] != 0:
            instruction = self.memory[self.pc]
            opcode = (instruction >> 4) & 0b1111
            operand = instruction & 0b1111
            
            print(f"Executing instruction: PC={self.pc}, Byte={instruction:02X}, Opcode={opcode:04b}, Operand={operand:04b}, Stack={self.stack}")
            
            if opcode in self.instructions:
                self.instructions[opcode](operand)
            else:
                print(f"Unknown opcode: {opcode:04b}")
                break
            
            self.pc += 1
    
    # Push value to stack
    def push(self, operand):
        self.stack.append(operand)
    
    # Subtraction: b - a (pop a first, then pop b)
    def sub(self, operand):
        if len(self.stack) >= 2:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append((b - a) & 0xFF)
    
    # Division: b // a (pop a first, then pop b, a ≠ 0)
    def div(self, operand):
        if len(self.stack) >= 2:
            a = self.stack.pop()
            b = self.stack.pop()
            if a != 0:
                self.stack.append((b // a) & 0xFF)
    
    # Addition: a + b
    def add(self, operand):
        if len(self.stack) >= 2:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append((a + b) & 0xFF)
    
    # Multiplication: a * b
    def mul(self, operand):
        if len(self.stack) >= 2:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append((a * b) & 0xFF)
    
    # No operation
    def nop(self, operand):
        pass
    
    # Pop value from stack
    def pop(self, operand):
        return self.stack.pop() if self.stack else 0
    
    # Duplicate top of stack
    def dup(self, operand):
        if self.stack:
            self.stack.append(self.stack[-1])
    
    # Jump to address
    def jmp(self, operand):
        self.pc = operand - 1
    
    # Jump if top of stack is zero
    def jz(self, operand):
        if self.stack and self.stack[-1] == 0:
            self.pc = operand - 1
    
    # Call function (push return address)
    def call(self, operand):
        self.stack.append(self.pc + 1)
        self.pc = operand - 1
    
    # Return from function (pop return address)
    def ret(self, operand):
        if self.stack:
            self.pc = self.stack.pop() - 1
    
    # Load value from memory
    def load(self, operand):
        address = operand & 0b1111
        self.stack.append(self.memory[address])
    
    # Store value to memory
    def store(self, operand):
        address = operand & 0b1111
        if self.stack:
            self.memory[address] = self.stack.pop()
    
    # Read input (simulated)
    def read(self, operand):
        self.stack.append(42)  # Simulated input value
    
    # Write value to output
    def write(self, operand):
        if self.stack:
            print(f"Output: {self.stack.pop()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vm.py binary_file.bin")
        sys.exit(1)
    
    vm = DNAVM()
    if vm.load_binary(sys.argv[1]):
        try:
            vm.run()
            print("Execution complete")
        except Exception as e:
            print(f"Execution error: {e}")
