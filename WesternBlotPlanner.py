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
    def __init__(self, gel_num, maxLanes = 10):
        assert(gel_num <6), "Too many gels"
        self.index = ['A','B','C','D','E','F'][gel_num]
        self.lanes = ()
        self.gel_num = gel_num
        assert(len(self.lanes) <= maxLanes),"Too many lanes"
    def getIndex(self):
        return self.index
    def setLane(self, lane):
        self.lanes += lane
    def getLanes(self):
        return self.lanes
    def availLanes(self):
        return maxLanes - len(self.lanes)
    def getID(self):
        return self.gel_num

class Lane(object):
    def __init__(self, exNums, ruNums, condition, sample_vol,
                 final_vol, control = False):
        self.exNums = exNums
        self.ruNums = ruNums
        self.condition = condition
        self.sample_vol = sample_vol
        self.control = control
        self.final_vol = final_vol
    def getSamples(self):
        return self.samples
    def getCondition(self):
        return self.condition
    def getSample_vol(self):
        return self.sample_vol
    def getControl(self):
        return self.control
    def __str__(self):
        return str(self.exNums).ljust(20," ")\
               + str(self.ruNums).ljust(20," ")+ \
               str(self.condition).ljust(15," ")+ str(self.sample_vol).ljust(7," ")+ \
               str(self.final_vol).ljust(3," ")
  
class FileReader(object):
    def __init__(self, file):
        self.inFile = open(file)
        self.forLanes = []
        for l in self.inFile:
            self.forLanes.append(self.splitUp(l))
    def splitUp(self, line):
        return line.split(";")
    def getForLanes(self):
        return self.forLanes
    def __str__(self):
        return (str(self.forLanes))

f = FileReader("plan.txt")
print(f)
cntrLn = []
testLn = [] 
laneTxts = f.getForLanes()
for elem in laneTxts:
    print(elem)
    if elem[0].lower() == "control":
        cntrLn.append(Lane(elem[1], elem[2], elem[3],
                     elem[4], elem[5], control = True))
    else:
        testLn.append(Lane(elem[0], elem[1], elem[2],
                     elem[3], elem[4]))
for Ln in cntrLn:
    print(Ln)
for Ln in testLn:
    print(Ln)

        
