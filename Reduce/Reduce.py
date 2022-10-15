
from ctypes.wintypes import _COORD
import math
N1 = 0

def dft(coord, isForward = True):
    global N1
    N1 = 0
    origCoord = [[]]
    origCoord.append([])
    divider = len(coord[0])
    numSign = -1
    insCount = 0
    if isForward == False:
        divider = 1
        numSign = 1
    for k in range(len(coord[0])):

        re = 0.0
        im = 0.0
        for n in range(len(coord[0])):
            N1+=5
            x = coord[0][n]
            y = coord[1][n]
            arg = 2*math.pi*k*n/len(coord[0])
            reCos = math.cos(arg)
            imSin = math.sin(arg)
            re += (x*reCos-y*imSin)
            im += (x*imSin + y*reCos)*numSign
        origCoord[0].append(re/divider)
        origCoord[1].append(im/divider)
    return origCoord

def reduce(arrA, arrB):
    answ = []

    for i in range(len(arrA)):
        answ.append(0)
        print(i, ":")
        for j in range (i+1):
            print(arrA[j], " ",arrB[i-j])
            answ[i]+=arrA[j]*arrB[i-j]
        print()

    for i in range(1, len(arrA)):
        answ.append(0)
        print(len(arrA)+i-1, ":")
        for j in range (i, len(arrA)):
            print(arrA[j], " ",arrB[len(arrB)-j+i-1])
            answ[len(answ)-1]+=arrA[j]*arrB[len(arrB)-j+i-1]
        print()

    return answ

def coordMult(arrA, arrB):
    answ = [[],[]]
    for i in range(len(arrA[0])):
        answ[0].append(arrA[0][i]*arrB[0][i] - arrA[1][i]*arrB[1][i])
        answ[1].append(arrA[0][i]*arrB[1][i] + arrB[0][i]*arrA[1][i])
    return answ

def reduceDft(arrA, arrB):
    arrSize = len(arrA)
   
    arrAforDft = []
    arrAforDft.append(arrA)
    arrAforDft.append([0]*(2*arrSize-1))
    arrBforDft = []
    arrBforDft.append(arrB)
    arrBforDft.append([0]*(2*arrSize-1))
    for i in range(arrSize - 1):
        arrAforDft[0].append(0)
        arrAforDft[0][i]*=2*arrSize-1
        arrBforDft[0].append(0)
    return dft(coordMult(dft(arrAforDft), dft(arrBforDft)),False)

def LevelLenOfArr(arrA, arrB):
    arrSizeDiff = abs(len(arrA)-len(arrB))
    if(len(arrA)>len(arrB)):
            for i in range(arrSizeDiff):
                arrB.append(0)
    else :
        if(len(arrB)>len(arrA)):
            for i in range(arrSizeDiff):
                arrA.append(0)
    return arrSizeDiff

################################################################

print("Standart:")
arrA = [1,2,3,4]
arrB = [1,2,3,4,5,6,7,8,9]
arrSizeDiff = LevelLenOfArr(arrA, arrB)
answ = reduce(arrA, arrB)
for i in range(arrSizeDiff):
        answ.pop()
for i in answ:
    print(round(i, 5), " ",end="")

print("\n\nWith dft:")
arrA = [1,2,3,4]
arrB = [1,2,3,4,5,6,7,8,9]
arrSizeDiff = LevelLenOfArr(arrA, arrB)
answ = reduceDft(arrA, arrB)
for i in range(arrSizeDiff):
        answ[0].pop()
        answ[1].pop()
for i in answ[0]:
    print(round(i, 5), " ",end="")
print("\n")