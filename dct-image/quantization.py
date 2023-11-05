#!/usr/bin/env python3

import numpy as np

THRESHOLD = 255
STANDARD = 50
BLOCKSIZE = 8

def calculate_quant_matrix(quality):
    '''
    Returns a quantization matrix based on given quality [0-100]
    '''
    standard_quant = np.array(
        [[16,  11,  10,  16,  24,  40,  51,  61],
        [12,  12,  14,  19,  26,  58,  60,  55],
        [14,  13,  16,  24,  40,  57,  69,  56],
        [14,  17,  22,  29,  51,  87,  80,  62],
        [18,  22,  37,  56,  68,  109, 103, 77],
        [24,  35,  55,  64,  81,  104, 113, 92],
        [49,  64,  78,  87,  103, 121, 120, 101],
        [72,  92,  95,  98,  112, 100, 103, 99]])
    
    if quality > STANDARD:
        scale = (100 - quality) / STANDARD
        standard_quant = np.round(standard_quant * scale)
    elif quality < STANDARD:
        standard_quant = standard_quant * STANDARD / quality
    return np.where(standard_quant > THRESHOLD, THRESHOLD, standard_quant)


def do_quantization(matrix, quality):
    '''
    Returns an 8x8 matrix of quantised coefficients
    '''
    quant_matrix = calculate_quant_matrix(quality)

    for i in range(BLOCKSIZE):
        for j in range(BLOCKSIZE):
            matrix[i][j] = np.divide(matrix[i][j], quant_matrix[i][j])
    return matrix


def do_inverse_quantization(matrix, quality):
    '''
    Returns an 8x8 matrix of inverse quantised coefficients
    '''
    quant_matrix = calculate_quant_matrix(quality)

    for i in range(BLOCKSIZE):
        for j in range(BLOCKSIZE):
            matrix[i][j] *= quant_matrix[i][j]
    return matrix
