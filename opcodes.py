names = [
  "LIT",
  "INC",
  "POP",
  "DUP",
  "NIP",
  "SWP",
  "OVR",
  "ROT",

  "EQU",
  "NEQ",
  "GTH",
  "LTH",
  "JMP",
  "JCN",
  "JSR",
  "STH",

  "LDZ",
  "STZ",
  "LDR",
  "STR",
  "LDA",
  "STA",
  "DEI",
  "DEO",

  "ADD",
  "SUB",
  "MUL",
  "DIV",
  "AND",
  "ORA",
  "EOR",
  "SFT",
]

def generate_opcode_offsets(counter_width=7, add_uxntal_offset=True):
    TWO = 1 << counter_width
    K = 2 << counter_width
    uxntal_offset = 0x100 if add_uxntal_offset else 0x000

    offsets = {}
    for opcode_num, opcode in enumerate(names):
        base_offset = opcode_num << (counter_width + 2)
        offsets[opcode] = (base_offset) + uxntal_offset
        offsets[opcode+"k"] = (base_offset | K) + uxntal_offset
        offsets[opcode+"2"] = (base_offset | TWO) + uxntal_offset
        offsets[opcode+"2k"] = (base_offset | TWO | K) + uxntal_offset

    return offsets
