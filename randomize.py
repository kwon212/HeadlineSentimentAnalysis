

#f = open("sentimenttweets.txt")
#for line in f:


import random

r = open("sentimenttweets_random.txt","w")

with open("sentimenttweets.txt") as f:
    lines = list(f)

random.shuffle(lines)
for l in lines:
    r.write(l)


r.close()
