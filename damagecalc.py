import math, battle, dex, json

def calc(mD, mA, move, targets=1,crit=False, screen=False):
    atk, df = statCat(move["damage_class"])
    atk = mA.stat(atk)
    df = mD.stat(df)
    #BP modifiers
    bp = move["power"]
    bp = pokeRound(bp*mA.bpm)
    d = (math.floor(2*mA.level/5)+2)*bp*atk
    d = math.floor(d/df)
    d = math.floor(d/50) +2
    d = pokeRound(d*targets)
    d = pokeRound(d*(3 if crit else 2)/2)
    d = [math.floor(x*d/100) for x in range(85,101)]
    #Stab
    if move["type"] in mA.form["Types"]:    #STAB
        d = [pokeRound(x*1.5) for x in d]
    #Types
    d = [pokeRound(x*dex.getWeak(mD.form["Types"],move["type"])) for x in d]
    #Burn
    if mA.status == "burn":
        d=[pokeRound(x*.5) for x in d]
    #Screen
    if screen:
        d=[pokeRound((x*.5)/targets) for x in d]
    return d
    
def pokeRound(n):
    if n%.5 ==0:
        return math.floor(n)
    else:
        return round(n)

def getStatSpread(baseStat, level=100,nature=1, isHp=False):
    list = [0]*64
    for i in range(64):
        if isHp:
            list[i] = hp(baseStat, level, evs=i*4)
        else:
            list[i] = stat(baseStat, level,nature=nature,evs=i*4)
    return list
    
def statCat(moveCat):
    if moveCat =="physical":
        atk = "Atk"
        df = "Def"
    elif moveCat == "special":
        atk = "Sp. Atk"
        df = "Sp. Def"
    else:
        return None
    return atk,df
    
def allEvs(mD, mA, move):
    atk, df = statCat(move["damage_class"])
    evs = {}
    for i in range(0,256,4):
        mD.setEv("HP",i)
        for j in range(0,256,4):
            mD.setEv(df,j)
            s = calc(mD,mA,move)
            s = s[15]+1
            if s==1:
                return "Immune"
            h = mD.stat("HP")
            w = math.floor(h/s)
            total = j+i
            if w not in evs:
                evs[w]=[]
            add = True
            n =0
            while n < len(evs[w]) and add:
                a,b,t = evs[w][n]
                n+=1
                if a <=i and b <=j:
                    add = False
            if add:
                n=0
                while n < len(evs[w]) and total > sum(evs[w][n]):
                    n+=1
                evs[w].insert(n,(i,j,i+j))
    return evs
    
def atkEvs(mD, mA, move):
    atk, df = statCat(move["damage_class"])
    evs = {}
    for i in range(0,256,4):
        mA.setEv(atk,i)
        s = calc(mD,mA,move)
        s = s[15]+1
        if s==1:
            return "Immune"
        h = mD.stat("HP")
        w = math.floor(h/s)+1
        if w not in evs or i < evs[w]:
            evs[w]=i
    return evs
        
def minEvs(evs):
    if evs != "Immune":
        for e in evs:
            evs[e]=evs[e][0]
    return evs

def allMoves(mD,mA,dclass=None):
   moves = {}
   for m in mA.form["Learnset"]:
       m = dex.searchMove(m)
       if (m["damage_class"] == dclass or dclass ==None) and m["power"] != 0:
            moves[m["name"]] = minEvs(allEvs(mD,mA,m))
   return moves
           
def allAtkMoves(mD,mA,dclass=None,top=0):
   moves = {}
   for m in mA.form["Learnset"]:
       m = dex.searchMove(m)
       if (m["damage_class"] == dclass or dclass ==None) and m["power"] != 0:
           moves[m["name"]] = atkEvs(mD,mA,m)
   if top>0:
       t = []
       for m in moves:
           if moves[m]=="Immune":
               continue
           s = min(moves[m].keys())
           p=0
           for i in range(len(t)):
               ko = t[i][1]
               if s > ko:
                   p=i+1
               if s == ko and moves[m][s]>t[i][2]:
                   p=i+1
           t.insert(p,(m,s,moves[m][s]))
           if len(t) > top:
               t.pop(len(t)-1)
       tmp = {}
       for i in range(len(t)):
           tmp[t[i][0]] = moves[t[i][0]]
       moves = tmp
   return moves
   
def teamAtk(mD, tA, top=0, level=100, nature=1, item=1, evs={"HP":0,"Atk":252,"Def":0,"Sp. Atk":252,"Sp. Def":0,"Spe":0}):
    print("Against " + mD.name)
    print()
    for mA in tA:
        mA = battle.mon(mA,level=level, nature=nature, item=item)
        print(mA.name)
        moves = allAtkMoves(mD,mA,top=top)
        for m in moves:
            s = min(moves[m].keys())
            print("{0}\t{1}\t{2}".format(m,s,moves[m][s]))
        print()
        
def teamSpread(tD, mA, dclass, level=100, item=1):
    for mD in tD:
        mD = battle.mon(mD,level=level,item=item)
        print(mD.name)
        moves = allMoves(mD,mA,dclass)
        for m in moves:
            s = min(moves[m])
            print("{0}\t{1}\t{2}".format(m,s,moves[m][s]))
        print()
           
def guessAtk(mD,mA,move,damage):
    atk, df = statCat(move["damage_class"])
    tmA = copy(mA)
    for item in [1,1.2,1.5]:
        tmA.item = item
        for nature in [1,1.1,0.9]:
           tmA.nature = nature
           for i in range(mA.evs[atk], min(510-mA.totalEv(),252),4):
               tmA.setEv(atk,i)
               s = calc(tmA,mD,move)
               print(item, nature, s)
 
def printMoves(string):
    print(json.dumps(string,indent=4))          
           
mD = battle.mon("Kartana", level=100,nature=1,item=1,evs={"HP":252,"Atk":0,"Def":252,"Sp. Atk":128,"Sp. Def":252,"Spe":0})
mA = battle.mon("Scyther", level=100, nature=1.1, item=1.5,bpm=1.5,evs={"HP":252,"Atk":252,"Def":252,"Sp. Atk":252,"Sp. Def":252,"Spe":0})
tD=["Ponyta-Galar","Shiinotic","Houndour","Stufful","Sandshrew-Alola","Phanpy","Flaaffy","Drifloon","Wailmer","Caterpie"]
tA=["Servine","Ponyta","Omanyte","Meditite","Cufant","Corvisquire","Cleffa","Vibrava","Minun","Wooloo","Bounsweet"]
#allMoves(mD,mA,"special")
m = dex.searchMove("Vacuum-Wave")
print(calc(mD,mA,m))
print(allEvs(mD,mA,m))
#print(allMoves(mD,mA,dclass="special"))
#print(teamAtk(mD,tA,top=4,nature=1,item=1.3))
#print(teamSpread(tDt,mA,"special",item=1.5))
#fullMonSpread(mD,mA)