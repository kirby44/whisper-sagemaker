import base64

# Assume 'file1.txt' and 'file2.txt' are the files containing your base64 strings.
with open('sandbox/convertedpayload', 'r') as file:
    str1 = file.read()

with open('sandbox/payload', 'r') as file:
    str2 = file.read()

# Decode the base64 strings to bytes
bytes1 = base64.b64decode(str1)
bytes2 = base64.b64decode(str2)

# Compare the byte sequences
# This will print True if they are identical, and False otherwise.
print(bytes1 == bytes2)
