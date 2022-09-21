import dex, math
class battle:
    def __init__(self):
        print("fight!")
        
class mon:
    def __init__(self, monName, bpm=1, status="Healthy", item=None, evs={"HP":0,"Atk":0,"Def":0,"SpA":0,"SpA":0,"Spe":0}, ivs={"HP":31,"Atk":31,"Def":31,"Sp. Atk":31,"Sp. Def":31,"Spe":31}, level=100, nature=1, stages={"Atk":0,"Def":0,"SpA":0,"SpD":0,"Spe":0,"Eva":0,"Acc":0}, ability=None):
        self.form = dex.searchMon(monName,writeAlt=False)
        self.name = monName
        self.level=level
        self.stages=stages
        self.ivs = ivs
        self.evs=evs
        self.bpm=bpm
        self.nature=nature
        self.status=status
        self.item=item
        self.moves=[]
        self.ability=ability
        
    def getBaseStat(self, statName):
        s = self.form["Stats"]
        if statName in s:
            return int(s[statName])
            
    def stat(self,statName):
        if statName == "HP":
            s = 2*self.getBaseStat(statName) + self.ivs[statName] + math.floor(self.evs[statName]/4)
            s = math.floor(s*self.level/100) + self.level + 10
        else:
            s = 2*self.getBaseStat(statName)+ self.ivs[statName] + math.floor(self.evs[statName]/4)
            s = math.floor(s*self.level/100) +5
            s = math.floor(s*self.nature)
            #stat stages
            a = 2
            b = 2
            if self.stages[statName] > 0:
                a += self.stages[statName]
            else:
                b -= self.stages[statName]
            s = math.floor((s*a)/b)
            #item
            s = math.floor(s*self.item)
        return s
    
    def setEv(self,statName,value):
        if statName in self.evs and value<256 and value>=0:
            self.evs[statName] = value
    
    def setStage(self,statName,value):
        if statName in self.stages and value < 7 and value >-7:
            self.stages[statName] = value
     
    def totalEv(self):
        total = 0
        for ev in evs:
            total += evs[ev]
        return total
        