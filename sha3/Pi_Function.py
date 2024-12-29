def pi_step(state):
    new_state = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            new_state[y][(2 * x + 3 * y) % 5] = state[x][y]
    return new_state
