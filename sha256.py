def translate(message): # returns a binary array
    bit_list = []
    for char in message:
        # Convert character to its ASCII value, then to 8-bit binary, and split into bits
        binary_representation = format(ord(char), '08b')  # Get binary string (e.g., '01000001' for 'A')
        bit_list.extend(int(bit) for bit in binary_representation)  # Add each bit as an integer to the list
    return bit_list


def join_binary_array(binary_arr): # returns a binary string from a binary array
    binary_str = ""
    for i in range(len(binary_arr)):
        binary_str += str(binary_arr[i])
    return binary_str


def binary_pretty_print(binary_arr, gap = 8): # return a binary string with spacing
    pretty_str = ""
    for i in range(len(binary_arr)):
        if i > 0 and i % gap == 0:
            pretty_str = pretty_str + " " + str(binary_arr[i])  
        else:
            pretty_str = pretty_str + str(binary_arr[i])
    return pretty_str


def add_paading(binary_str): # returns the padded binary string
    new_str = binary_str + '1' # this adds 1 to the binary string provided
    while (len(new_str) % 512) != 448: # this loops appends 0's to the new string as long as the length is not equal to 448 modulo 512
        new_str = new_str + '0'
    input_length = len(binary_str)
    input_length_binary = format(input_length, '064b') # this converts the input length to its binary form in 64 bits
    new_str = new_str + input_length_binary # this appends the input length to the new string making it a perfect modulo of 512
    return new_str


def get_bitwise_xor(binary_str1,binary_str2,binary_str3 = '0',binary_str4 = '0',binary_str5 = '0'): # takes in upto 5 binary strings and returns the xor of all of them as a binary string
    result = int(binary_str1,2) ^ int(binary_str2,2) ^ int(binary_str3,2) ^ int(binary_str4,2) ^ int(binary_str5,2)
    result = format(result, '032b')
    return result

def binary_to_hex(binary_str):
    # Convert binary string to an integer and then to a hexadecimal string
    return format(int(binary_str, 2), 'x')


def mod_add(*args): # For as many args given find their sum in modulo pow(2,32) and return it as a binary string
    total = 0
    for arg in args:
        # Convert binary string to int if needed
        if isinstance(arg, str):
            # print ("y")
            total = (total + int(arg, 2)) % (2**32)
        else:
            total = (total + arg) % (2**32)
    return format(total, '032b')

def sigma0(binary_str):  # takes in a 32 bit binary string and return 32bit output binary str
    rotatedby7 = binary_str[-7:] + binary_str[:-7]
    rotatedby18 = binary_str[-18:] + binary_str[:-18]
    shiftedby3 = '0' * 3 + binary_str[:-3]
    
    result = get_bitwise_xor(rotatedby7, rotatedby18, shiftedby3) # get xor of these 3 strings
    return result


def sigma1(binary_str):  # takes in a 32 bit binary string and return 32bit output binary str
    rotatedby17 = binary_str[-17:] + binary_str[:-17]
    rotatedby19 = binary_str[-19:] + binary_str[:-19]
    shiftedby10 = '0' * 10 + binary_str[:-10]
    
    result = get_bitwise_xor(rotatedby17, rotatedby19, shiftedby10) # get xor of these 3 strings
    return result


def get_all_W (binary_str): # Takes in a binary string of 512 bits(padded input) and returns all W as a list
    w_list = []
    for t in range(64):
        if t < 16:
            start_index = t * 32
            end_index = start_index + 32
            val = binary_str[start_index:end_index]  # Slice 32 characters
            w_list.append(val)
        else:
            val = mod_add(sigma1(w_list[t-2]),w_list[t-7],sigma0(w_list[t-15]),w_list[t-16]) # For the next values we need to get previous values from the formula σ1(t-2) ,t-7 ,σ0(t-15) ,t-16 and then we xor all of it
            # print (len(res))
            w_list.append(val)
            # print (w_list)
            # break
    # print (w_list)
    return w_list


def csigma0(binary_str): # Takes in binary string and return binary string 
    rotatedby2 = binary_str[-2:] + binary_str[:-2]
    rotatedby13 = binary_str[-13:] + binary_str[:-13]
    rotatedby22 = binary_str[-22:] + binary_str[:-22]
    result = get_bitwise_xor(rotatedby2,rotatedby13,rotatedby22)
    return result

def csigma1(binary_str): # Takes in binary string and return binary string 
    rotatedby6 = binary_str[-6:] + binary_str[:-6]
    rotatedby11 = binary_str[-11:] + binary_str[:-11]
    rotatedby25 = binary_str[-25:] + binary_str[:-25]
    result = get_bitwise_xor(rotatedby6,rotatedby11,rotatedby25)
    return result

def ch(binary_str1,binary_str2,binary_str3): # Takes in binary string and return binary string 
    result = ""
    for i in range(32):
        if binary_str1[i] == '0':
            result = result + binary_str3[i]
        else:
            result = result + binary_str2[i]
    return result

def maj(binary_str1,binary_str2,binary_str3):
    x = int(binary_str1, 2)
    y = int(binary_str2, 2)
    z = int(binary_str3, 2)
    result = (x & y) ^ (x & z) ^ (y & z)
    return bin(result)[2:].zfill(32)

def main_compression(w_list, H):
    # Convert current H values to binary
    a = bin(int(H[0], 16))[2:].zfill(32)
    b = bin(int(H[1], 16))[2:].zfill(32)
    c = bin(int(H[2], 16))[2:].zfill(32)
    d = bin(int(H[3], 16))[2:].zfill(32)
    e = bin(int(H[4], 16))[2:].zfill(32)
    f = bin(int(H[5], 16))[2:].zfill(32)
    g = bin(int(H[6], 16))[2:].zfill(32)
    h = bin(int(H[7], 16))[2:].zfill(32)

    k = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4', '0xab1c5ed5', 
         '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe', '0x9bdc06a7', '0xc19bf174', 
         '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f', '0x4a7484aa', '0x5cb0a9dc', '0x76f988da', 
         '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7', '0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', 
         '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc', '0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', 
         '0xa2bfe8a1', '0xa81a664b', '0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', 
         '0x19a4c116', '0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3',
         '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7', '0xc67178f2']
    
    for i in range(len(k)):
        k[i] = bin(int(k[i], 16))[2:].zfill(32) # Convert K values to binary

    # Main compression loop
    for i in range(64):
        t1 = mod_add(h, csigma1(e), ch(e, f, g), k[i], w_list[i])
        t2 = mod_add(csigma0(a), maj(a, b, c))
        
        h = g
        g = f
        f = e
        e = mod_add(d, t1)
        d = c
        c = b
        b = a
        a = mod_add(t1, t2)
    
    # Calculate new hash values
    new_H = [
        mod_add(a, bin(int(H[0], 16))[2:].zfill(32)),
        mod_add(b, bin(int(H[1], 16))[2:].zfill(32)),
        mod_add(c, bin(int(H[2], 16))[2:].zfill(32)),
        mod_add(d, bin(int(H[3], 16))[2:].zfill(32)),
        mod_add(e, bin(int(H[4], 16))[2:].zfill(32)),
        mod_add(f, bin(int(H[5], 16))[2:].zfill(32)),
        mod_add(g, bin(int(H[6], 16))[2:].zfill(32)),
        mod_add(h, bin(int(H[7], 16))[2:].zfill(32))
    ]
    
    return new_H

def getHash(message):
    # Convert message to binary
    binary_arr = translate(message)
    binary_str = join_binary_array(binary_arr)
    
    # Pad the binary string
    padded_str = add_paading(binary_str)
    
    # Get number of 512-bit blocks
    num_blocks = len(padded_str) // 512 # padded string is a multiple of 512 so we will have no remainder
    
    # Initialize hash values
    H = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a', 
         '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']
    
    # iterate to get 512-bit blocks
    for block in range(num_blocks):
        start = block * 512
        end = start + 512
        current_block = padded_str[start:end] # each block is divided into 512 bits
        
        # Get message schedule (W) for this block
        w_list = get_all_W(current_block)
        
        # Get new hash values after processing this block
        new_H = main_compression(w_list, H)
        
        # Convert binary hash values to hex for next iteration
        for i in range(8):
            H[i] = hex(int(new_H[i], 2))
    
    # Format final hash value
    final_hash = ''
    for h in H:
        final_hash += format(int(h, 16), '08x')
    
    return final_hash
