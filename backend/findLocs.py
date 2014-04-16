
#Read file in
f = open("../data/welsh-hist.txt", 'r')
line = f.readline()
searches = []
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

            #save into dict for that location
            searches.append([term, addr, freq])

            #Onto the next one!
            line = f.readline()
            words = line.split()
            pass
    line = f.readline()
print searches #TODO: Right now this is an array of arrays of the form [search term, address, frequency]
#Create json representing circle objects and print to file that javascript can read in
