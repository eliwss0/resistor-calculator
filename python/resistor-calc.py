def getResistance(bands):

    digitDict = {
        "black":0,
        "brown":1,
        "red":2,
        "orange":3,
        "yellow":4,
        "green":5,
        "blue":6,
        "purple":7,
        "gray":8,
        "white":9
    }

    tolDict = {
        "brown":0.01,
        "red":0.02,
        "green":0.005,
        "blue":0.0025,
        "purple":0.001,
        "gray":0.0005,
        "gold":0.5,
        "silver":0.1
    }

    mulDict = {
        "black":1,
        "brown":10,
        "red":100,
        "orange":1000,
        "yellow":10000,
        "green":100000,
        "blue":1000000,
        "gold":0.1,
        "silver":0.01
    }

    bandList = bands.split()
    if len(bandList)==4:
        resistance = (digitDict.get(bandList[0])*10+digitDict.get(bandList[1]))*mulDict.get(bandList[2])
        tolerance = tolDict.get(bandList[3])*resistance
        return [resistance,tolerance]
    elif len(bandList)==5:
        resistance = (digitDict.get(bandList[0])*100+digitDict.get(bandList[1])*10+digitDict.get(bandList[2]))*mulDict.get(bandList[3])
        tolerance = tolDict.get(bandList[4])*resistance
        return [resistance,tolerance]
    else:
        return [0,0]
    return

bands = input("Enter band colors: ")
resistance, tolerance = [str(getResistance(bands)[i]) for i in (0,1)]
if resistance!=1:
    resistance = resistance+" Ohms"
else:
    resistance = resistance+" Ohm"
if tolerance!=1:
    tolerance = tolerance+" Ohms"
else:
    tolerance = tolerance+" Ohm"

print(str(resistance)+", "+"+-"+str(tolerance))
