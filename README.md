 # DNA-Lang1.1
DNA-Lang: A Minimal Virtual Machine Language Based on DNA Bases
 
License: MIT
 
Project Overview
 
DNA-Lang is a conceptual programming language inspired by DNA bases (A/T/C/G), simulating biomolecular operations for simple computations. The current version supports basic arithmetic operations (addition/subtraction/multiplication/division), stack manipulation, and flow control, aiming to explore the intersection of biocomputing and traditional programming.
 
Features
 
1. Arithmetic Operations: ADD, SUB, MUL, DIV

2. Stack Manipulation: PUSH, POP, DUP

3. Control Flow: JMP (unconditional jump), JZ (conditional jump if zero)

4. I/O Operations: Simulated input (READ) and terminal output (WRITE)

5. Toolchain: Compiler (DNA → binary) and virtual machine (VM)
 
Environment Setup
 
Dependencies: Python 3.6+

Installation: No setup required; run source code directly
 
Usage Guide
 
1. Write DNA Code (.dna file)
dna
  
Example: Calculate 3 + 2 = 5  
ATG   # PUSH 3 
ATC   # PUSH 2   
TA    # ADD
GGAA  # WRITE 0 
 

2. Compile to Binary
bash
  
python dna_compiler.py your_dna_file.dna generated_bin_file.bin 
 

3. Run Virtual Machine
bash
  
python vm.py generated_bin_file.bin 
 
Output:
plaintext
  
Output: 5  
 
 
Instruction Set Reference

  
DNA Instruction Opcode Description Operand Length 
 AT[X]   0001  Push value (X: A=0, T=1, C=2, G=3) 1 base 
 TA   0100  Add (pop a, pop b, push a+b) None 
 TT   0101  Subtract (pop a, pop b, push b-a) None 
 TC   0110  Multiply None 
 TG   0111  Divide (b//a, a≠0) None 
 GG[XY]   1111  Write top of stack to output 2 bases 
 

 
1. Subtraction (2-3=-1→255)

  
ATC   # PUSH 2  
ATG   # PUSH 3  
TT    # SUB  
GGAA  # WRITE  
 

2. Division (6÷2=3)

  
ATC ATG TC ATC TG GGAA  # PUSH 2 PUSH 3 MUL PUSH 2 DIV WRITE  
 
 
Known Limitations
 
1. Error Handling: No runtime checks for division by zero or stack overflow

2. Instruction Limits:  PUSH  supports only 0-3 (single-base operands); large numbers require multiplication

3. Biological Mapping: No implementation of DNA double-strand or base-pairing rules

4. Performance: Limited to 256-byte memory and simple stack structure
 
Contribution
 
We welcome contributions!
 
Submit issues for bugs/suggestions

Pull requests to optimize code, expand the instruction set, or add test cases

Contact: ding2011_0114@outlook.com
 
License
 
This project is licensed under the MIT License.
