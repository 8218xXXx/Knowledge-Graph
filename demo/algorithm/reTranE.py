import sys
sys.path.append('../')
from tranE import *

def loadData(str):
    fr = open(str)
    sArr = [line.strip().split("\t") for line in fr.readlines()]
    datArr = [[float(s) for s in line[1][1:-1].split(", ")] for line in sArr]
    nameArr = [line[0] for line in sArr]
    dic = {}
    for name, vec in zip(nameArr, datArr):
        dic[name] = vec
    return dic

if __name__ == '__main__':
    dirEntityVector = "/Users/yfli/Desktop/实验品/demo/algorithm/result/entityVector.txt"
    entityList = loadData(dirEntityVector)
    dirRelationVector = "/Users/yfli/Desktop/实验品/demo/algorithm/result/relationVector.txt"
    relationList = loadData(dirRelationVector)
    dirTrain = "/Users/yfli/Desktop/实验品/demo/algorithm/train.txt"
    tripleNum, tripleList = openTrain(dirTrain)
    transE = TransE(entityList, relationList, tripleList, learingRate = 0.01, dim = 50)
    transE.transE(100000)
    transE.writeRelationVector("/Users/yfli/Desktop/实验品/demo/algorithm/result/relationVector.txt")
    transE.writeEntilyVector("/Users/yfli/Desktop/实验品/demo/algorithm/result/entityVector.txt")