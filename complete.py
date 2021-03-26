import re
import os

def get_all_file(parent_dic_name):
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
            
        out_complete_wuzhongming.write(title+"\t"+accession_no+"\t"+organism+"\t"+family+"\n")
        inputfile.close()
    out_complete_wuzhongming.close()
