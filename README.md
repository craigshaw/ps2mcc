# ps2mcc

ps2mcc is a command line tool that converts PS2 memory card images between versions with and without Error Correction Codes (ECCs). I created this to help convert memory card images created by 8BitMods MemCard PRO2 for use with PCSX2 and vice versa. I'm using it as part of a bigger workflow for keeping saves in sync between my PS2 and instances of PCSX2.

### Notes
If the input file is a standard PS2 memory card image with ECCs, the output will be a version of the file with ECCs stripped.

If the input file is an ECC-less virtual memory card image (like those used by the MemCardPro2, for example), the output will be converted to a standard PS2 memory card image with generated ECCs added.

### Usage Instructions
```
usage: ps2mcc.py [-h] input output

Converts PS2 memory card images between those with and without ECCs. Mainly for compatibility with MCP2 VMCs

positional arguments:
  input       Path to PS2 memory card image to be converted
  output      Path to converted PS2 memory card image

options:
  -h, --help  show this help message and exit
```

### Examples
Convert the virtual memory card image from a MemCard PRO 2 to a PCSX2 compatible format
```
$ python3 SLUS-21274-1.mc2 Mcd001.ps2
```
This command takes the input file `SLUS-21274-1.mc2`, adds ECCs to it, and generates a new memory card image named `Mcd001.ps2` that is compatible with PCSX2
***

Convert the virtual memory card image from PCSX2 to a MemCard PRO 2 compatible format
```
$ python3 Mcd001.ps2 MemoryCard1-1.mc2
```
This command takes the input file `Mcd001.ps2`, strips ECCs from it, and generates a new memory card image named `MemoryCard1-1.mc2` that is compatible with MemCard PRO 2

