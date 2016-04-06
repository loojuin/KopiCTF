import sys

'''
#### PixelPrison ####
Free the flag from the pixels!

Brought to you by Team 0xDEADBEEF:
1000457 James Wiryo
1000493 Hiang Cheong Kai
1000546 Loo Juin
1000600 Koh En Yan
'''

def formatting(inpFile):
    mat = []
    for line in f.readlines():
        if '<tr>' in line:
            row = []
        elif '</tr>' in line:
            mat.append(row)
        elif '</td>' in line:
            if '#000000' in line:
                row.append(0)
            elif '#FFFFFF' in line:
                row.append(1)
    return mat

def invertAlt(inpArray):
    for ind in xrange(1,len(inpArray),2):
        inpArray[ind] ^= 1

def decode(inpFile):
    mat = formatting(inpFile)
    array = [element for row in mat for element in row]
    invertAlt(array)
    length = int("".join(str(bit) for bit in array[-8:]),2)
    array = array[:8*length]
    decodedString = ''
    
    for charIndex in xrange(length):
        char = array[charIndex::length]
        char = int("".join(str(bit) for bit in char[::-1]),2)
        decodedString += chr(char)
        
    return decodedString

if __name__ == "__main__":
    if len(sys.argv) != 2:
    	print 'Usage: $ python encode.py "[html file]"'
    	exit()
    inp = sys.argv[1]
    with open(inp,'r') as f:
        print decode(f)