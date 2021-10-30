"""
8-bit data bus
16-bit ram addresses
16-bit ALU with 2 16-bit registers
Microcode table is looked up on depending on opcode and keep/short bits. The return bit is used to toggle which stack is being operated on

16-bit IP register
16-bit ram address register


"""
import re, math
import argparse

import opcodes

def bit(n):
    return 1 << n

flags = {}

# The first 3 bits are for ALU commands

flags["ALU_ADD"]   = 0
flags["ALU_SUB"]   = 1
flags["ALU_MUL"]   = 2
flags["ALU_DIV"]   = 3
flags["ALU_AND"]   = 4
flags["ALU_OR"]    = 5
flags["ALU_XOR"]   = 6
flags["ALU_SHIFT"] = 7

stack_offset = 3

# The next 2 bits are for moving the stack pointer

flags["STACK=0"]  = 0 << stack_offset
flags["STACK=1"]  = 1 << stack_offset
flags["STACK=-1"] = 0b11 << stack_offset

bus_outputs = (
    "STACK_OUT",
    "RAM_OUT",
    "PC_OUT",
    "ALU_OUT",
    "ALU_A_OUT",
    "ALU_B_OUT",
    "CONST_0_OUT",
    "CONST_1_OUT",
    "CONST_7_OUT",
)

bus_outputs_offset = stack_offset + 2 + 1 # 1 bit for output enable

# only enable bus outputs when the  
flags["ENABLE_OUTPUT"] = bit(stack_offset + 2)

for i, token in enumerate(bus_outputs):
    flags[token] = (i << bus_outputs_offset) | flags["ENABLE_OUTPUT"]

one_bit_flags_offset = bus_outputs_offset + math.ceil(math.log(len(bus_outputs), 2)) + 1

tokens = [
"STACK_IN",
"STACK_SWAP",

"RAM_IN",

"RAM_ADDR_IN",
"RAM_ADDR_HIGH",

"OPCODE_IN",

"PC_IN",
"PC_INC",
"PC_HIGH",

"ALU_A_IN",
"ALU_B_IN",
"ALU_LATCH",
"ALU_HIGH",

"MICROCODE_RESET",
"RESET_IF_CARRY",
"RESET_IF_ZERO",
"DONE_FETCH",
]

for i, token in enumerate(tokens):
    flags[token] = bit(i + one_bit_flags_offset)

# Low byte is the default state so these tokens exist only for
# clarity in the microcode assembly
nops = [
"RAM_ADDR_LOW",
"PC_LOW",
"ALU_LOW",
]

for token in nops:
    flags[token] = 0

aliases = {
    "MICROCODE_RESET": ("DONE", "END", "RESET", "NEXT"),
    "CONST_1_OUT": ("ONE",),
    "CONST_0_OUT": ("ZERO",),
}

for token in aliases:
    for alias in aliases[token]:
        flags[alias] = flags[token]


print("Using {:d} bits".format(len(tokens)+one_bit_flags_offset))

exclusive = [
        set(bus_outputs), # Don't allow two things to write to the data bus
        set(("RAM_ADDR_HIGH", "RAM_ADDR_LOW")),
        set(("PC_HIGH", "PC_LOW")),
        set(("ALU_HIGH", "ALU_LOW")),
        set(("ALU_ADD", "ALU_SUB", "ALU_MUL", "ALU_DIV", "ALU_AND", "ALU_OR", "ALU_XOR", "ALU_SHIFT")),
]

opcode_offsets = opcodes.generate_opcode_offsets()
opcode_offsets["BRK"] = opcode_offsets["LIT"]

pat = r"[_\-=0-9A-Z]+"
def assemble_microcode(line):
    output = 0
    tokens = set(re.findall(pat, line))
    for group in exclusive:
        conflicting = tokens.intersection(group)

        if len(conflicting) > 1:
            raise Exception(', '.join(conflicting)+" conflicts @"+line)

    for token in tokens:
        output = output | flags[token]

    return output

def strip_newlines(match):
    return match.group(0).replace("\n", " ")

def parse_lines(lines):
    for line in lines:
        if line[0] == "|":
            name = line.split(" ")[0][1:].strip()
            yield "|" + hex(opcode_offsets[name])[2:] + " ( " + name + " )"
        elif line[0] in ("%", ":", "}"):
            yield line
        else:
             
            comments = ""
            for comment in re.findall("\((.*?)\)", line):
                comments+=(" ( "+comment.strip()+" )")

            line = re.sub("\(.*?\)", "", line)

            tokens = set(re.findall(pat, line))
            if len(tokens) > 0: 
                raw = assemble_microcode(line)
                hexed = f"{raw:08x}" 

                # https://stackoverflow.com/a/9475354
                formatted = " ".join([hexed[i:i+2] for i in range(0, len(hexed), 2)])
            else:
                formatted = ""
            yield formatted + comments

def parse_file(file):
    new = ""
    for line in parse_lines(file):
        new += line + "\n"

    # Collapse macros onto one line for uxnasm
    return re.sub('{(.*?)}', strip_newlines, new, flags=re.DOTALL)

def interactive():
    while True:
        microcode = parse_line(input(">"))
        print(f"0x{microcode:08x} - {microcode:032b}")

parser = argparse.ArgumentParser(description="Assemble the microcode")

parser.add_argument("infile", type=argparse.FileType('r'))
parser.add_argument("outfile", type=argparse.FileType('w'))

args = parser.parse_args()

args.outfile.write(parse_file(args.infile.readlines()))
