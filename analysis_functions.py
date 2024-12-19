# This file contains all of the requisite function definitions to perform the analysis in the Jupyter Notebooks.

# All of the S boxes for DES. Most of our analysis pertains to the first S-box only.
from typing import List
from itertools import combinations
import numpy as np
from aes_functions import aes_sub_bytes 

from des_helpers import permute
import random

random.seed = 0

DES_Sboxes:List[List[List[int]]] = [
    [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]
    ],
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
    ],
    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
    ],
    [
        [7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
    ],
    [
        [2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]
    ],
    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]
    ],
    [
        [4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]
    ],
    [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]
    ]
]



# This function computes the confusion coefficients for DES.
def compute_confusion_coefficients(sbox, attack_type='DPA', algorithm='DES'):
    coefficients = []
    # num_keys = 2**6 if algorithm == 'DES' else 2**64
    key_pairs = []# All unique key pairs
    if algorithm == 'DES':
        key_pairs = list(combinations(range(2**6), 2))
    else:
        keys = generate_n_random_strings(2**6)
        key_pairs = list(combinations(keys, 2))

    inputs = range(64) if algorithm == 'DES' else generate_n_random_strings(2**8)
    print("[compute_confusion_coefficients] Setup complete!")
    
    for ki, kj in key_pairs:
        if ki == kj:
            continue
        # Conditional
        selection_function = get_first_bit if attack_type == "DPA" else hamming_weight
        permutation_function = (lambda val: des_sbox_output(val, sbox)) if algorithm == 'DES' else aes_sub_bytes
        
        kappa = compute_kappa(ki, kj, permutation_function, selection_function, inputs)

        coefficients.append(kappa)
        
    return coefficients
    
def hamming_weight(bits):
    return bin(int(bits, 2)).count('1')

def get_first_bit(val:str):
    return int(val[0], 2)

def get_h_bits(val, h):
    return int(val[0:h])


# Compute the Kappa step for a generic function
def compute_kappa(ki, kj, permutation_function, selection_function, inputs):
    diff_squared = []
    for input_val in inputs:
        vi = permutation_function(input_val ^ ki) # V|ki
        vj = permutation_function(input_val ^ kj) # V|kj
        diff = selection_function(vi) - selection_function(vj)
        diff_squared.append(diff**2)

    return np.mean(diff_squared) # This is the expected value

# Given some input and an sbox, computes the output bits
def des_sbox_output(input_bits:int, sbox:List[List[int]]):
    bits = format(input_bits, '06b')
    row = int(bits[0] + bits[5], 2)
    col = int(bits[1:5], 2)
    return format(sbox[row][col], '04b') # outputs a binary string

# The AES Sbox is 16x16
def generate_n_random_strings(n):
    # randomly selects 2^16 strings...
    
    # Randomly select 2^16 unique numbers from the full 64-bit range
    selected_strings = []
    for _ in range(n) :
        selected_bit_string = generate_random_bit_string(64)
        selected_strings.append(int(selected_bit_string, 2))
    
    return selected_strings

def generate_random_bit_string(length):
    return ''.join(random.choice('01') for _ in range(length))
    