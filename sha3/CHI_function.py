def chi(input):
    """Chi step mapping"""
    output = np.zeros_like(input)
    for x in range(5):
        for y in range(5):
            for z in range(LANE_SIZE):
                output[x][y][z] = input[x][y][z] ^ ((~input[(x+1)%5][y][z] & input[(x+2)%5][y][z]) & 1)
    
    return output
