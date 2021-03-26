f = open("全基因组序列信息统计.txt","r")
out1 = open("全基因组序列号.txt","a")
out2 = open("全基因组物种列表.txt","a")
lines = f.readlines()
need1 = []
need2 = []
for line in lines:
    a = line.split("\t")
    b = a[1]
    c = a[2]
    need1.append(b)
    need2.append(c)
    out1.write(b+"\n")
need2 = list(set(need2))
for i in need2:
    out2.write(i+"\n")
out1.close()
out2.close()
