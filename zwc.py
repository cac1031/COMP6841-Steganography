#!/usr/bin/env python3
import re
import random
import math

BLOCK_SIZE = 8
'''
### Encoding ###
Input: Cover Message, Secret Text
Output: Cover Message with Non-Printing Character Embedded
Algo:
1. For each grapheme, encode them separately into utf-8 codepoints. This gives an array
2. Then, for each hex codepoint, we will
    - transform it into an integer
    - make it into a 8 character long binary string
    - concatenate each sequence together

3. Now, we will replace:
    - 0 --> "\u200B"    zero-width space
    - 1 --> "\u200C"    zero-width non-joiner

4. [TODO] Now we have to interlace the zero width characters throughout the cover

### Decoding ###
Input: Cover Message with Non-Printing Character Embedded
Output: Secret Message
Algo:
1. From the cover message, we will delete all characters that are not \u200B or \u200c (see hello2.py)
2. Now, we do the reverse mapping:
    - "\u200B" --> "0"
    - "\u200C" --> "1"
    This gives us a binary string of 0s and 1s

3. Now, we will separate them out into blocks of 8
    E.g. ['11011001', '10000101', '11011011']

4. Now, we will transform each 8-char binary string to an integer
    E.g. [240, 54, 2]

5. Then we use bytearray to transform it into a hex sequence
6. Now we can use .decode('utf-8') to get extract the final message

### Some Potential Improvements ###
• Is there a way to not hard code the specific zero width characters? Maybe can allow for user input
'''

def conceal(cover_message, secret_message):
    hex_codepoints = [s.encode("utf-8") for s in secret_message]
    binary_string = "".join(format(int.from_bytes(f), "08b") for f in hex_codepoints)

    zwc_string = binary_string.replace("0", "\u200b").replace("1", "\u200c")
    stego_string = shuffle_string(cover_message, zwc_string)
    # stego_string = cover_message + zwc_string
    return stego_string


def shuffle_string(text1, text2):
    shuffled = []
    i, j = 0, 0

    len1 = len(text1)
    len2 = len(text2)

    upper_bound = math.ceil(len2 / len1)

    while i < len(text1) and j < len(text2):
        num_characters = random.randint(0, upper_bound)
        shuffled.append(text1[i])
        shuffled.append(text2[j: j + num_characters])
        i += 1
        j += num_characters
    
    while i < len1:
        shuffled.append(text1[i])
        i += 1
    while j < len2:
        shuffled.append(text2[j])
        j += 1
    
    return "".join(shuffled)


def reveal(stego_message):
    zwc_string = re.sub(r'[^\u200b-\u200c]', "", stego_message)
    binary_string = zwc_string.replace("\u200b", "0").replace("\u200c", "1")

    block8_binaries = [binary_string[i: i + BLOCK_SIZE] for i in range(0, len(binary_string), BLOCK_SIZE)]
    block8_integers = [int((block8_binary), 2) for block8_binary in block8_binaries]

    utf8_encoding_bytestream = bytearray(block8_integers)
    return utf8_encoding_bytestream.decode('utf-8')


def main():
    cover_message = input("Please enter your cover message: ")
    secret_message = input("Please enter your secret message: ")
    print()

    concealed_message = conceal(cover_message, secret_message)
    print(f"Your concealed message is: {concealed_message}")
    
    revealed_message = reveal(concealed_message)
    print(f"The revealed message is: {revealed_message}")


if __name__ == "__main__":
    main()
