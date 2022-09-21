import csv, json

n = ["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"," Null","Dry Skin","Flash Fire","Levitate","Lightning Rod","Sap Sipper","Water Bubble","Wonder Guard","Motor Drive","Storm Drain","Water Absorb","Thick Fat","Volt Absorb","Heatproof"]

chart={}
for i in n:
    chart[i] = {}
with open("typechart.csv", encoding='utf-8') as f:
        i=0
        for rows in f:
            if i<32:
                r = rows.strip().split(",")
                for j in range(len(r)):
                    chart[n[i]][n[j]] = r[j]
                i = i+1
with open("typechart.json", "w") as f:
    print(json.dumps(chart, indent=4),file = f)
            