import sys

OPCODES = {
    'AA': 0b0000, 'AT': 0b0001, 'AC': 0b0010, 'AG': 0b0011,
    'TA': 0b0100, 'TT': 0b0101, 'TC': 0b0110, 'TG': 0b0111,
    'CA': 0b1000, 'CT': 0b1001, 'CG': 0b1010, 'CC': 0b1011,
    'GA': 0b1100, 'GT': 0b1101, 'GC': 0b1110, 'GG': 0b1111,
}

BASE_TO_NUM = {'A': 0, 'T': 1, 'C': 2, 'G': 3}

def compile_dna(input_file, output_file):
    """Compile DNA source code to binary."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read().upper()
            # Filter valid DNA bases (A/T/C/G)
            sequence = ''.join(c for c in source if c in 'ATCG')
        
        tokens = []
        index = 0
        while index < len(sequence):
            # Extract 2-base opcode
            if index + 2 > len(sequence):
                break
            opcode = sequence[index:index+2]
            index += 2
            
            # Determine operand length based on opcode
            operand_len = 1 if opcode == 'AT' else 2 if opcode in ['CA', 'CT', 'CG', 'GA', 'GT', 'GC', 'GG'] else 0
            operand = sequence[index:index+operand_len] if operand_len > 0 else ''
            index += operand_len
            tokens.append((opcode, operand))
        
        binary_code = bytearray()
        for opcode, operand in tokens:
            if opcode not in OPCODES:
                raise ValueError(f"Invalid opcode: {opcode}")
            
            # Calculate operand value (base-4 to decimal)
            operand_val = sum(BASE_TO_NUM[c] * (4 ** i) for i, c in enumerate(reversed(operand)))
            instruction = (OPCODES[opcode] << 4) | (operand_val & 0b1111)
            binary_code.append(instruction)
        
        with open(output_file, 'wb') as f:
            f.write(binary_code)
        print(f"Compilation successful: {input_file} -> {output_file}")
        return True
    except Exception as e:
        print(f"Compilation error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dna_compiler.py input_file.dna [output_file.bin]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.dna', '.bin')
    
    compile_dna(input_file, output_file)
