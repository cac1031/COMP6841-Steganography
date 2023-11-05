#!/usr/bin/env python3
import numpy as np

BLOCKSIZE = 8

def embed_message(y_block, binary_message, index):
    '''
    Take in a single 8 by 8 block and
    embeds a bit of a secret message per LSB of quantised block
    '''
    y_block = (np.rint(y_block)).astype(int)

    for j in range(BLOCKSIZE):
        for i in range(BLOCKSIZE):
            if index >= len(binary_message):
                return y_block, index
            
            else:
                if y_block[j][i] > 1 and not(i == 0 and j == 0):
                    y_block[j][i] = y_block[j][i] >> 0x01 << 0x01
                    message_bit = int(binary_message[index])
                    y_block[j][i] = y_block[j][i] | message_bit
                    index += 1

    return y_block, index


def reveal_message(y_block):
    '''
    Take in a single 8 by 8 block and
    extracts a bit of the embedded secret message per LSB of quantised block
    '''
    y_block = (np.rint(y_block)).astype(int)
    bits_in_block = ''

    for j in range(BLOCKSIZE):
        for i in range(BLOCKSIZE):
            if y_block[j][i] > 1 and not(i == 0 and j == 0):
                bits_in_block += str(y_block[j][i] & 0x01)
    return bits_in_block
