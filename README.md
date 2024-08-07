# ps2mcc

PS2 memory card convertor. Converts memory card images between versions with and without ECCs (Error Correction Codes). Mainly for compatibility with MCP2 VMCs

Usage:
```
ps2mcc.py <path to file to convert> <path to converted file>
```

Examples:
```
ps2mcc.py Mcd001.ps2 vmc.mc2

ps2mcc.py SLUS-21274-1.mc2 Mcd001.ps2
````

If the input file is a standard PS2 memory card image with ECCs, the output will be a version of the file with ECCs stripped.

If the input file is an ECC-less virtual memory card image (like those used by the MemCardPro2, for example), the output will be converted to a standard PS2 memory card image with generated ECCs added.