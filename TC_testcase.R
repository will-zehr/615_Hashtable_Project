library('reticulate')
library(hash)
library(Matrix)
library(nem)
use_python("/usr/local/bin/python")
setwd('~/Desktop/2019fall/biostat615/project/')
source_python('hash_matrix_transitive_closure.py',convert = F)
#transitive closure

##designed
i=c()
j=c()
dims=c(10000,10000)
for (k in 1:100){
  ind=sample(1:100,2,replace = T)
  i=c(i,sample(((ind[1]-1)*100+1):(ind[1]*100),300,replace = T))
  j=c(j,sample(((ind[2]-1)*100+1):(ind[2]*100),300,replace = T))
}
value=rep(1,length(i))

kara=hash_matrix(i,j,dims=dims)
kara=transitive_closure(kara)

kara_adj=sparseMatrix(i,j,x=value,dims=dims)
kara_adj=as.matrix(kara_adj)
tc=transitive.closure(kara_adj,mat=T)
