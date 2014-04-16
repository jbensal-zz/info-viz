from whodat import whodat
import json
#Read file in
f = open("../data/jay_raw.txt", 'r')
line = f.readline()
searches = {}
while len(line)>0:
    words = line.split()
    if len(words)>0 and words[0] == "Searched":
        term = " ".join(words[2:-1])
        line = f.readline()
        words = line.split()
        while len(words)>0:
            #parse out address and frequency
            if words[-2] == "times":
                freq = int(words[-3])
                addr = words[-6]
            else:
                freq = 1
                addr = words[-2]
            #find physical location for the address
            loc = whodat(addr)
            #save into dict for that location
            if loc in searches:
                names, priorfreq = searches[loc]
                searches[loc] = (names+'\n'+term, freq+priorfreq)
            searches[loc] = (term, freq)

            #Onto the next one!
            line = f.readline()
            words = line.split()
            pass
    line = f.readline()
f.close()
f = open("jay.json", 'w')
f.write(json.dump(searches))
f.close()
#Create json representing circle objects and print to file that javascript can read in
