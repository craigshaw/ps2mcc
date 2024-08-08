#!/usr/bin/env python3

import argparse

from ecc import calculate_ecc

TOTAL_PAGES = 16
ECC_PAGE_SIZE = 528
ECC_BLOCK_SIZE = ECC_PAGE_SIZE * TOTAL_PAGES
PAGE_SIZE = 512
BLOCK_SIZE = PAGE_SIZE * TOTAL_PAGES

def main():
    parser = argparse.ArgumentParser(description='Converts PS2 memory card images between those with and without ECCs. Mainly for compatibility with MCP2 VMCs')
    parser.add_argument('input', type=str, help='Path to PS2 memory card image to be converted')
    parser.add_argument('output', type=str, help='Path to converted PS2 memory card image')

    args = parser.parse_args()

    try:
        with open(args.input, 'rb') as infile:
            vmc_raw = infile.read()

        if len(vmc_raw) == 8650752: # Strip ECC
             output = strip_ecc(vmc_raw)
        elif len(vmc_raw) == 8388608: # Add ECC
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
    output = bytearray(8650752)

    for block in range(1024):
        for page in range(16):
            # Each page is 528 bytes. The last 16 bytes are the ECC. 
            # Each block (16 pages) with ECC is 8448 bytes
            o1 = (block*ECC_BLOCK_SIZE)+(page*ECC_PAGE_SIZE)
            o2 = o1 + PAGE_SIZE
            c1 = (block*BLOCK_SIZE)+(page*PAGE_SIZE)
            c2 = c1 + PAGE_SIZE
            block_bytes = vmc_raw[c1:c2] # Copy ECC-less block for reference
            output[o1:o2] = block_bytes

            page_eccs = bytearray(16)

            # Now calculate the ECCs
            for chunk in range(4):
                    page_eccs[chunk*3:(chunk*3)+3] = calculate_ecc(block_bytes[chunk*128:(chunk*128)+128])

            # Bolt the ECCs onto the new page
            output[o2:o2+16] = page_eccs

    return output

def strip_ecc(vmc_raw):
    output = bytearray(8388608) # 8MB

    for block in range(1024):
        for page in range(16):
            # Each page is 528 bytes. The last 16 bytes are the ECC. 
            # Therefore 512 byte page without ECC
            # Each block (16 pages) without ECC is 8192 bytes
            o1 = (block*BLOCK_SIZE)+(page*PAGE_SIZE)
            o2 = o1 + PAGE_SIZE
            c1 = (block*ECC_BLOCK_SIZE)+(page*ECC_PAGE_SIZE)
            c2 = c1 + PAGE_SIZE
            output[o1:o2] = vmc_raw[c1:c2]

    return output

if __name__ == "__main__":
    main()