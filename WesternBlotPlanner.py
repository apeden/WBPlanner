from datetime import date
today = date.today()
d1 = today.strftime("%d/%m/%Y")


class WBRecord(object):
    def __init__(self, file, planData = d1, operative = "Alex Peden",
                 dev = "3F4 1:10K, antiMFab 1:25K"):
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
        self.laneType = laneType
        self.exNums = exNums
        self.ruNums = ruNums
        self.condition = condition
        self.sample_vol = sample_vol
        self.control = control
        self.final_vol = final_vol
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
        return str(self.laneType).ljust(10," ")\
               + str(self.exNums).ljust(20," ")\
               + str(self.ruNums).ljust(20," ")\
               + str(self.condition).ljust(20," ")\
               + str(self.sample_vol).ljust(7," ") \
               + str(self.final_vol).ljust(3," ")
  
class FileReader(object):
    def __init__(self, directory, file):
        self.inFile = open(directory+"/"+file)
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
    def __init__(self, directory, file):
        self.r = WBRecord(file)
        self.f = FileReader(directory, file+".txt")
        self.f.laneSort()
        self.mrk, self.cntrLn, \
        self.testLn, self.std = self.f.getLanes()
        self.g = None
        self.num = 0
    def getTestLns(self):
        return self.testLn
    def getRecord(self):
        return self.r
    def closeFile(self):
        self.f.close()
    def setGel(self):
        self.g = Gel(self.num)
        self.num += 1
    def getGel(self):
        return self.g
    def setLn(self, ln):   
        self.g.setLane(ln)
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

file = "WB#19.XXX AP (PMCA - 20)"

p = GelPlanner("plans",file)
i = 0
memo = open(file+" lane order.txt", "w")

print(p.getRecord())
memo.write(p.getRecord().__str__()+"\n")
while len(p.getTestLns())>0:
    p.setGel()
    p.add_conlanes()
    #for lanes in p.if it says alone
    #and none of the lanes already in gel mismatch on elem[2] continue
        #continue
        #else: break
    p.add_testlanes()
    
    p.add_stdlanes()
    p.addGel(p.getGel().copy())   
gel_it = p.getRecord().getGelsIt()
for gel in gel_it:
    print(gel)
    memo.write(gel.__str__()+"\n")
    positn = 1
    for lane in gel.getLanes():
        print(str(positn).ljust(3," "),lane)
        memo.write(str(positn).ljust(3," ")+str(lane)+"\n")
        positn += 1
memo.close()            
p.closeFile()
        
