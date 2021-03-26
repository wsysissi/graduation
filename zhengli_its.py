import re
import os

def get_all_file(parent_dic_name , marker_name1 , marker_name2):
    parent_dic = os.listdir(r'E:'+parent_dic_name)#(r'文件夹路径E:xxx')
    out_complete_wuzhongming = open("叶绿体全基因组的物种名汇集.txt","a")
    out_complete_wuzhongming.write("title"+"\t"+"accession_no"+"\t"+"organism"+"\t"+"family"+"\t"+"start_ad"+"\t"+"end_ad"+"\t"+"lenth"+"\t"+"note"+"\n")
    for file in parent_dic:  #读取到的文件夹里的文件以列表的形式储存，通过列表里的的每个文件进行for循环
        domain = os.path.abspath(r'E:'+parent_dic_name)
        file = os.path.join(domain,file)
        inputfile = open(file,'r')
        #out_complete_wuzhongming = open("叶绿体全基因组的物种名汇集.txt","a")
        #out_complete_wuzhongming.write("title"+"\t"+"accession_no"+"\t"+"organism"+"\t"+"family"+"\t"+"start_ad"+"\t"+"end_ad"+"\t"+"lenth"+"\n")
        in_genefile = inputfile.readlines()#使用oython文件操作读入基因文件，并按行储存在列表的数据格式中
        i = 0
        start_ad = ""
        end_ad = ""
        for line in in_genefile:#逐行扫描寻找基因文件中需要的字段，提取关键信息
            if "DEFINITION" in line:#判断文件是否为叶绿体全基因组文件，如果是全基因组的文件就跳过操作。也可以通过文件大小在外部判断，转移到其他文件夹里。
                deff = line.replace("\n"," ")
                j = i #记录i的本次循环真正的值，以便之后恢复i取值，准确记录行数
                while ("ACCESSION" not in in_genefile[i+1]):
                    deff = deff + in_genefile[i+1].replace("\n"," ").replace("            "," ")
                    i = i+1
                i = j#恢复i在本次循环中原本的行数值
                if ("complete genome" in deff) and ("chloroplast" in deff) :
                    break
                else:
                    title = deff.split("DEFINITION ",1)[1]
                    print(title)
            if "VERSION" in line :
                title = line.split("VERSION     ",1)[1].replace("\n"," ") + title.replace("\n"," ")
                print("title:" , title)
            if "ACCESSION" in line:
                accession_no = line.split("ACCESSION   ",1)[1].replace("\n"," ")
                print("accession_no:" , accession_no)
            if "ORGANISM" in line :
                organism = line.split("  ORGANISM  ",1)[1].replace("\n"," ")
                print("organism:" , organism)
            if "/Family" in line:
                family = re.match(r'.*/Family="(.*?)"',line,re.M|re.I)[1].replace("\n"," ")
                print("family:" , family)
            if ("misc_feature" in line) or ("misc_RNA" in line):
                gene_note_line = i+1
                if ("/note" in in_genefile[gene_note_line]) : #or ("/product" in in_genefile[gene_note_line] ): #获取基因marker的名字,注释
                    gene_note = in_genefile[gene_note_line].split("/note=",1)[1].replace("\n"," ")#re.match(r'(.*)="(.*?)',in_genefile[gene_note_line],re.M|re.I)[2]
                elif ("/product" in in_genefile[gene_note_line] ) :
                    gene_note = in_genefile[gene_note_line].split("/product=",1)[1].replace("\n"," ")
                yinhao_num = gene_note.count("\"")
                if yinhao_num != 2 :
                    j = gene_note_line #j=i记录i的本次循环真正的值，以便之后恢复i取值，准确记录行数
                    print("note_pre:",gene_note)
                    while 1:
                        if "\"" in in_genefile[gene_note_line+1]:
                            gene_note = gene_note + in_genefile[gene_note_line+1].replace("\n"," ").replace("                     ","")
                            break
                        else:
                            gene_note = gene_note + in_genefile[gene_note_line+1].replace("\n"," ").replace("                     ","")
                            gene_note_line = gene_note_line+1
                    gene_note_line = j #i=j恢复i在本次循环中原本的行数值
                print("note:",gene_note)
                if (marker_name1.lower() in gene_note.lower()) or (marker_name2.lower() in gene_note.lower()) :#对于是基因marker的片段
                    k=0#用来分辨地址数字是开头还是结尾，为0是开头，1是结尾
                    flag=0#用来标记下面单行循环中光标的位置
                    for letter in line:#获取位置数字
                        if letter.isdigit() and k==0:
                            start_ad = start_ad + letter
                            print("start:" , start_ad)
                        if letter == "." and k==0 :
                            k = 1
                        if letter.isdigit() and k==1:
                            end_ad = end_ad + letter
                            print(" end:" , end_ad)
                            
            i = i+1
        if (end_ad != "") and (start_ad != ""):
            lenth = str(int(end_ad) - int(start_ad) + 1)
            print("lenth:" , lenth)
            out_complete_wuzhongming.write(title+"\t"+accession_no+"\t"+organism+"\t"+family+"\t"+start_ad+"\t"+end_ad+"\t"+lenth
                                       +"\t"+gene_note+"\n")
        inputfile.close()
    out_complete_wuzhongming.close()
