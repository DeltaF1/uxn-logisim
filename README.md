# Uxn-Logisim

Implements the Uxn instruction set in digital hardware. 

![An animation showing different Uxn mode bits lighting up as stack control signals flow through logic gates](splash.gif)

## Contents

* cpu.circ - The Logisim file
* microcode.mc - Microcode source file
* microcode-asm.py - Microcode assembler
* opcodes.py - Definitions for where opcodes live in the microcode ROM

## Quickstart

1. Open `cpu.circ` in Logisim
2. ( Optional ) Build the latest microcode
	i. To assemble the microcode rom file run
	```sh
	python microcode-asm.py microcode.mc microcode.tal
	uxnasm microcode.tal microcode.rom
	```
	ii. Right click on the ROM labelled `Microcode_ROM`

	iii. Load Image > Select microcode.rom > Select binary (big-endian)
3. Load the
	i. Right click on the 64K RAM module
	ii. Load Image > Select a UXN rom > Select binary (big-endian)

## Microcode Format

**TODO**

## Microcode Assembler

The microcode assembler is only a partial assembler and relies upon Uxntal assembly for the conversion to binary. It takes in a [format](Microcode Format) similar to tal, and outputs a valid .tal file (Including comments!). Requires uxnasm or asma.tal to assemble into the microcode rom.
