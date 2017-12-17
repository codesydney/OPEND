import re


fileIn  = open("NSWPopulation_001.csv", "r")
fileOut  = open("NSWPopulation_002.csv", "w")

for line in fileIn: 
    #print(line)
    data = line.split(",")
    print(data[1],"=>",end = '')
    suburbNoBracket = re.sub("[\(].*?[\)]", "", data[1])
    suburbNoBracket = re.sub("\s+\Z","",suburbNoBracket)
    #suburbNoBracket.rstrip()
    print(suburbNoBracket,"=>",end='')
    data[1]=suburbNoBracket
    dataOut = ','.join(data)
    print(dataOut)
    fileOut.write(dataOut);

fileOut.close()
fileIn.close()

