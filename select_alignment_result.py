import os
import re


# 统计每个物种

# 从一个文件夹提取全部的文件返回以列表形式返回所有的文件
def get_files_from_dic(dic_name):
    files_path = []
    dic_files = os.listdir(r"E:/" + dic_name)
    for file in dic_files:  # 读取到的文件夹里的文件以列表的形式储存，通过列表里的的每个文件进行for循环
        domain = os.path.abspath(r'E:' + dic_name)
        file = os.path.join(domain, file)
        files_path.append(file)
        #print(files_path)
    return files_path


# 按照指定的标注找对应的信息
def find_annotation_in_line(ann_name, line_of_doc):
    if ann_name in line_of_doc:
        return True
    return False


# 输入想要找的（marker名称，文件当前的一行，当前行的行数，文件，备用marker名）
# 输出这个文件中的marker的起始位点和结束位点
def find_gene_start_end(marker_name, line_of_doc, line_num, in_genefile, marker_name2=None):
    #print("in find_gene_start_end")
    start_ad = ""
    end_ad = ""
    # 对于matk和rbcl的文件格式,如果在传入行内形式为“gene  123..234”,则看下一行(第line_num+1行)中是否为对应的marker_name
    if find_annotation_in_line("gene", line_of_doc) and (
            marker_name.lower() == "matk" or marker_name.lower() == "rbcl"):
        # 获取“gene”的下一行“/gene = "matk"”所在的行数gene_name_line
        gene_name_line = line_num + 1
        # 获取genebank 文件中 marker的名字
        if find_annotation_in_line("/gene", in_genefile[gene_name_line]):  # 确定下一行的形式是否是所需要形式
            gene_name = re.match(r'(.*)="(.*?)"', in_genefile[gene_name_line], re.M | re.I)[2]  # 获取固定格式中“”内部的基因名称gene_name
            # print(re.match(r'(.*)="(.*?)"',line,re.M|re.I)[2])
            if gene_name.lower() == marker_name.lower():  # 对于是基因名称gene_name是输入目标基因名marker_name(matk或rbcl)的片段
                k = 0  # 用来分辨地址数字是开头还是结尾，为0是开头，1是结尾
                # 从本行(line_of_doc)获取数字
                for letter in line_of_doc:  # 对“gene 123..234”行识别每一个字符
                    if letter.isdigit() and k == 0:  # 是开头数字
                        start_ad = start_ad + letter
                        #print("start:", start_ad)
                    if letter == "." and k == 0:  # 开头数字读完
                        k = 1
                    if letter.isdigit() and k == 1:  # 是结尾数字
                        end_ad = end_ad + letter
                        #print(" end:", end_ad)

    # 对于its1和its2的文件格式,如果在传入行内形式为“misc_feature  <123..234” 或 “misc_RNA 123..234”,则看下一行(第line_num+1行)中是否为对应的marker_name
    if marker_name.lower() == "its1" or marker_name.lower() == "its2":
        if find_annotation_in_line("misc_feature", line_of_doc) or find_annotation_in_line("misc_RNA", line_of_doc):
            # 下一行的行数为gene_note_line_num
            gene_note_line_num = line_num + 1
            # 获取基因的名字gene_note
            if find_annotation_in_line("/note", in_genefile[gene_note_line_num]):
                gene_note = in_genefile[gene_note_line_num].split("/note=", 1)[1].replace("\n", " ")
            elif find_annotation_in_line("/product", in_genefile[gene_note_line_num]):
                gene_note = in_genefile[gene_note_line_num].split("/product=", 1)[1].replace("\n", " ")
            # 判断获取到的第gene_note_line_num行中gene_note是否完整，
            # 如果完整应该有2个”，
            # 如果只有1个“，那么这一行就不完整，需要继续读取之后的行的内容
            yinhao_num = gene_note.count("\"")
            if yinhao_num != 2:
                j = gene_note_line_num  # j=i记录i的本次循环真正的值，以便之后恢复i取值，准确记录行数
                print("note_pre:", gene_note)
                while 1:
                    if find_annotation_in_line("\"", in_genefile[gene_note_line_num + 1]):
                        gene_note = gene_note + in_genefile[gene_note_line_num + 1].replace("\n", " ").replace(
                            "                     ", "")
                        break
                    else:
                        gene_note = gene_note + in_genefile[gene_note_line_num + 1].replace("\n", " ").replace(
                            "                     ", "")
                        gene_note_line_num = gene_note_line_num + 1
                gene_note_line_num = j  # i=j恢复i在本次循环中原本的行数值
            print("note:", gene_note)
            # 如果gene_note和需要的marker_name中的一个相同
            if (marker_name.lower() in gene_note.lower()) or (marker_name2.lower() in gene_note.lower()):  # 对于是基因marker的片段
                k = 0  # 用来分辨地址数字是开头还是结尾，为0是开头，1是结尾
                for letter in line_of_doc:  # 获取位置数字
                    if letter.isdigit() and k == 0:
                        start_ad = start_ad + letter
                        print("start:", start_ad)
                    if letter == "." and k == 0:
                        k = 1
                    if letter.isdigit() and k == 1:
                        end_ad = end_ad + letter
                        print(" end:", end_ad)

    # 对于trnt-trnl和atpb-rbcl的文件格式,如果在传入行内形式为“gene  123..234”,则看下一行(第line_num+1行)中是否为对应的marker_name
    if marker_name.lower() == "trnt-trnl" or marker_name.lower() == "atpb-rbcl":
        #print("file is atpb-rbcl or trnt-trnl")
        if find_annotation_in_line("misc_feature", line_of_doc):
            gene_note_line_num = line_num + 1
            if find_annotation_in_line("/note", in_genefile[gene_note_line_num]):  # 获取基因marker的名字,注释
                gene_note = in_genefile[gene_note_line_num].split("/note=", 1)[1].replace("\n", " ")
                print("note:", gene_note)
                if marker_name.lower() in gene_note.lower():  # 对于是基因的片段
                    k = 0  # 用来分辨地址数字是开头还是结尾，为0是开头，1是结尾
                    for letter in line_of_doc:  # 获取位置数字
                        if letter.isdigit() and k == 0:
                            start_ad = start_ad + letter
                            print("start:", start_ad)
                        if letter == "." and k == 0:
                            k = 1
                        if letter.isdigit() and k == 1:
                            end_ad = end_ad + letter
                            print(" end:", end_ad)
    if start_ad != "" and end_ad != "":
        return [int(start_ad),int(end_ad)]


# 提取文件对应的genebank编号
def find_accession_num(line_of_doc):
    if find_annotation_in_line("ACCESSION", line_of_doc):
        accession_no = line_of_doc.split("ACCESSION   ", 1)[1].replace("\n", " ")
        #print(accession_no)
        return accession_no


# 提取文件对应物种
def find_organism(line_of_doc):
    if find_annotation_in_line("ORGANISM", line_of_doc):
        organism = line_of_doc.split("  ORGANISM  ", 1)[1].replace("\n", " ")
        return organism


# 计算序列长度
def calculate_gene_lenth(start_end):
    start = start_end[0]
    end = start_end[1]
    lenth = end - start + 1
    return lenth


# 以accession no.为名称建立类，该accession对应的物种，序列长度为属性
class Sequence:
    def __init__(self, accesion_num, specie, sequence_lenth):
        self.accession_num = accesion_num
        self.specie = specie
        self.lenth = sequence_lenth


#
def get_all_sequences(dic_name, marker_name, marker_name2=None):
    files_path = get_files_from_dic(dic_name)
    sequences = []
    for path in files_path:
        file = open(path, 'r')
        file_lines = file.readlines()
        line_of_doc_num = 0
        accession = None
        organism = None
        while line_of_doc_num < len(file_lines):
            line = file_lines[line_of_doc_num]
            if accession is None:
                accession = find_accession_num(line)
            if organism is None:
                organism = find_organism(line)
            #print("accession:", accession)
            if find_gene_start_end(marker_name, line, line_of_doc_num, file_lines, marker_name2) is not None:
                #print("line_num:" , line_of_doc_num)
                lenth = calculate_gene_lenth(find_gene_start_end(marker_name, line, line_of_doc_num, file_lines, marker_name2))
            line_of_doc_num += 1
        sequence = Sequence(accession, organism, lenth)
        sequences.append(sequence)
    return sequences


# 对物种字典进行处理，对指定物种的选择指定排位序列, 并输出【out_seq_list】作为所有挑选出来的序列的列表
# 输入species【字典】，changes{chage_specie【要改变序列的物种】:change_times【要改变该物种序列的次数】}
# 在调换时要【注意】如果已经用的是最小的序列，即输入的调换的次数大于该物种包含的序列数-1，则需要程序提醒已经没有可以调换的序列
def diction_to_list(species, changes):
    # 以[(key1,value1),(key2,value2)]的形式返回字典内容
    species_list = species.items()
    out_seq_list = []
    for specie in species_list:
        # specie[0]是该物种的物种名，specie[1]是该物种对应的所有序列的列表，
        # changes[specie[0]]是在输入的变动字典中与物种对应的变动次数
        if specie[0] in changes:  # 如果该物种在需要变动的物种字典中
            if changes[specie[0]] <= len(specie[1]) - 1:
                seq_of_specie = specie[1][changes[specie[0]]]
                out_seq_list.append(seq_of_specie)
            elif changes[specie[0]] > len(specie[1]) - 1:
                print("调换次数超出物种%s的序列数" % specie[0])
        out_seq_list.append(specie[1][0])  # 如果该物种不在需要变动的物种字典中，直接使用物种对应的序列列表的第一位。
    return out_seq_list


# 下一步根据输入的要调换的物种和调换次数，使用函数【dection_to_list】,得到所有需要挑选出来的序列列表【out_seq_list】
# 使用【out_seq_list】从比对后的fasta文件中挑选输出所有要使用的序列
# 写入一个新的fasta文件，xxx_select.fasta
def get_need_sequence_from_fasta(seq_accession_nums, seq_species, fasta_align_file_path, marker_name):
    #print(seq_accession_nums)
    fasta_file = open(fasta_align_file_path, "r")
    fasta_select_file = open(marker_name + "_select.fasta", "a")
    fasta_align_lines = fasta_file.readlines()
    now_hang = 0
    for line in fasta_align_lines:
        j = now_hang
        if line[0] == ">":
            if line[1:9]+" " in seq_accession_nums:
                #print(line[1:9])
                num_specie_of_line = seq_accession_nums.index(line[1:9]+" ")
                fasta_select_file.write(">"+seq_species[num_specie_of_line]+"\n")
                now_hang += 1
                while fasta_align_lines[now_hang][0] != ">":
                    fasta_select_file.write(fasta_align_lines[now_hang])
                    if now_hang < len(fasta_align_lines)-1:
                        now_hang += 1
                    elif now_hang == len(fasta_align_lines)-1:
                        break
        now_hang = j
        now_hang += 1


def main(dic_name, marker_name, marker_name2=None, changes={}, fasta_align_file_path=""):
    sequences = get_all_sequences(dic_name, marker_name, marker_name2)
    species = {}  # 记录物种数目
    for sequence in sequences:
        if not (sequence.specie in species):
            # 如果是新出现的物种，就创建一个新的物种字典键，并给该键赋值一个包含这个序列的序列类列表
            #print(sequence.specie)
            species_seq = [sequence]
            specie = sequence.specie
            species[specie] = species_seq
        elif sequence.specie in species:
            # 如果是已经归入物种字典中的物种，则向该键对应的序列类列表中添加这一新的序列
            species[sequence.specie].append(sequence)

    # 以上完成了对序列的物种归类
    # 下一步进行对每个物种内序列长度的排序
    for key in species:
        seq_list = species[key]
        out_seq_list = []
        while len(seq_list) > 0:
            # 持续循环，每次选出最长的序列加入out_seq_list，然后从原列表中删除加入out的序列，直到原列表为空结束循环
            longest = 0
            for seq in seq_list:
                if seq.lenth > longest:
                    longest = seq.lenth
            # 此时longest记录了这些序列中最长的序列的长度
            for seq in seq_list:
                if seq.lenth == longest:
                    out_seq_list.append(seq)
                    seq_index = seq_list.index(seq)
                    seq_list.pop(seq_index)
        # 得到的out_seq_list是从大到小的序列列表
        # 把顺序排列的序列列表赋值给对应的物种的键
        species[key] = out_seq_list

    # 完成了对所有序列的排列
    out_seqs = diction_to_list(species, changes)
    seq_accession_nums = []
    seq_species = []
    # 获取所有要使用的序列的登录号列表seq_accession_num
    for i in out_seqs:
        seq_accession_nums.append(i.accession_num)
        seq_species.append(i.specie)
    # 下一步根据输入的要调换的物种和调换次数，从比对后的fasta文件中挑选输出所有要使用的序列
    # 写入一个新的fasta文件，xxx_select.fasta
    get_need_sequence_from_fasta(seq_accession_nums,seq_species, fasta_align_file_path, marker_name)

    # 输出过程文件，输出所有使用的序列的登录号，并记录调换过的物种和调换的次数（第几长的序列）
    out_log_file = open("log_file.txt", "a")
    out_log_file.write("#########本次挑选中进行调换的物种及次数##########\n")
    for key in changes:
        out_log_file.write(key + ":被调换了" + str(changes[key]) + "次\n")
    out_log_file.write("#########本次挑选出来的序列登录号##########\n")
    for i in seq_accession_nums:
        out_log_file.write(str(i) + "\n")

main("phylosuite/GenBank_File/files/.data/atpb-rbcl","atpb-rbcl",None,{},"atpb_rbcl_alignmentresult.fasta")
#main("phylosuite/GenBank_File/files/.data/rbcl","rbcl",None,{},"rbcl_mafft.fasta")
#main("phylosuite/GenBank_File/files/.data/matk","matk",None,{},"matk_mafft.fasta")
