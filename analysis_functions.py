# This file contains all of the requisite function definitions to perform the analysis in the Jupyter Notebooks.

# All of the S boxes for DES. Most of our analysis pertains to the first S-box only.
from typing import List
from itertools import combinations
import numpy as np

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

def compute_confusion_coefficients_DES(sbox, attack_type='DPA'):
    """
    Compute confusion coefficients using Pearson correlation for DPA or CPA.

    Parameters:
    - sbox: The S-box to analyze.
    - attack_type: 'DPA' or 'CPA'.

    Returns:
    - List of confusion coefficients.
    """
    coefficients = []
    cpa_arrays = []
    key_pairs = list(combinations(range(64), 2))  # All unique key pairs
    V = []
    
    for ki, kj in key_pairs:
        if ki == kj:
            continue

        vi_list = []
        vj_list = []
        
        sum_diff_squared = 0
        for input_val in range(64):
            vi = des_sbox_output(format(input_val ^ ki, '06b'), sbox)
            vj = des_sbox_output(format(input_val ^ kj, '06b'), sbox)
            V.append(int(vi))
            V.append(int(vj, 2))
            
            if attack_type == 'DPA':
                # Use the first bit of the S-box output for DPA
                diff = int(vi[0], 2) - int(vj[0], 2)
                sum_diff_squared += diff ** 2
            elif attack_type == 'CPA':
                # Use the Hamming weight of the S-box output for CPA
                vi_list.append(int(vi, 2))
                vj_list.append(int(vj, 2))

        # Convert correlation into confusion coefficient
        kappa = 0
        if attack_type == 'DPA':
            kappa = sum_diff_squared / 64
            coefficients.append(kappa)
        elif attack_type == 'CPA':
            # For the key hypothesis vi and vj
            vi_array = np.array(vi_list)
            vj_array = np.array(vj_list)

            denominator = np.var(V) 
            cpa_arrays.append((vi_array, vj_array))
    if attack_type == 'CPA':
        V_mean = np.mean(V)
        V_var = np.var(V)
        for ki,kj in cpa_arrays:
            kappa = (np.mean((ki - V_mean) * (kj - V_mean)) / V_var) if denominator != 0 else 0
            coefficients.append(kappa)
        
    return coefficients
    

# Given some input and an sbox, computes the output bits
def des_sbox_output(input_bits:str, sbox:List[List[int]]):
    row = int(input_bits[0] + input_bits[5], 2)
    col = int(input_bits[1:5], 2)
    return format(sbox[row][col], '04b') # outputs a binary string
