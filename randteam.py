import random, json, math, group, time
import dex as d
teamsize = 8
maxTypes = 1

#tiers = ["A","B","B","C","C","D","D","E"]
tiers = ["C","B","B"]
setMons=["Charizard-Mega-X"]
banList = ["Slaking","Archeops"]

with open("CPN.json",'r') as f:
    j = json.load(f)
with open("typechart.json",'r') as f:
    tc = json.load(f)
    
def monValid(form):
    for t in getTypes(form):
        if teamTypes(mons)[t] >= maxTypes:
            return False
    if form["Group"] not in ["","Psuedo"]:
        return False
    for n in form["Name"]:
        if  "-Mega" in n:
            return False
        if n in banList:
            return False
    return True

def randTeam():
    global mons
    mons = []
    tc = tiers.copy()
    for m in setMons:
        f = d.searchMon(m)
        t = d.getKey(f,"Tier")
        if t in tc:
            tc.remove(t)
            mons.append(f)
        else:
            print(m + " is too expensive")     
    ftr = d.dexFilter()
    for t in tc:
        ftr.tierList(t)
        f = ftr.randMon()
        mons.append(f)
    return mons

def teamTypes(team):
    typeCount = {"normal":0,"fire":0,"water":0,"electric":0,"grass":0,"ice":0,"fighting":0,"poison":0,"ground":0,"flying":0,"psychic":0,"bug":0,"rock":0,"ghost":0,"dragon":0,"dark":0,"steel":0,"fairy":0}
    for u in team:
        for t in getTypes(u):
            typeCount[t]+=1
    return typeCount

def teamNames(team):
    return [getName(x) for x in team]
                
def getTypes(f):
    types = f["Types"]
    return types

def typeToString(types):
    types.sort()
    sortTypes = " ".join(types)
    return (sortTypes)
    
def getName(m):
    return m["Name"][0]

def getStrengths(mon):
    monType = getTypes(mon)
    types=["normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel","fairy"]
    strengths = [1]*len(types)
    for i in range(len(types)):
        strengths[i] = float(max([tc[types[i]][x] for x in monType]))
    return strengths

def bestMon(team,ftr):
    weak = sum(calcTeamWeak(team))
    avgBst = avgStats(team)["Total"]
    ftr.reset()
  #  ftr.randOrder()
    f = ftr.next()
    bestMon = f
    while f != None:
        tteam = team.copy()
        tteam.append(f)
        tt = teamTypes(tteam)
        tweak = calcTeamWeak(tteam)
      #  print(f["Name"][0],tweak)
        tweak = sum(tweak)
     #   print(f["Name"][0],tweak)
        tbst = avgStats(tteam)["Total"]
        if weak>tweak or (weak==tweak and tbst> avgBst):
            bestMon = f
            weak = tweak
            avgBst = tbst
        f = ftr.next()
    return bestMon
                    
def getWeakness(mon):
    monType = getTypes(mon)
    weak = [1]*18
    types=["normal","fire","water","electric","grass","ice","fighting","poison","ground","flying","psychic","bug","rock","ghost","dragon","dark","steel","fairy"]
    for mt in monType:
        for t in range(18):
            weak[t] = weak[t]*float(tc[mt][types[t]])
    for a in mon["Abilities"]:
        if a in tc:
           for t in range(18):
               weak[t] = weak[t]*float(tc[a][types[t]])
    return weak
    
def calcTeamWeak(team):
    teamWeak=[0]*18
    for u in team:
        weak = getWeakness(u)
        for w in range(18):
                if weak[w] == 0:
                    weak[w] += .25
                teamWeak[w] += math.log2(weak[w])
    for w in range(18):
        if teamWeak[w] > 0:
            teamWeak[w] = teamWeak[w]*5
    return teamWeak
    
def calcTeamStrength(team):
    teamWeak=[0]*18
    for u in team:
        strengths = getStrengths(u)
        for w in range(18):
            teamWeak[w]+=(strengths[w]-1)
    return teamWeak

def uniqueTypes(team):
    types = []
    for u in team:
        for t in getTypes(u):
            types.append(t)
    return set(types)
        
def printTeam(team):
    for u in team:
        name = getName(u)
        print(name)

def avgStats(team):
    astats = {"HP":0,"Atk":0,"Def":0,"Sp. Atk":0,"Sp. Def":0,"Spd":0,"Total":0}
    if len(team) == 0:
        return astats
    for u in team:
        for s in u["Stats"]:
            astats[s]+=int(u["Stats"][s])
    for u in astats:
        astats[u] = round(astats[u]/len(team))
    return astats

def evaluate(team):
    tt = teamTypes(team)
    count =0
    for t in tt:
        if tt[t]>2:
            return None
        if tt[t]>1:
            count+=1
            if count>2:
                return None
    return(team)

def main():
    lowestteam = []
    highestteam = []
    highestbst = 0
    lowestweak = 100
    
    for i in range(200):
        print(str(i))
        eteam = None
        while eteam == None:
            eteam = randImpTeam()
        tw = calcTeamWeak(eteam)
        avs = avgStats(eteam)
        s=sum(tw)
        if lowestweak>s or (lowestweak==s and highestbst <avs["Total"]):
            lowestweak=s
            lowestteam=eteam
            highestbst= avs["Total"]
    print()
    printTeam(lowestteam)
    print(lowestweak)

def newRandTeam(n):
    ftr = d.dexFilter(d)
    team = []
    ftr.filter(["Viable=TRUE","Group!Restricted","Group!Mythical","Group!Legendary","Group!Ultra Beast","Group!Mega"])
    ftr.filter(["Name_!Slaking"])
    for i in range(n):
        f = ftr.randMon()
        team.append(f)
        for t in f["Types"]:
            ftr.filter(["Types_!="+t])
    return team

def randBestTeam(n):
    d = dex.makeDex()
    ftr = dex.dexFilter(d)
    team = []
    ftr.filter(["Viable=TRUE","Group!Restricted","Group!Mythical","Group!Legendary","Group!Ultra Beast","Group!Mega"])
    ftr.filter(["Name_!Slaking","Name_!Shedinja"])
    for i in range(n):
        f = bestMon(team,ftr)
        for t in f["Types"]:
            ftr.filter(["Types_!="+t])
        team.append(f)
    return(team)

def improveTeam(team):
    d = dex.makeDex()
    for i in range(len(team)):
        ftr = dex.dexFilter(d)
        ftr.filter(["Viable=TRUE","Group!Restricted","Group!Mythical","Group!Legendary","Group!Ultra Beast","Group!Mega"])
        ftr.filter(["Name_!Slaking","Name_!Shedinja"])
        tteam = team.copy()
        tteam.pop(i)
        for m in tteam:
            ftr.filter(["Name_!"+m["Name"][0]])
        for t in uniqueTypes(tteam):
            ftr.filter(["Types_!="+t])
           
        team[i] = bestMon(tteam,ftr)
      #  print(team[i]["Name"][0],sum( calcTeamWeak(team)))
    return team 

'''
rt = newRandTeam(8)
printTeam(rt)
print(calcTeamWeak(rt))
print()
d = dex.makeDex()
ftr = dex.dexFilter(d)
ftr.filter(["Viable=TRUE","Group!Restricted","Group!Mythical","Group!Legendary","Group!Ultra Beast","Group!Mega"])
ftr.filter(["Name_!Slaking","Name_!Shedinja"])
for i in range(8):
    tteam = rt.copy()
    tteam.pop()
    f = bestMon(tteam,ftr)
    rt[i] = f
    printTeam(rt)
    print(calcTeamWeak(rt))
'''
def randImpTeam():
    rt = newRandTeam(8)
    it = None
    count = 0
    while it != rt:
        count += 1
        it = rt.copy()
        rt =improveTeam(rt)
    return rt

team = []
for m in setMons:
    team.append(d.searchMon(m))
ftr = d.dexFilter()
ftr.filter(["Viable=TRUE","Group!Restricted","Group!Mythical","Group!Legendary","Group!Ultra Beast","Group!Mega"])
ftr.filter(["Name_!Slaking","Name_!Shedinja"])
ftr.filter(["Tier!C","Tier!B"])
for i in range(5):
    f = bestMon(team,ftr)
    ftr.remove(f)
    print(f["Name"][0])