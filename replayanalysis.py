import battle, paste, os, json
import requests

usage = {}
class replay:
    def __init__(self):
        self.data={}
        self.joined=[]
        self.chatlog=""
        self.gtype=""
        self.gn=""
        self.tr=""
        self.rules=[]
        self.battle = battle.battle()
   
    def j(self, d):
        if d[0] not in self.joined:     
            self.joined.append(d[0])
    
    def switch(self,d):
        m = self.monTeam(d[0])
        if m==None:
            player, nick = d[0].split(": ")
            n = d[1].split(',')[0]
            #print(player, nick,n)
            for m in self.data[player[:-1]]["team"]:
                if m.name == n:
                    m.name = nick                             
                                        
    def player(self,d):
        self.data[d[0]] = {}
        self.data[d[0]]["name"] = d[1]
        
    def c(self,d):
        self.chatlog = self.chatlog+(": ".join(d)+"\n")
    
    def teamsize(self,d):
        size = int(d[1])
        self.data[d[0]]["teamsize"]=[size]
    
    def gametype(self,d):
        self.gametype=d[0]
    
    def gen(self,d):
        self.gn=d[0]

    def tier(self,d):
        self.tr=d[0]
        
    def rule(self,d):
        self.rules.append(d[0])
    
    def clearpoke(self,d):
        for p in self.data:
            self.data[p]["team"] = []
    
    def poke(self,d):
        mon = d[1]
        mon = mon.split(",")[0]
        self.data[d[0]]["team"].append(battle.mon(mon))
      
    def move(self,d):
        mon = self.monTeam(d[0])
        for m in mon.moves:
            if m == d[1]:
                return
        mon.moves.append(d[1])
    
    def item(self, d):
        mon = self.monTeam(d[0])
        mon.item = d[1]
            
    def monTeam(self, playerMon):
        player, monName = playerMon.split(": ")
        player = player[:-1]
        for m in self.data[player]["team"]:
            if m.name == monName:
                return m
        return None
                
    def boost(self,d):
        mon = self.monTeam(d[0])
        rename = {"spa": "SpA","atk":"Atk", "def":"Def", "spd":"SpD", "spe":"Spe", "evasion":"Eva", "accuracy":"Acc"}
        d[1] = rename[d[1]]
        stage = mon.stages[d[1]]+int(d[2])
        #print(mon.name,d[1],stage)
        mon.setStage(d[0],stage)
        
    def unboost(self,d):
        d[2]=int(d[2])*-1
        self.boost(d)
        
    def update(self):
        for player in self.data:
            if self.data[player]["name"] in ["DJSen"]:
                for m in self.data[player]["team"]:
                    mname = m.form["Name"][0]
                    if mname not in usage:
                        usage[mname] = {}
                    if "used" not in usage[mname]:
                        usage[mname]["used"]=0
                    usage[mname]["used"]+=1
                    if "moves" not in usage[mname]:
                        usage[mname]["moves"]={}
                    for move in m.moves:
                        if move not in usage[mname]["moves"]:
                            usage[mname]["moves"][move]=0
                        usage[mname]["moves"][move]+=1    
                    
def scanUrl(url):
    r = requests.get(url+".json")
    return(r.json()["log"].split("\n"))                   
        
def scanFile(file):
    raw = []
    collecting =False
    with open(file,'r') as f:
        for l in f:
            if "class=\"battle-log-data\"" in l and not collecting:
                raw.append(l[l.find('>')+1:])
                collecting=True
            elif collecting:
                if "</script>" in l:
                    break
                else:
                    raw.append(l)
    return raw

def parseLog(log):
    data = []
    for l in log:
        l = l[1:]
        l = l.strip()
        if l!='':
            data.append(l.split('|'))
    return data

def runData(data):
    m = replay()
    for d in data:
        if d[0][0]=='-':
            d[0]=d[0][1:]
        if hasattr(m,d[0]):
            getattr(m,d[0])(d[1:])
        else:
            print(d)
        
  #  for player in m.data:
      #  print(m.data[player]["name"])
        #if m.data[player]["name"] =="DJSen":
            #paste.export(m.data[player]["team"])
    m.update()

    
'''            
dir = "Replays"
for file in os.listdir(dir):
    print(scanFile(os.path.join(dir,file)))
'''
log = scanFile("replay.html")
data=parseLog(log)
print(data)
#runData(data)
    
#print(json.dumps(usage, indent=4))
#log = scanUrl("https://replay.pokemonshowdown.com/sports-gen8nationaldexvgc-719272-o9i9tcbbre0revrm3p5vxsmrdjhawndpw")
