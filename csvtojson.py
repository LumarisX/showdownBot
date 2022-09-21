import csv, json, dex
 
 
def make_json(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        headers = csvf.readline().rstrip().split(",")
        for h in headers:
            data[h]=[]
        for row in csvf:
            n = row.rstrip().split(",")
            for i in range(len(n)):
                h = headers[i]
                if n[i]!="":
                    data[h].append(n[i])
        print(json.dumps(data,indent=4))

def validate(csvFilePath):
    f = dex.dexFilter()
    f.filter(["Stats_Total<411"])
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvf.readline()
        for row in csvf:
            n = row.rstrip().split(",")
            for i in range(len(n)):
                if n[i]!="":
                    f.remove(n[i])
    f.sort("Total")
    f.printList()
        
csvFilePath = r'tiers.csv'
 
# Call the make_json function
#make_json(csvFilePath, jsonFilePath)
validate(csvFilePath)
