#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description='Strips ECC (Error Correction Codes) from PS2 memory card images. Mainly for compatibility with MCP2 VMCs')
    parser.add_argument('f1', type=str, help='PS2 memory card image with ECC enabled')
    parser.add_argument('f2', type=str, help='PS2 memory card image with ECC stripped')

    args = parser.parse_args()

    try:
        with open(args.f1, 'rb') as infile:
            content = infile.read()

        if len(content) != 8650752:
             print(f"Length isn't right ... is {len(content)} bytes, should be 8650752 bytes")

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
                output[o1:o2] = content[c1:c2]

        with open(args.f2, 'wb') as outfile:
            outfile.write(output)

        print(f"ECC stripped output written to {args.f2}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def are_binary_equivalent(f1, f2):
    with open(f1, 'rb') as infile:
            f1_contents = infile.read()

    with open(f2, 'rb') as infile:
            f2_contents = infile.read()

    return f1_contents == f2_contents


if __name__ == "__main__":
    main()