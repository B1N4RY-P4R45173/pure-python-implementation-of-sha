import numpy as np

LANE_SIZE = 64
STATE_SIZE = 1600
RATE_SHA3_512 = 576  # r = 1600 - 2×512
CAPACITY = STATE_SIZE - RATE_SHA3_512
OUTPUT_LENGTH = 512

def to_bits(data):
    """Convert bytes to bits with correct ordering"""
    result = []
    for byte in data:
        for i in range(8):
            result.append((byte >> i) & 1)
    return result

def from_bits(bits):
    """Convert bits to bytes with correct ordering"""
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(min(8, len(bits) - i)):
            byte |= bits[i + j] << j
        bytes_list.append(byte)
    return bytes(bytes_list)

def sha3_padding(input_data):
    """SHA3 padding: append domain separation bits and 10*1"""
    bits = to_bits(input_data)
    bits.extend([0, 1, 1, 0])
    bits.extend([0] * (((-len(bits) - 1) % RATE_SHA3_512)))
    bits.append(1)
    return bits

def state_to_bytes(input):
    """Convert state array to bytes in correct order"""
    out = []
    for y in range(5):
        for x in range(5):
            lane_bits = []
            for z in range(LANE_SIZE):
                lane_bits.append(input[x][y][z])
            out.extend(lane_bits)
    return from_bits(out[:OUTPUT_LENGTH])

def theta(input):
    """Theta step mapping"""
    C = np.zeros((5, LANE_SIZE), dtype=np.uint8)
    D = np.zeros((5, LANE_SIZE), dtype=np.uint8)
    
    # Compute C[x,z]
    for x in range(5):
        for z in range(LANE_SIZE):
            C[x][z] = input[x][0][z] ^ input[x][1][z] ^ input[x][2][z] ^ input[x][3][z] ^ input[x][4][z]
    
    # Compute D[x,z]
    for x in range(5):
        for z in range(LANE_SIZE):
            D[x][z] = C[(x-1)%5][z] ^ C[(x+1)%5][(z-1)%LANE_SIZE]
    
    # Apply D to state
    for x in range(5):
        for y in range(5):
            for z in range(LANE_SIZE):
                input[x][y][z] ^= D[x][z]
    
    return input

def rho(state):
    """Rho step mapping"""
    offsets = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14]
    ]
    
    output = np.zeros_like(state)
    for x in range(5):
        for y in range(5):
            for z in range(LANE_SIZE):
                new_z = (z - offsets[x][y]) % LANE_SIZE
                output[x][y][z] = state[x][y][new_z]
    
    return output

def pi(input):
    """Pi step mapping"""
    output = np.zeros_like(input)
    for x in range(5):
        for y in range(5):
            for z in range(LANE_SIZE):
                new_x = y
                new_y = (2*x + 3*y) % 5
                output[new_x][new_y][z] = input[x][y][z]
    
    return output

def chi(input):
    """Chi step mapping"""
    output = np.zeros_like(input)
    for x in range(5):
        for y in range(5):
            for z in range(LANE_SIZE):
                output[x][y][z] = input[x][y][z] ^ ((~input[(x+1)%5][y][z] & input[(x+2)%5][y][z]) & 1)
    
    return output


def iota(input, round):
    """Iota step mapping with precomputed constants."""
    
    ROUND_CONSTANTS = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
        0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]

    RC = ROUND_CONSTANTS[round]

    for z in range(64):  
        if (RC >> z) & 1:  
            input[0][0][z] ^= 1
    
    return input


def keccak_f(input):
    """Keccak-f[1600] permutation"""
    for round in range(24):
        input = theta(input)
        input = rho(input)
        input = pi(input)
        input = chi(input)
        input = iota(input, round)
    return input

def sha3_512(message):
    """SHA3-512 hash function"""
    if isinstance(message, str):
        message = message.encode()
    input = np.zeros((5, 5, LANE_SIZE), dtype=np.uint8)
    padded_bits = sha3_padding(message)

    for i in range(0, len(padded_bits), RATE_SHA3_512):
        block = padded_bits[i:i + RATE_SHA3_512]
        for j in range(len(block)):
            x = (j // LANE_SIZE) % 5
            y = (j // (5 * LANE_SIZE))
            z = j % LANE_SIZE
            if y < 5: 
                input[x][y][z] ^= block[j]
        
        input = keccak_f(input)
    return state_to_bytes(input).hex()


s = input("Enter a string: ")
out = sha3_512(s)
print(out)
