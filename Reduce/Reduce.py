
from asyncio.windows_events import NULL
import math
N1 = 0

def dft(coord, isForward = True):
    global N1
    origCoord = [[], []]
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
            arg = 2*math.pi*k*n/len(coord[0])*numSign
            reCos = math.cos(arg)
            imSin = math.sin(arg)
            re += (x*reCos-y*imSin)
            im += (x*imSin + y*reCos)
        origCoord[0].append(re/divider)
        origCoord[1].append(im/divider)
    return origCoord




###################################################################
def dftA1(data, p1, p2, isForward):
    global N1
    furieA1 = [[None]*p1*p2,[None]*p1*p2]
    divider = p1
    numSign = -1
    if isForward == False:
        divider = 1
        numSign = 1
    for k1 in range(p1):
        for j2 in range(p2):
            re = 0.0
            im = 0.0
            for j1 in range(p1):
                N1+=5
                x = data[0][j2 + p2*j1]
                y = data[1][j2 + p2*j1]
                arg = 2 * math.pi *j1*k1/p1*numSign
                reCos = math.cos(arg)
                imSin = math.sin(arg)
                re += (x*reCos-y*imSin)
                im += (x*imSin + y*reCos)
            furieA1[0][k1*p2 + j2] = re/divider
            furieA1[1][k1*p2 + j2] = im/divider
            
    return furieA1



def dftA2(data, p1, p2, isForward = True):
    
    furieA2 = [[None]*p1*p2, [None]*p1*p2]
    global N1
    furieA1 = dftA1(data, p1, p2, isForward)
    divider = p2
    numSign = -1
    if isForward == False:
        divider = 1
        numSign = 1
    for k2 in range(p2):
        for k1 in range(p1):
            re = 0.0
            im = 0.0
            for j2 in range(p2):
                N1+=5
                x = furieA1[0][k1*p2 + j2]
                y = furieA1[1][k1*p2 + j2]
                arg = 2*math.pi*((j2*(k1+p1*k2)/(p1*p2)))*numSign
                reCos = math.cos(arg)
                imSin = math.sin(arg)
                re += (x*reCos-y*imSin)
                im += (x*imSin + y*reCos)
            furieA2[0][k2*p1 + k1] = re/divider
            furieA2[1][k2*p1 + k1] = im/divider
    return furieA2

###################################################################

def ChangeDigit(num, ind, dg):
    powOf2 = 2 ** ind
    if(dg == 1): num |= powOf2
    else: num &= ~powOf2
    return num

def MirrorBinarry(num,maxSize):
    offsetHints = [0b11110000,0b11001100,0b10101010]
    powOf2 = 4
    for i in range(3):
        num = ((num & offsetHints[i])>>powOf2) | ((num & ~offsetHints[i])<<powOf2)
        powOf2=int(powOf2/2)
    num >>= 8 - maxSize
    return num


def fftAn(r, dt, binarMaxSize, isForward, isLast = False):
    global N1
    answ = [[NULL]*len(dt[0]), [NULL]*len(dt[0])]
    divider = 2
    numSign = -1
    powerOf2 = 2 ** r

    if isForward == False:
        divider = 1
        numSign = 1
    for i in range(len(dt[0])):
        N1+=5
        bn = i
        mirBn = MirrorBinarry(bn, binarMaxSize) & ~((~0)<<r)
        #mirBn = MirrorBinarry(bn, binarMaxSize)

        bn = ChangeDigit(bn, binarMaxSize - r, 0)
        re = dt[0][bn]
        im = dt[1][bn]

        arg = 2*math.pi*mirBn/powerOf2*numSign
        bn = ChangeDigit(bn, binarMaxSize - r, 1)
        x = dt[0][bn]
        y = dt[1][bn]
        reCos = math.cos(arg)
        imSin = math.sin(arg)
        re += (x*reCos-y*imSin)
        im += (x*imSin + y*reCos)

        if isLast:
            answ[0][mirBn] = re/divider
            answ[1][mirBn] = im/divider
        else:
            answ[0][i] = re/divider
            answ[1][i] = im/divider 
    return answ

def fft(data, isForward = True):
    global N1
    dt = data[:]
    binarMaxSize = int(math.log2( len(data[0])+0.1))
    for i in range(binarMaxSize - 1):
        dt = fftAn(i+1, dt, binarMaxSize, isForward)
    dt = fftAn(binarMaxSize, dt, binarMaxSize, isForward, True)
    return dt

###################################################################

def reduce(arrA, arrB):
    answ = []
    global N1
    for i in range(len(arrA)):
        answ.append(0)
        print(i, ":")
        for j in range (i+1):
            print(arrA[j], " ",arrB[i-j])
            answ[i]+=arrA[j]*arrB[i-j]
            N1+=1
        print()

    for i in range(1, len(arrA)):
        answ.append(0)
        print(len(arrA)+i-1, ":")
        for j in range (i, len(arrA)):
            print(arrA[j], " ",arrB[len(arrB)-j+i-1])
            answ[len(answ)-1]+=arrA[j]*arrB[len(arrB)-j+i-1]
            N1+=1
        print()

    return answ

def coordMult(arrA, arrB, dopMult = 1):
    global N1
    answ = [[],[]]
    for i in range(len(arrA[0])):
        N1+=2
        answ[0].append((arrA[0][i]*arrB[0][i] - arrA[1][i]*arrB[1][i])*dopMult)
        answ[1].append((arrA[0][i]*arrB[1][i] + arrB[0][i]*arrA[1][i])*dopMult)
    return answ

def reduceDft(arrA, arrB, dftType):
    arrSize = len(arrA)
    global N1
    arrAforDft = [arrA, [0]*(2*arrSize)]
    arrBforDft = [arrB,[0]*(2*arrSize)]
    dopMult = 2*arrSize
    for i in range(arrSize):
        arrAforDft[0].append(0)
        #N1+=1
        #arrAforDft[0][i]*=2*arrSize
        arrBforDft[0].append(0)
    if dftType == 0:
        return dft(coordMult(dft(arrAforDft), dft(arrBforDft), dopMult),False)[0]
    elif dftType == 1:
        size = len(arrA)
        for i in range(1, math.floor(math.sqrt(len(arrA)))+1):
            if(size%i==0):
                mult1 = i
                mult2 = int(size/i)
        print("Mult = ", mult1," ",mult2)
        dftA = dftA2(arrAforDft, mult1, mult2)
        dftB = dftA2(arrBforDft, mult1, mult2)
        crmult = coordMult(dftA, dftB, dopMult)
        return dftA2(crmult, mult1, mult2, False)[0]
    elif dftType == 2:
        return fft(coordMult(fft(arrAforDft), fft(arrBforDft), dopMult),False)[0]

def LevelLenOfArr(arrA, arrB):
    dopDiff = (len(arrA)-1)+(len(arrB)-1) +1
    arrSizeDiff = abs(len(arrA)-len(arrB))
    if(len(arrA)>len(arrB)):
            for i in range(arrSizeDiff):
                arrB.append(0)
    else :
        if(len(arrB)>len(arrA)):
            for i in range(arrSizeDiff):
                arrA.append(0)
    return dopDiff

def ChooseReduceAndRun(name, rtype, A, B):
    print("\n\n", name)
    arrSizeDiff = LevelLenOfArr(A, B)
    global N1
    N1 = 0
    #0 - standart     1 - dft       2 - pdft
    if rtype == 0:
        answ = reduce(A, B)
    else:
        answ = reduceDft(A, B, rtype - 1)
    s =len(answ)
    for i in range(s - arrSizeDiff):
            answ.pop()
    for i in answ:
        print(round(i, 5), " ",end="")

    print("\nN1 = ", N1)


################################################################

arrA = [1,2,3]
arrB = [4,5,6,9]
print("A:", arrA)
print("B:", arrB)
ChooseReduceAndRun("Standart",0,arrA[:], arrB[:])
ChooseReduceAndRun("With dft:",1,arrA[:], arrB[:])
ChooseReduceAndRun("With pdft:",2,arrA[:], arrB[:])
ChooseReduceAndRun("With fft:",3,arrA[:], arrB[:])