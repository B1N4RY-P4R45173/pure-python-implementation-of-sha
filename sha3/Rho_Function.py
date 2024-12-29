LANE_SIZE=64
def rho(state):
    offsets = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14]
    ]
    for x in range(5):
        for y in range(5):
            state[x][y] = (state[x][y] << offsets[x][y] | state[x][y] >> (LANE_SIZE - offsets[x][y])) % (1 << LANE_SIZE)
    return state
