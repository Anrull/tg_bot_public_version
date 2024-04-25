import json

with open("dicts/dict.json") as js:
    tabel = json.load(js)

# print(tabel)
list_classes = ["11B", "11A", "10B", "10A", "9B", "9A", "8B", "8A", "7C", "7B", "7A", "6B", "6A"]
set_sub = set()
    
for i in range(2):
    for j in list_classes:
        for n in range(5):
            for k in tabel[str(i)][j][str(n)]:
                sub = k[0]
                if "/" in sub:
                    for l in sub.split("/"):
                        set_sub.add(l)
                else:
                    set_sub.add(sub)

print(list(set_sub))