import sha256
import sys
# If no arguments are provided, prompt for a message
if len(sys.argv) == 1:
    # message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas hendrerit ac risus sit amet maximus. Suspendisse in aliquam libero. Etiam pulvinar orci eros, commodo sollicitudin urna lobortis sit amet. In efficitur dapibus dictum. Proin rhoncus ex at augue pretium finibus. Donec mattis condimentum arcu, nec ultricies sem. Integer non finibus odio. Vivamus ac mauris mauris. Nullam viverra erat et blandit malesuada.Quisque sed libero dolor. Mauris eget metus nisl. Vivamus ultricies leo ut diam placerat, in pharetra ex maximus. Integer libero purus, congue ac venenatis ut, ornare in diam. Maecenas feugiat, metus tristique accumsan tempor, tellus nisi porta massa, vitae ultricies massa sem non orci. Suspendisse potenti. Cras a tellus at risus finibus volutpat ut eu purus. Cras nisi dui, accumsan vel tellus et, mattis venenatis dui. Curabitur rhoncus sem arcu, sed fringilla elit porttitor vitae. Aenean eu est mattis, pulvinar ligula aliquet, cursus odio. Sed bibendum felis condimentum tortor finibus dictum. Cras blandit diam sit amet mattis tincidunt. Vivamus ultrices tristique dolor et tincidunt. Etiam sit amet euismod ligula. Morbi at dui sit amet sem mollis condimentum.Nulla eleifend quis purus at ornare. Nullam at orci eget nisi mattis fringilla eget vel lacus. Phasellus aliquet auctor convallis. Pellentesque maximus lectus at purus semper, a iaculis ipsum euismod. Suspendisse felis mauris, blandit vel sodales ut, porttitor nec nunc. Phasellus sodales velit quis orci consequat pretium. Mauris egestas nec magna sed pellentesque."
    message = input("Enter your string to hash: ")
    # hash,binary_str = sha256.getHash(message)
    # print (f"The binary notation of {message} is {binary_str} and its SHA-256 bit hash is {hash}")
    print(f"The SHA-256 bit hash of {message} is: {sha256.getHash(message)}")
    exit(0)

# If a file path is provided as an argument, process the file
try:
    with open(sys.argv[1], 'r') as file:
        counter = 0
        for line in file:
            counter += 1
            # hash, binary_str = sha256.getHash(line.strip())
            # Strip whitespace/newline before hashing
            print(f"The SHA-256 bit hash at line{counter} is: {sha256.getHash(line.strip())}")
except FileNotFoundError:
    print(f"Error: File '{sys.argv[1]}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
