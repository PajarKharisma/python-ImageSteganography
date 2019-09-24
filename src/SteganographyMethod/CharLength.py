def setCharLength(val):
    char1, char2, char3, char4 = 0, 0, 0, 0
    if val > 255 and val <= (255 * 255):
        char1 = 255
        char3 = 1
        for i in range(1, 255):
            if val < i*255:
                char2 = i - 1
                break
        char4 = val - (char1 * char2)
    elif val > (255 * 255):
        char1 = 255
        char2 = 255
        for i in range(1,255):
            if val < i * (255 * 255):
                char3 = i-1
                break
        char4 = val - (char1 * char2 * char3)
    else:
        char1 = val
        char2 = 1
        char3 = 1
    
    return char1, char2, char3, char4

def getCharLenth(a, b, c, d):
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    return int((a * b * c) + d)