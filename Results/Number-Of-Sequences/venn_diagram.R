setwd("/Users/fg17761/OneDrive - University of Bristol/Desktop/running_metacurator/metacurator_output")

library(ggplot2)
library(ggVennDiagram)

set1 <- read.table("its2_Amplicons.tax", header=FALSE, sep="\t")
set2 <- read.table("rbcL_Amplicons.tax", header=FALSE, sep="\t")
set3 <- read.table("trnH_Amplicons.tax", header=FALSE, sep="\t")
set4 <- read.table("trnL_Amplicons.tax", header=FALSE, sep="\t")

sets <- list(A=unique(set1$V2), B=unique(set2$V2), C=unique(set3$V2), D=unique(set4$V2))

length(unique(set1$V2))
length(unique(set2$V2))
length(unique(set3$V2))
length(unique(set4$V2))

comp <- ggVennDiagram(sets, label_alpha = 0, label = "count", color = "black",
                     category.names = c("its2", "rbcL", "trnH", "trnL")) + 
  scale_fill_gradient(low = "white", high = "darkgrey")
comp


set1 <- read.table("its2_Lineages.csv", header=TRUE, sep=",")
set2 <- read.table("rbcL_Lineages.csv", header=TRUE, sep=",")
set3 <- read.table("trnH_Lineages.csv", header=TRUE, sep=",")
set4 <- read.table("trnL_Lineages.csv", header=TRUE, sep=",")

sets <- list(A=unique(set1$tax_its2), B=unique(set2$tax_rbcL), C=unique(set3$tax_trnH), D=unique(set4$tax_trnL))

comp <- ggVennDiagram(sets, label_alpha = 0, label = "count", color = "black",
                      category.names = c("its2", "rbcL", "trnH", "trnL")) + 
  scale_fill_gradient(low = "white", high = "darkgrey")
comp

length(unique(set1$tax_its2))
length(unique(set2$tax_rbcL))
length(unique(set3$tax_trnH))
length(unique(set4$tax_trnL))


#Better if we include whole genomes?

