import sha256
import sys

# If no arguments are provided, prompt for a message
if len(sys.argv) == 1:
    message = input("Enter your string to hash: ")
    print(sha256.getHash(message))
    exit(0)

# If a file path is provided as an argument, process the file
try:
    with open(sys.argv[1], 'r') as file:
        for line in file:
            # Strip whitespace/newline before hashing
            print(sha256.getHash(line.strip()))
except FileNotFoundError:
    print(f"Error: File '{sys.argv[1]}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
