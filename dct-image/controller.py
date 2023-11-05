#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import sys
import argparse
import os

from process_file import *
from prep_image import *
from quantization import *
from process_secret import *

MINIMUM_ARGUMENTS = 2
QUALITY = 50

np.set_printoptions(threshold=sys.maxsize)

def create_command_line_parser():
    '''
    Uses the argparse library to create command line processing for time
    '''
    parser = argparse.ArgumentParser(prog='controller.py', usage='%(prog)s cover_image_path [-e filepath] [-r]')

    parser.add_argument('image_path', type=str)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-e', type=str, help='embed <filepath>')
    action.add_argument('-r', help='reveal', action='store_true')

    return parser


def perform_forward_dct(luminance_layer):
    '''
    Given the luminance layer of an image, perform forward DCT II on it
    We return an array of 8x8 blocks
    '''
    luminance_layer_blocks = prep_image_eight_by_eight(luminance_layer)
    dct_blocks = [(cv.dct(luminance_layer_block)) for luminance_layer_block in luminance_layer_blocks]
    quantised_blocks = [np.around(do_quantization(dct_block, QUALITY)) for dct_block in dct_blocks]
    return quantised_blocks


def perform_reverse_dct(ncols, embedded_blocks):
    dequantised_blocks = [do_inverse_quantization(quantised_block, QUALITY) for quantised_block in embedded_blocks]
    idct_blocks_unadjusted = [cv.idct(np.float32(dequantised_block)) for dequantised_block in dequantised_blocks]
    idct_blocks = [idct_block_unadjusted + OFFSET for idct_block_unadjusted in idct_blocks_unadjusted]
    decompressed_y_layer = combine_blocks_to_single_image(ncols, idct_blocks)
    return decompressed_y_layer


def max_bits_for_embedding(blocks_of_eight):
    '''
    Given a series of quantised blocks, find the max number of bits that can be hidden in the LSB
    '''
    max_bits = 0
    for block_of_eight in blocks_of_eight:
       max_bits += np.count_nonzero(block_of_eight[1:, 1:] > 1) + np.count_nonzero(block_of_eight[0, 1:] > 1) + np.count_nonzero(block_of_eight[1:, 0] > 1)

    return max_bits


def do_embed(luminance_layer, secret_file_path):
    '''
    Given a valid file path, read it and turn it into a binary string
    Embed the binary string in the LSB of quantised coefficients that are > 1
    Return the reversed quantised y-layer
    '''
    secret_in_binary = file_to_binstring(secret_file_path)

    quantised_blocks = perform_forward_dct(luminance_layer)

    max_bits = max_bits_for_embedding(quantised_blocks)
    if len(secret_in_binary) > max_bits:
        raise ValueError(f'Image not large enough to hide data. Your file has {len(secret_in_binary)} bits but only a maximum of {max_bits} bits can be encoded.')
    
    index = 0
    embedded_blocks = []
    for quantised_block in quantised_blocks:
        quantised_block, index = embed_message(quantised_block, secret_in_binary, index)
        embedded_blocks.append(quantised_block)
    
    decompressed_y_layer = perform_reverse_dct(luminance_layer.shape[1], embedded_blocks)
    return decompressed_y_layer


def make_stego_image(y_mod_layer, cr_layer, cb_layer, input_path):
    stego_img_ycrcb = cv.merge((y_mod_layer, cr_layer, cb_layer))
    stego_img_int = np.uint8(np.clip(stego_img_ycrcb, 0, THRESHOLD))

    stego_img_bgr = cv.cvtColor(stego_img_int, cv.COLOR_YCR_CB2BGR)
    stego_img_processed = np.uint8(np.clip(stego_img_bgr, 0, THRESHOLD))

    stego_image_path = make_file_path(input_path)
    cv.imwrite(stego_image_path, stego_img_processed)
    print(f'View your stego image at {stego_image_path}')


def do_reveal(luminance_layer):
    quantised_blocks = perform_forward_dct(luminance_layer)

    extracted_file_bits = ''
    for quantised_block in quantised_blocks:
        extracted_file_bits += reveal_message(quantised_block)

    output_path = make_file_path('extracted.dat')
    binstring_to_file(extracted_file_bits, output_path)
    print(f'View the extracted data at {output_path}')


def main():
    parser = create_command_line_parser()
    if len(sys.argv) < MINIMUM_ARGUMENTS:
        print('Usage: ./controller.py cover_image_path [-e filepath] [-r]')
        exit(1)

    cover_image_path = sys.argv[1]
    secret_file_path = None

    if not os.path.exists(cover_image_path):
        print('Invalid cover image path')
        exit(1)
    
    luminance_layer, cr_layer, cb_layer = process_raw_image(cover_image_path)
    args = parser.parse_args()

    if args.e is not None:
        if not os.path.exists(args.e):
            print('Invalid file path')
            exit(1)
        else:
            secret_file_path = args.e
            try:
                decompressed_y_layer = do_embed(luminance_layer, secret_file_path)
                make_stego_image(decompressed_y_layer, cr_layer, cb_layer, cover_image_path)
            except ValueError as e:
                print(e)
    
    if args.r == True:
        do_reveal(luminance_layer)


if __name__ == "__main__":
    main()
