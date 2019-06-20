class WBRecord(object):
    def __init__(self, date, gels, id = 'WB#XX.YYY',
               head = ('Ex#', 'RU#', 'Cond', 'sample vol',
                       'buffer', 'LB')):
        self.date = date
        self.gels = gels
        self.id = id
        self.head = head
    def getID(self):
        return self.id
    def getHead(self):
        return self.head
            
class Gel(object):
    gel_num = 0
    def __init__(self, maxLanes = 10):
        assert(Gel.gel_num <6), "Too many gels"
        self.index = ['A','B','C','D','E','F'][Gel.gel_num]
        self.laneNum = 2
        self.lanes = []
        self.gel_num = Gel.gel_num
        assert(len(self.lanes) <= maxLanes),"Too many lanes"
    def getIndex(self):
        return self.index
    def setLane(self, lane):
        assert(self.laneNum <= 10),"Too many lanes"
        self.lanes.append(lane)
        self.laneNum += 1
    def getLanes(self):
        for lane in self.lanes:
            yield lane.__str__()
    def availLanes(self):
        return maxLanes - len(self.lanes)
    def getID(self):
        return self.gel_num

class Lane(object):
    def __init__(self, exNums, ruNums, condition, sample_vol,
                 final_vol, control = False):
        self.num = 0
        self.exNums = exNums
        self.ruNums = ruNums
        self.condition = condition
        self.sample_vol = sample_vol
        self.control = control
        self.final_vol = final_vol
    def setNum(self, num):
        self.num = num
    def getNum():
        return self.num
    def getSamples(self):
        return self.samples
    def getCondition(self):
        return self.condition
    def getSample_vol(self):
        return self.sample_vol
    def getControl(self):
        return self.control
    def __str__(self):
        return str(self.num).ljust(4, " ") + str(self.exNums).ljust(20," ")\
               + str(self.ruNums).ljust(20," ")+ \
               str(self.condition).ljust(15," ")+ str(self.sample_vol).ljust(7," ")+ \
               str(self.final_vol).ljust(3," ")
  
class FileReader(object):
    def __init__(self, file):
        self.inFile = open(file)
        self.forLanes = []
        for l in self.inFile:
            self.forLanes.append(self.splitUp(l))
        self.cntrLn = []
        self.testLn = []
        self.std = []
        self.mrk = []
    def splitUp(self, line):
        return line.split(";")
    def getForLanes(self):
        return self.forLanes
    def laneSort(self):      
        laneType = None
        for elem in self.forLanes:
            if elem[0].lower() == "control":
                laneType = self.cntrLn
            elif elem[0].lower() == "standard":
                laneType = self.std
            elif elem[0].lower() == "marker":
                laneType = self.mrk
        if laneType == None:
            for i in range(len(elem[2].split(","))):
                self.testLn.append(Lane(elem[0], elem[1],
                                        elem[2].split(",")[i],
                                        elem[3].split(",")[i],
                                        elem[4]))

        else:
            for i in range(len(elem[2].split(","))):
                laneType.append(Lane(elem[1], elem[2],
                                        elem[3].split(",")[i],
                                        elem[4].split(",")[i],
                                        elem[5]))



            
    def getLanes(self):
        return self.mrk, self.cntrLn, self.testLn, self.std 
    def close(self):
        self.inFile.close()
    def __str__(self):
        return (str(self.forLanes))

f = FileReader("plan.txt")
f.laneSort()
mrk, cntrLn, testLn, std = f.getLanes()
g = Gel()
num = 1
for laneType in mrk, cntrLn, testLn, std :
    for Ln in laneType:
        Ln.setNum(num)
        g.setLane(Ln)
        num += 1
    
g.getLanes()
print("Gel ", g.getIndex())
for lane in g.getLanes():
    print(lane)
f.close()
        
