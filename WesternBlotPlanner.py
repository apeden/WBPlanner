class WBRecord(object):
    def __init__(self, id = 'WB#XX.YYY', date, gels,
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
    def __init__(self, gel_num, lanes, maxLanes = 10):
        self.lanes = lanes
        self.gel_num = gel_hum
        assert(len(self.lanes) <= maxLanes)"Too many lanes"
    def getLanes(self):
        return self.lanes
    def getID(self):
        return self.gel_num

class Lane(object):
    def __init__(self, samples,  condition, sample_vol,
                 control = False, final_vol = 20):
        self.samples = samples
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
        return self.condition, str(self.sample_vol), \
               str(self.final_vol - self.sample_vol - (self.final-vol//4)),\
               str(self.final_vol//4)


    
class fileReader(object):
    def __init__(self, file):
        self.inFile = open(file)
        self.forLanes = []
        for l in inFile:
            forLanes.append(splitUp(l))
    def splitUp(self, line)
        return line.split(",")
        
