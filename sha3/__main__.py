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
