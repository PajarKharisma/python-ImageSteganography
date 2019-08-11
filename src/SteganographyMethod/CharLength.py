def setCharLength(val):
    char1, char2, char3 = 0, 0, 0
    if val > 255:
        char1 = 255
        for i in range(1, 255):
            if val < i*255:
                char2 = i - 1
                break
        char3 = val - (char1 * char2)
    else:
        char1 = val
        char2 = 1
    
    return char1, char2, char3

def getCharLenth(a,b,c):
    return int((a*b)+c)