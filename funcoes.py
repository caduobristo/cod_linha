def ami_encode(data):
    last_positive = True
    encoded = ''

    for bit in data:
        if bit == '0':
            encoded += '0'
        elif bit == '1':
            if last_positive:
                encoded += '1'
            else:
                encoded += '-1'
            last_positive = not last_positive
    
    return encoded

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    return binary

def ami_decode(data):
    decode = ''

    for bit in data:
        if bit == '0':
            decode += '0'
        elif bit == '1':
            decode += '1'

    return decode


def binary_to_string(binary):
    string = ''.join(chr(int(binary[byte:byte+8], 2)) for byte in range(0, len(binary), 8))
    return string

