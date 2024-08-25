#!/usr/bin/env python3

import argparse

from ecc import calculate_ecc

# A standard 8MB PS2 memory card has 16384 pages.
# Each page is 528 bytes. The last 16 bytes are the ECC. 
# Therefore 512 byte page without ECC
# Erase blocks are 16 pages long
TOTAL_PAGES = 16384
PAGE_SIZE = 528
PAGE_SIZE_SLIM = PAGE_SIZE - 16 # Without ECC

def main():
    parser = argparse.ArgumentParser(description='Converts PS2 memory card images between those with and without ECCs. Mainly for compatibility with MCP2 VMCs')
    parser.add_argument('input', type=str, help='Path to PS2 memory card image to be converted')
    parser.add_argument('output', type=str, help='Path to converted PS2 memory card image')

    args = parser.parse_args()

    try:
        with open(args.input, 'rb') as infile:
            vmc_raw = infile.read()

        if len(vmc_raw) == TOTAL_PAGES * PAGE_SIZE: # Strip ECC
             output = strip_ecc(vmc_raw)
        elif len(vmc_raw) == TOTAL_PAGES * PAGE_SIZE_SLIM: # Add ECC
             output = add_ecc(vmc_raw)
        else:
             print(f"{args.input} isn't a compatible image format")
             exit(1)

        with open(args.output, 'wb') as outfile:
            outfile.write(output)

        print(f"{args.input} converted and written to {args.output}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def add_ecc(vmc_raw):
    output = bytearray(TOTAL_PAGES*PAGE_SIZE)

    for page in range(TOTAL_PAGES):
        page_bytes = vmc_raw[(page*PAGE_SIZE_SLIM):(page*PAGE_SIZE_SLIM)+PAGE_SIZE_SLIM] # Copy ECC-less block for reference
        o1 = (page*PAGE_SIZE)
        o2 = o1 + PAGE_SIZE_SLIM
        output[o1:o2] = page_bytes

        # Now calculate the ECCs
        page_eccs = bytearray(16)
        for chunk in range(4):
            page_eccs[chunk*3:(chunk*3)+3] = calculate_ecc(page_bytes[chunk*128:(chunk*128)+128])

        # Bolt the ECCs onto the new page
        output[o2:o2+16] = page_eccs

    return output

def strip_ecc(vmc_raw):
    output = bytearray(TOTAL_PAGES*PAGE_SIZE_SLIM)

    for page in range(TOTAL_PAGES):
        output[(page*PAGE_SIZE_SLIM):(page*PAGE_SIZE_SLIM)+PAGE_SIZE_SLIM] = vmc_raw[(page*PAGE_SIZE):(page*PAGE_SIZE)+PAGE_SIZE_SLIM]

    return output

if __name__ == "__main__":
    main()