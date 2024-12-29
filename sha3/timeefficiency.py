import numpy as np
import time
import hashlib

class SHA3_512:
    LANE_SIZE = 64
    STATE_SIZE = 1600
    RATE_SHA3_512 = 576
    CAPACITY = STATE_SIZE - RATE_SHA3_512
    OUTPUT_LENGTH = 512

    def __init__(self, message):
        if isinstance(message, str):
            message = message.encode()
        self.message = message
        self.state = np.zeros((5, 5, self.LANE_SIZE), dtype=np.uint8)

    @staticmethod
    def to_bits(data):
        result = []
        for byte in data:
            for i in range(8):
                result.append((byte >> i) & 1)
        return result

    @staticmethod
    def from_bits(bits):
        bytes_list = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(min(8, len(bits) - i)):
                byte |= bits[i + j] << j
            bytes_list.append(byte)
        return bytes(bytes_list)

    def sha3_padding(self):
        bits = self.to_bits(self.message)
        bits.extend([0, 1, 1, 0])
        bits.extend([0] * (((-len(bits) - 1) % self.RATE_SHA3_512)))
        bits.append(1)
        return bits

    @staticmethod
    def state_to_bytes(state):
        out = []
        for y in range(5):
            for x in range(5):
                lane_bits = []
                for z in range(SHA3_512.LANE_SIZE):
                    lane_bits.append(state[x][y][z])
                out.extend(lane_bits)
        return SHA3_512.from_bits(out[:SHA3_512.OUTPUT_LENGTH])

    @staticmethod
    def theta(Input):
        C = np.zeros((5, SHA3_512.LANE_SIZE), dtype=np.uint8)
        D = np.zeros((5, SHA3_512.LANE_SIZE), dtype=np.uint8)
        for x in range(5):
            for z in range(SHA3_512.LANE_SIZE):
                C[x][z] = Input[x][0][z] ^ Input[x][1][z] ^ Input[x][2][z] ^ Input[x][3][z] ^ Input[x][4][z]
        for x in range(5):
            for z in range(SHA3_512.LANE_SIZE):
                D[x][z] = C[(x - 1) % 5][z] ^ C[(x + 1) % 5][(z - 1) % SHA3_512.LANE_SIZE]
        for x in range(5):
            for y in range(5):
                for z in range(SHA3_512.LANE_SIZE):
                    Input[x][y][z] ^= D[x][z]
        return Input

    @staticmethod
    def rho(state):
        offsets = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
        output = np.zeros_like(state)
        for x in range(5):
            for y in range(5):
                for z in range(SHA3_512.LANE_SIZE):
                    new_z = (z - offsets[x][y]) % SHA3_512.LANE_SIZE
                    output[x][y][z] = state[x][y][new_z]
        return output

    @staticmethod
    def pi(Input):
        output = np.zeros_like(Input)
        for x in range(5):
            for y in range(5):
                for z in range(SHA3_512.LANE_SIZE):
                    new_x = y
                    new_y = (2 * x + 3 * y) % 5
                    output[new_x][new_y][z] = Input[x][y][z]
        return output

    @staticmethod
    def chi(Input):
        output = np.zeros_like(Input)
        for x in range(5):
            for y in range(5):
                for z in range(SHA3_512.LANE_SIZE):
                    output[x][y][z] = Input[x][y][z] ^ ((~Input[(x + 1) % 5][y][z] & Input[(x + 2) % 5][y][z]) & 1)
        return output

    @staticmethod
    def iota(Input, round):
        ROUND_CONSTANTS = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B,
                           0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088,
                           0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
                           0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
                           0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
        RC = ROUND_CONSTANTS[round]
        for z in range(64):
            if (RC >> z) & 1:
                Input[0][0][z] ^= 1
        return Input

    def keccak_f(self, Input):
        for round in range(24):
            Input = self.theta(Input)
            Input = self.rho(Input)
            Input = self.pi(Input)
            Input = self.chi(Input)
            Input = self.iota(Input, round)
        return Input

    def hash(self):
        padded_bits = self.sha3_padding()
        for i in range(0, len(padded_bits), self.RATE_SHA3_512):
            block = padded_bits[i:i + self.RATE_SHA3_512]
            for j in range(len(block)):
                x = (j // self.LANE_SIZE) % 5
                y = (j // (5 * self.LANE_SIZE))
                z = j % self.LANE_SIZE
                if y < 5:
                    self.state[x][y][z] ^= block[j]
            self.state = self.keccak_f(self.state)
        return self.state_to_bytes(self.state).hex()

def measure_time_sha3_512_custom(input_message):
    start = time.time()
    sha3 = SHA3_512(input_message)
    sha3.hash()
    end = time.time()
    return end - start

def measure_time_sha3_512_standard(input_message):
    start = time.time()
    hashlib.sha3_512(input_message).hexdigest()
    end = time.time()
    return end - start

if __name__ == "__main__":
    test_message = b"Sample message for SHA3 testing"
    custom_time = measure_time_sha3_512_custom(test_message)
    standard_time = measure_time_sha3_512_standard(test_message)
    print(f"Custom SHA3-512 Time: {custom_time:.6f} seconds")
    print(f"Standard SHA3-512 Time: {standard_time:.6f} seconds")
