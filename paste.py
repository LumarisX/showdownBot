
import battle

def export(team):
    for mon in team:
        name = mon.name
        form = mon.form["Name"][0]
        if name!=form:
            name = name + " ("+form+")"
        if mon.item!=None:
            name = name+" @"+ str(mon.item)
        print(name)
        if mon.ability!=None:
            print("Ability: "+mon.ability)
        if mon.level!=100:
            print("Level: "+mon.level)
        nzstat=[]
        for stat in mon.evs:
            if mon.evs[stat]>0:
                nzstat.append(mon.evs[stat]+" "+ stat)
        if len(nzstat)>0:
            print("EV: "+" / ".join(nzstat))
        for m in mon.moves:
            print("-"+m)
        print()
    
    print()
    
    
    
    '''
Cosmoem  
Ability: Sturdy  
Level: 50  
EVs: 252 HP / 252 SpD / 4 Spe  
Careful Nature  
IVs: 0 Atk  
- Teleport  
- Cosmic Power  
- Splash
    '''