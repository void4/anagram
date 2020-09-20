import json

with open("verbs-conjugations.json") as f:
    j = json.loads(f.read())

f = open("verbs-participle.txt", "w+")

for v in j:
    if "participle" in v:
        f.write(v["participle"][0]+"\n")

f.close()
