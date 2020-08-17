def getRSI(data):
    iter = 0
    AU=0
    AD=0
    for curPrice in data.values:
        if iter > 0:
            if data.values[iter - 1] < curPrice:
                AU = AU + (curPrice - data.values[iter - 1])
            elif data.values[iter - 1] > curPrice:
                AD = AD + (data.values[iter - 1] - curPrice)

        iter = iter + 1
    return AU / (AD + AU)

def getOBV(data):
    iter = 0
    # for curPrice in data.values: