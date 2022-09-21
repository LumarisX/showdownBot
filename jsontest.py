import json, damagecalc

def makeforms():
    k = [0]*898
    for i in range(898):
        k[i] = {"Form":[]}
    
    for i in j:
        e = j[i]
        n = int(e["Dex. No."])-1
        k[n]["Form"].append(e)
    return k

def delkey(s):
    for i in j:
        del j[i]["Form"][s]
        
def searchMon(name):
    for e in j:
        for o in e["Form"]:
            for n in o["Name"]:
                if n == name:
                    return name
    print(name)
    return searchMon(input("Alternate Name: "))
                    
def manRef(s=None):
    if s != None:
        print(s)
    dex = 0
    while dex<1 or dex > len(j)+1:
        dex = input("Dex No:")
        if dex == "s":
            return None
        dex =int(dex)-1
    e = j[dex]
    l = len(e["Form"])
    for n in range(0, l):
        print(n+1, e["Form"][n])
    fn = -1
    while fn < 0 or fn>=l:
        fn = int(input("Form No:"))-1
    form = e["Form"][fn]
    if s!=None:
        form["Name"].append(s)
    return(form)
    
with open("CPN.json", 'r') as f:
    j= json.load(f)

del j[891]["Form"][1]["Types"][1]

with open("CPN.json",'w') as f:
    print(json.dumps(j,indent=4),file = f)
