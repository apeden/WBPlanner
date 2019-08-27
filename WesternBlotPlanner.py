from datetime import date
today = date.today()
d1 = today.strftime("%d/%m/%Y")
import pylab


class WBRecord(object):
    """Record of WB and its gels"""
    def __init__(self, file, planData = d1, operative = "Alex Peden",
                 dev = "3F4 1:10K, antiMFab 1:25K"):
        self.gels = []
        self.id = file
        self.planDate = d1
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
        return self.id+"\n"+self.operative+"\n"+"Printed on "+self.planDate\
               +"\n"+self.dev 
            
class Gel(object):
    """Describes samples analysed on one gel"""
    def __init__(self, num, maxLanes = 10):
        self.num = num
        self.maxLanes = maxLanes
        self.index = ['A','B','C','D','E','F'][self.num]
        self.lanes = []
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
        return "\nGel " + self.index

class Lane(object):
    """A Lane to be placed on a gel"""
        #forLanes: type;RU#;Tissues;Exs;Conditions;Volumes;FinalVol
        #or:       type;Markers;Vol;None;None;None;FinalVol
    def __init__(self, laneType, ruNums, tissue, exNums, condition, sample_vol,
                 final_vol, numCond, control = False):
        self.laneType = laneType
        self.tissue = tissue
        self.exNums = exNums
        self.ruNums = ruNums
        self.condition = condition
        self.sample_vol = sample_vol
        self.final_vol = final_vol
        self.numCond = numCond
        self.control = control
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
    def getTissue(self):
        return self.tissue
    def getNumCond(self):
        return self.numCond
    def getLaneComponents(self):
        return [str(self.laneType),
               str(self.exNums),
               str(self.ruNums),
               str(self.condition),
               str(self.tissue),
               str(self.sample_vol),
               str(self.final_vol)]
    def __str__(self):
        return str(self.laneType).ljust(10,"_")\
               + str(self.exNums).ljust(25,"_")\
               + str(self.ruNums).ljust(27,"_")\
               + str(self.condition).ljust(15,"_")\
               + str(self.tissue).ljust(10,"_")\
               + str(self.sample_vol).ljust(3,"_") \
               + str(self.final_vol).ljust(3,"_")
  
class FileReader(object):
    def __init__(self, directory, file):
        try:
            self.inFile = open(directory+"/"+file)
        except FileNotFoundError:
            print("Could not find file ",file,"in ",directory)
        self.forLanes = []
        for l in self.inFile:
            self.forLanes.append(l.split(";"))
        self.lanes = [] 
        self.dscrpt = self.forLanes[0][0]
        self.perfDate =self.forLanes[1][0]
    def getForLanes(self):
        return self.forLanes
    def laneSort(self):      
        """Classify lanes and sort into separate dicts"""
        laneType = None
        for lineData in self.forLanes[2:]:
            laneDict = {}
            for i in range(len(lineData[2].split(","))):
                for j in range(len(lineData[4].split(","))):
                    try:
                        laneDict["Type"] = lineData[0] 
                        laneDict["Case"] = lineData[1]
                        laneDict["Tissue"] = lineData[2].split(",")[i] 
                        laneDict["Ex Num"] = lineData[3].split(",")[i]
                        laneDict["Condition"] = lineData[4].split(",")[j]
                        laneDict["Sample Volume"] = lineData[5].split(",")[j]
                        laneDict["Final Vol"] = lineData[6]
                    except IndexError:
                        print("There must be a load volume stated",
                              " for each condition",
                              " and an extract number",
                              "  for each tissue")
                        raise
            self.lanes.append(laneDict)
    def getDscrpt(self):
        return self.dscrpt
    def getPerfDate(self):
        return self.perfDate 
    def getLanes(self):
        return self.lanes
    def close(self):
        self.inFile.close()
    def __str__(self):
        return (str(self.forLanes))

##class GelPlanner(object):
##    def __init__(self, directory, file):
##        self.r = WBRecord(file)
##        self.f = FileReader(directory, file+".txt")
##        self.f.laneSort()
##        self.lanes = self.f.getLanes()
##        self.g = None
##        self.num = 0
##    def getTestLns(self):
##        return self.testLn
##    def getRecord(self):
##        return self.r
##    def getDscrpt(self):
##        return self.f.getDscrpt()
##    def getPerfDate(self):
##        return self.f.getPerfDate()
##    def closeFile(self):
##        self.f.close()
##    def setGel(self):
##        self.g = Gel(self.num)
##        self.num += 1
##    def getGel(self):
##        return self.g
##    def setLn(self, ln):   
##        self.g.setLane(ln)
##    def add_conlanes(self):
##        for laneType in self.mrk, self.cntrLn:
##            for i in range(len(laneType)):
##                self.setLn(laneType[i])
##    def add_testlanes(self):
##        tissue = ""
##        availSpaces = self.g.getMaxLanes()\
##        -len(self.mrk)\
##        -len(self.cntrLn)\
##        -len(self.std)
##        #if there aren't enough spaces for all conditions, move on
##        i = 0
##        while(availSpaces-i>0) and (len(self.testLn) > 0):
##            if (self.testLn[0].getTissue() != tissue) \
##               and (self.testLn[0].getNumCond() > availSpaces-i):
##                break
##            tissue = self.testLn[0].getTissue()
##            self.setLn(self.testLn.pop(0))
##            i += 1
##    def add_stdlanes(self):
##        for i in range(len(self.std)):
##            self.setLn(self.std[i])
##    def buildGels(self):
##        while len(self.testLn) > 0:
##            self.setGel()
##            self.add_conlanes()
##            self.add_testlanes()
##            self.add_stdlanes()
##            self.addGel(self.getGel().copy())
##    def buildDiagGels(self, numStd = 4):
##        while len(self.testLn) > 0:
##            self.setGel()
##            n = 0
##            self.setLn(self.mrk[0])
##            while(len(self.testLn) > 0):
##                self.setLn(self.testLn.pop(0))
##                self.setLn(self.std[n]) 
##                n += 1
##            self.setLn(self.std[n])
##            self.addGel(self.getGel().copy())
##    def addGel(self, gel):
##        self.r.setGel(gel)
##    def __str__(self):
##        return str(self.r)
##
##def toTextFile(
##    file, directory = "plans", scrnPrnt = True, repeat = 1, diag = False):
##    p = GelPlanner(directory,file)
##    memo = open(file+" lane order.txt", "w")
##    if scrnPrnt:
##        print(p.getRecord())
##        print(p.getDscrpt())
##        print("Performed on "+p.getPerfDate())
##    memo.write(p.getRecord().__str__()+"\n")
##    memo.write(p.getDscrpt()+"\n")
##    memo.write("Performed on "+p.getPerfDate())
##    if diag:
##        p.buildDiagGels() 
##    else:
##        p.buildGels()
##    gel_it = p.getRecord().getGelsIt()
##    for gel in gel_it:
##        rowLabels, columnLabels, tableVals = [],[],[]
##        if scrnPrnt: print(gel)
##        memo.write(gel.__str__()+"\n")
##        positn = 1
##        for lane in gel.getLanes():
##            columnLabels = ["Lane",
##                            "Type",
##                            "Ex#",
##                            "RU#",
##                            "Cond",
##                            "Tissue",
##                            "Sample vol",
##                            "Final vol"]
##            rowLabels.append(positn)
##            if scrnPrnt: print(str(positn).ljust(3,"_"),lane)
##            lane.replace("_"," ")
##            print(lane.__str__().split("_"," "))
##            tableVals.append(lane.__str__().split("_",""))
##            memo.write(str(positn).ljust(3,"_")+str(lane)+"\n")
##            positn += 1
##        #Produce table
##        table = pylab.table(rowLabels = rowLabels,
##                            colLabels = columnLabels,
##                            cellText = tableVals,
##                            cellLoc = 'center',
##                            loc = 'center',
##                            colWidths = [0.2]*8)
##        table.scale(1, 2.5)
##        pylab.title(gel.__str__())
##    memo.close()            
##    p.closeFile()
##
##toTextFile("WB#19.089 AP (NaPTA - 21 23 24 25 28 29)")
##
##
##
