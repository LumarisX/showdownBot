import dex, json

m = dex.searchMove("surging-strikes")
m["value"]=112.5

with open("moves.json","w") as f:
    print(json.dumps(dex.ml,indent=4),file=f)