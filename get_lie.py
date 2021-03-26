import codecs

def get_clum (file_name,clum_num):
    in_file = codecs.open(file_name,mode="r",encoding="GB2312")
    file = in_file.readlines()
    need_clum = []
    for line in file:
        a = line.split("\t")
        b = a[clum_num-1]
        need_clum.append(b)
    in_file.close()
    return need_clum

def qu_chong (organism_list):
    out = list(set(organism_list))
    out.sort(key=organism_list.index)
    return len(out)-1

