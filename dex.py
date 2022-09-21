import json, random, re

filepath = "CPN.json"

with open(filepath,'r') as f:
    j = json.load(f)
with open("typechart.json",'r') as f:
    tc = json.load(f)
with open("moves.json","r") as f:
    ml = json.load(f)

def searchMove(name):
    for m in ml:
        if m["name"].lower() == name.lower():
            return m
    return None
                                    
def searchMon(name, writeAlt=True):
    for e in j:
        for o in e["Form"]:
            for n in o["Name"]:
                if n.lower() == name.lower():
                    return o
    print(name)
    f = searchMon(input("Alternate Name: "))
    ans = ""
    if writeAlt:
        while ans != "y" and ans != "n":
            ans = input("Add " + name + " to " +getName(f) + "? ")
            if ans =="y":
                f["Name"].append(name)
    return f
        
def getName(m):
    return m["Name"][0]
        
def write():
    ans = ""
    while ans != "y" and ans != "n":
        ans = input("Write changes? ")
        if ans =="y":
           with open(filepath,'w') as f:
                print(json.dumps(j,indent=4),file = f)
     
def getKey(form,key):
    if key in form:
        return form[key]
    print(key+" not found in "+ getName(form))
    return None
                    
def setTier(form, tier):
    form["Tier"] = tier

def getWeak(defTypes, atkType):
    s = 1
    for f in defTypes:
        s*=float(tc[f][atkType])
    return(s)
    
def quickSort(list, stat):
    if len(list) <= 1:
        return list
    pivot = list[-1]["Stats"][stat]
    high = []
    low = []
    same = []
    for f in list:
        if f["Stats"][stat]>pivot:
            high.append(f)
        elif f["Stats"][stat]<pivot:
            low.append(f)
        else:
            same.append(f)
    low = quickSort(low, stat)
    high = quickSort(high, stat)
    low.extend(same)
    low.extend(high)
    return low
    
def names(list):
    name=[]
    for l in list:
        name.append(l["Name"][0])
    return name
    
def mvalue(move):
    return int(move["power"])*int(move["accuracy"])/100
    
def coverage(f, dclass=""):
    coverage = []
    for m in f["Learnset"]:
        m = searchMove(m)
        if (dclass == "" or m["damage_class"] == dclass) and m["damage_class"] != "status" and m["type"] not in coverage:
            coverage.append(m["type"])
    return coverage
            
def bestMoves(f, dclass=""):
    coverage = {}
    for m in f["Learnset"]:
        m = searchMove(m)
        type = m["type"]
        if (dclass == "" or m["damage_class"] == dclass) and m["damage_class"] != "status" and (type not in coverage or coverage[type][1]<mvalue(m)):
            coverage[type]=(m["name"],mvalue(m))
    return coverage
    
class dexFilter:
    def __init__(self):
        self.list = []
        self.count = 0
        for m in j:
            for f in m["Form"]:
                self.list.append(f)
    
    def tierList(self, tier):
        self.list=[]
        for m in j:
            for f in m["Form"]:
                t = f["Tier"]
                if t==tier:
                    self.list.append(f)
     
    def reset(self):
        self.count = 0                
    
    def next(self):
        form = None
        if self.count < len(self.list):
            form = self.list[self.count]
        self.count +=1
        return form
        
    def size(self):
        return len(self.list)
    
    def randMon(self, remove=True):
        n = random.randrange(self.size())
        if remove:
            return self.list.pop(n)
        return self.list[n]   
    
    def randOrder(self):
        tlist = []
        list = self.list
        while len(list)>0:
            n = random.randrange(len(list))
            tlist.append(list.pop(n))
        self.list=tlist
        
    def printList(self):
      for i in self.list:
          print(i["Name"][0],i["Stats"]["Total"])
      
    def filter(self,params):
        for p in params:
            opp = re.search("[!<>=]+",p).group(0)
            keys, value = [x.strip() for x in p.split(opp,1)]
            keys = keys.split("_")                
            tlist = []
            for f in self.list:
                u = f
                for key in keys:
                    if key != "":
                        u= u[key]
                    elif "!" in opp:
                        opp = "out"
                    elif "=" in opp:
                        opp = "in"
                if "!" in opp and u != value:
                    tlist.append(f)
                elif "=" in opp and u == value:
                    tlist.append(f)
                if "<" in opp and int(u) < int(value):
                    tlist.append(f)
                if ">" in opp and u > value:
                    tlist.append(f)
                if opp == "in" and value in u:
                    tlist.append(f)
                if opp == "out" and value not in u:
                    tlist.append(f)
            self.list=tlist              

    def sort(self,stat):
        tList = self.list.copy()
        self.list= quickSort(tList, stat)
   
    def remove(self, f):
        for i in range(self.size()):
            if f in self.list[i]["Name"]:
                return self.list.pop(i)
        return None


#print(searchMon("Xerneas-*"))
#write()