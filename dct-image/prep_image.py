#!/usr/bin/env python3

import numpy as np
import cv2 as cv

OFFSET = 128
BLOCKSIZE = 8


def make_compliant_dimensions(image):
    '''
    Take an image and change its dimensions so that they are in multiples of 8
    '''
    height, width = image.shape[:2]
    while (height % BLOCKSIZE): height += 1
    while (width % BLOCKSIZE): width += 1

    resized_image = cv.resize(image, (width, height))
    return resized_image


def process_raw_image(image_path):
    '''
    Prepares Image for DCT Transformation
    - Read in image with colour flag
    - Change colour channel to YCbCr
    - Pad image to make it in multiples of 8
    - Change channel datatype from uint8 -> float32
    - Take only y(luminance) channel and minus 128 to each value
    Returns: Tuple separated into Y layer, Cr layer and Cb layer
    '''
    raw_image = cv.imread(image_path, flags=cv.IMREAD_COLOR)    # read in BGR image
    ycrcb_image = cv.cvtColor(raw_image, cv.COLOR_BGR2YCR_CB)   # change it to YCbCr
    padded_image = make_compliant_dimensions(ycrcb_image)       # resize image
    
    float32_image = np.float32(padded_image)                    # change it to float32 for dct
    y_layer, cr_layer, cb_layer = cv.split(float32_image)       # split it to Y Cr Cb layer (Cr and Cb layer will not be touched)
    return (y_layer - OFFSET, cr_layer, cb_layer)               # return all


def prep_image_eight_by_eight(image):
    '''
    Take in a grid with dimensions that are multiples of 8
    Breaks it into 8x8 blocks
    '''
    img_blocks = []
    height, width = image.shape[:2]

    for j in range(0, height, BLOCKSIZE):
        for i in range(0, width, BLOCKSIZE):
            block = image[j:j + BLOCKSIZE, i:i + BLOCKSIZE]
            img_blocks.append(block)

    return img_blocks


def combine_blocks_to_single_image(numcols, image_blocks):
    '''
    Combine 8x8 blocks into a single grid
    '''
    image_rows = []
    single_row = []
    for i in range(len(image_blocks)):
        if i > 0 and not(i % int(numcols / BLOCKSIZE)):
            image_rows.append(single_row)
            single_row = [image_blocks[i]]
        else:
            single_row.append(image_blocks[i])
    image_rows.append(single_row)

    return np.block(image_rows)
