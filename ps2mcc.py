#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description='Converts PS2 memory card images between those with and without ECCs. Mainly for compatibility with MCP2 VMCs')
    parser.add_argument('input', type=str, help='Path to PS2 memory card image to be converted')
    parser.add_argument('output', type=str, help='Path to converted PS2 memory card image')

    args = parser.parse_args()

    try:
        with open(args.input, 'rb') as infile:
            vm_raw = infile.read()

        if len(vm_raw) == 8650752: # Strip ECC
             output = strip_ecc(vm_raw)
        elif len(vm_raw) == 8388608: # Add ECC
             pass
        else:
             print(f"{args.input} isn't a compatible image format")

        with open(args.output, 'wb') as outfile:
            outfile.write(output)

        print(f"{args.input} converted and written to {args.output}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def strip_ecc(vm_raw):
    output = bytearray(8388608) # 8MB

    total_pages = 16
    ecc_page_size = 528
    ecc_block_size = ecc_page_size * total_pages
    page_size = 512
    block_size = page_size * total_pages

    for block in range(1024):
        for page in range(16):
            # Each page is 528 bytes. The last 16 bytes are the ECC. 
            # Therefore 512 byte page without ECC
            # Each block (16 pages) without ECC is 8192 bytes
            o1 = (block*block_size)+(page*page_size)
            o2 = o1 + page_size
            c1 = (block*ecc_block_size)+(page*ecc_page_size)
            c2 = c1 + page_size
            output[o1:o2] = vm_raw[c1:c2]

    return output

def are_binary_equivalent(f1, f2):
    with open(f1, 'rb') as infile:
            f1_contents = infile.read()

    with open(f2, 'rb') as infile:
            f2_contents = infile.read()

    return f1_contents == f2_contents


if __name__ == "__main__":
    main()