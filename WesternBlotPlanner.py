from datetime import date
today = date.today()
d1 = today.strftime("%d/%m/%Y")


class WBRecord(object):
    def __init__(self, file, planData = d1, operative = "Alex Peden",
                 dev = "3F4 1:10K, antiMFac 1:25K"):
        self.gels = []
        self.id = file
        self.planDate = d1
        self.planDate
        self.operative = operative
        self.dev = dev
        if "napta" in self.id.lower():
            self.dev += " SuperSignal"
        else: self.dev += " prime"          
    def getID(self):
        return self.id
    def setGel(self, gel):
        self.gels.append(gel)
    def getGels(self):
        return self.gels
    def getGelsIt(self):
        for gel in self.gels:
            yield gel
    def __str__(self):
        return self.id+"\n"+self.operative+"\n"+self.planDate\
               +"\n"+self.dev 
            
class Gel(object):
    def __init__(self, num, maxLanes = 10):
        self.num = num
        self.maxLanes = maxLanes
        self.index = ['A','B','C','D','E','F'][self.num]
        self.lanes = []
        assert(len(self.lanes) <= self.maxLanes),"Too many lanes"
    def getMaxLanes(self):
        return self.maxLanes
    def setLane(self, lane):
        self.lanes.append(lane)
    def getLanes(self):
        for lane in self.lanes:
            yield lane.__str__()
    def availLanes(self):
        return self.maxLanes - len(self.lanes)
    def getID(self):
        return self.gel_num
    def copy(self):
        return self
    def __str__(self):
        return "Gel " + self.index

class Lane(object):
    def __init__(self, laneType, exNums, ruNums, condition, sample_vol,
                 final_vol, control = False):
        self.num = 0
        self.laneType = laneType
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
        return str(self.num).ljust(4, " ") \
               + str(self.laneType).ljust(10," ")\
               + str(self.exNums).ljust(20," ")\
               + str(self.ruNums).ljust(20," ")\
               + str(self.condition).ljust(20," ")\
               + str(self.sample_vol).ljust(7," ") \
               + str(self.final_vol).ljust(3," ")
  
class FileReader(object):
    def __init__(self, file):
        self.inFile = open(file)
        self.forLanes = []
        for l in self.inFile:
            self.forLanes.append(l.split(";"))
        self.cntrLn = []
        self.testLn = []
        self.std = []
        self.mrk = []
    def getForLanes(self):
        return self.forLanes
    def laneSort(self):      
        laneType = None
        for elem in self.forLanes:
            typ = elem[0].lower()
            if "control" in typ:
                laneType = self.cntrLn
            elif "marker" in typ:
                laneType = self.mrk
            elif "standard" in typ:
                laneType = self.std
            else: laneType = self.testLn 
            for i in range(len(elem[3].split(","))):
                laneType.append(Lane(elem[0], elem[1], elem[2],
                                     elem[3].split(",")[i],
                                     elem[4].split(",")[i],
                                     elem[5]))
    def getLanes(self):
        return self.mrk, self.cntrLn, self.testLn, self.std 
    def close(self):
        self.inFile.close()
    def __str__(self):
        return (str(self.forLanes))

class GelPlanner(object):
    def __init__(self, file):
        self.r = WBRecord(file)
        self.f = FileReader(file)
        self.f.laneSort()
        self.mrk, self.cntrLn, \
        self.testLn, self.std = self.f.getLanes()
        self.g = None
        self.num = 0
        self.lane_num = 1
    def getTestLns(self):
        return self.testLn
    def getRecord(self):
        return self.r
    def closeFile(self):
        self.f.close()
    def setGel(self):
        self.lane_num = 1
        self.g = Gel(self.num)
        self.num += 1
    def getGel(self):
        return self.g
    def setLn(self, ln):
        print(self.lane_num)
        ln.setNum(self.lane_num)    
        self.g.setLane(ln)
        self.lane_num += 1
    def add_conlanes(self):
        for laneType in self.mrk, self.cntrLn:
            for i in range(len(laneType)):
                self.setLn(laneType[i])
    def add_testlanes(self):
            for i in range(self.g.availLanes()-1):
                try:
                    self.setLn(self.testLn.pop(0))
                except: break
    def add_stdlanes(self):
        for i in range(len(self.std)):
            self.setLn(self.std[i])
    def addGel(self, gel):
        self.r.setGel(gel)
    def __str__(self):
        return str(self.r)


p = GelPlanner("plan.txt")
i = 0
print(p.getRecord())
while len(p.getTestLns())>0:
    p.setGel()
    p.add_conlanes()
    p.add_testlanes()
    p.add_stdlanes()
    p.addGel(p.getGel().copy())   
    gel = p.getRecord().getGels()[i]
    print(gel)
    i += 1
p.closeFile()
        
