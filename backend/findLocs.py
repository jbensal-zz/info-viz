#!/bin/python2

from whodat import whodat
import json
#Read file in
f = open("../data/jay_raw.txt", 'r')
line = f.readline()
searches = {}
locations = {}
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
            if addr in locations:
                loc = locations[addr]
            else:
                loc = whodat(addr)
                locations[addr] = loc
            #save into dict for that location
            if loc != None:
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
objs = []
#Create json representing circle objects and print to file that javascript can read in
for key, val in searches.iteritems():
    (name, freq) = val
    (lat, lng) = key
    d = {}
    d["name"] = name
    d["latitude"] = lat
    d["longitude"] = lng
    d["radius"] = freq
    d["fillKey"] = 'bcolor'
    objs.append(d)

with open("jay.json", 'w') as f:
    json.dump(objs, f)
