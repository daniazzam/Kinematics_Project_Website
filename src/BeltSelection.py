import math


def selectbelt(hp,w1):
    if (w1/(2*math.pi))/hp > 40 or (w1/(2*math.pi))>=3225 :
        if hp<=100:
            v2 = 3
    elif 4 < (w1/(2*math.pi))/hp < 40 :
        if hp <= 400:
            v2 = 5
    elif 0.3<(w1/(2*math.pi))/hp<4 :
        if hp<=1000:
            v2 = 8
    return v2

def approximateRPM(d1 , w1 , SPD , v):
    VR = w1 / w2

    d2 = VR * d1

    for x in SPD[v]:
        if (x - d2)>=0:
            d2 = x
            break
        if x==SPD[v][-1]:
            d2 = x

    w2 = w1*d1/d2
    return w2

def AvailableDiameter(d , SPD , v):
    for x in SPD[v]:
        if (x - d)>=0:
         d = x
        break
        if x==SPD[v][-1]:
            d = x
    return d
def checkAvailable(d , SPD , v):
    check = False
    for x in SPD[v]:
        if x == d:
            check = True
    if check == False:
        return 'Not Available'
    if check == True:
        return 'Available'
        
def getSecondDiameter(d1 , w1 , w2 , SPD , v ):
    VR = w1 / w2

    d2 = VR * d1

    for x in SPD[v]:
        if (x - d2)>=0:
            d2 = x
            break
        if x==SPD[v][-1]:
            d2 = x
    return d2
def AvailableLength(L ,VBL , v):
    for x in VBL[v]:
        if (x - L)>0:
            L = x
            break
        if x==VBL[v][-1]:
            L = x
    return L
def BFormula(L, d1, d2):
    return 4*L - (2*math.pi*(d2+d1))
def CFormula(B, d1, d2):
    return (B + math.sqrt(B**2 - 32*(d2-d1)**2))/16