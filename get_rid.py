def get_rid(file,char):
    f = open(file,"r")
    outf = open(file +"rid.txt","a")
    lines = f.readlines()
    for line in lines:
        if char not in line:
            outf.write(line)
        elif char in line:
            outline1 = line.split(char,1)[0]
            outline2 = line.split(char,1)[1]
            outline = outline1 + outline2
            outf.write(outline)
    f.close()
    outf.close()
