library(vioplot)
p1 = read.table("C:\\Users\\wangsiyi\\Desktop\\matk序列信息统计.txtrid.txt",head=T,sep="\t")
matk <- p1[,7]
p2 = read.table("C:\\Users\\wangsiyi\\Desktop\\rbcl序列信息统计.txt",head=T,sep="\t")
rbcl <- p2[,7]
p3 = read.table("C:\\Users\\wangsiyi\\Desktop\\atpb-rbcl序列信息统计.txt",head=T,sep="\t")
atpb_rbcl <- p3[,7]
p4 = read.table("C:\\Users\\wangsiyi\\Desktop\\trnt-trnl序列信息统计.txt",head=T,sep="\t")
trnt_trnl <- p4[,7]
p5 = read.table("C:\\Users\\wangsiyi\\Desktop\\its1序列信息统计.txt",head=T,sep="\t")
its1 <- p5[,7]
p6 = read.table("C:\\Users\\wangsiyi\\Desktop\\its2序列信息统计.txtrid.txt",head=T,sep="\t" )
its2 <- p6[,7]
vioplot(matk,rbcl,atpb_rbcl,trnt_trnl,its1,its2,names = c("matk","rbcl","atpb_rbcl","trnt_trnl","its1","its2"))
title("序列长度统计" , ylab = "序列长度" , xlab="序列名")
