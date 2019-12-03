library('reticulate')
library(hash)
library(Matrix)
use_python("/usr/local/bin/python")
setwd('~')
source_python('hash_table.py')



hash_table_sparse_matrix=function(i,j,value,dime){
  index=paste(as.character(i),as.character(j),sep=",")
  h=hash(index,value)
  .set(h,"posi"=index)
  .set(h,"dime"=dime)
  .set(h, 'i'=i)
  .set(h, 'j'=j)
  .set(h, 'value'=value)
  return (h)
}

convert_hash=function(h){
  dime=h[["dime"]]$dime
  index=paste(as.character(rep(1:dime[1],dime[2])),as.character(rep(1:dime[2],each=dime[1])),sep=",")
  array=has.key(index,h)
  int_ar=as.integer(array)
  mat=matrix(int_ar,nrow=dime[1],ncol=dime[2])
  position=which(mat==1)
  a=position%%dime[1]
  ind=paste(as.character(ifelse(a==0,dime[1],a)),as.character(ceiling(position/dime[1])),sep=",")
  mat[position]=values(h,ind)
  return (mat)
}

plus=function(h1,h2){
  posi1=h1[["posi"]]$posi
  posi2=h2[["posi"]]$posi
  h3=setRefClass('hash',fields=keys(h2),contains=hash::values(h2))
  haskey=has.key(posi1,h2)
  value=values(h1,posi1)
  pos=which(haskey)
  value[pos]=value[pos]+values(h2,posi1[pos])
  .set(h3,posi1,value)
  return (h3)
}

#Rewrite using for loop in c++

#will be square matrix
multiply_hash=function(h1,h2){ #h1 = h2
  h1=hash_matrix(i=h1$i$i, j=h1$j$j, value=h1$value$value, dims=h1$dime$dime)
  h2=hash_matrix(i=h2$i$i, j=h2$j$j, value=h2$value$value, dims=h2$dime$dime)
  h3=multiply(h1,h2)
  #h3=hash_table_sparse_matrix(i=h3$r,j=h3$c,value=h3$val, dime=h3$dims)
  return(h3)
}

args=commandArgs(trailingOnly=T)
#cat(seq(1e4,1e5, by=1000), file='sample_sizes.txt')
k_full=as.numeric(args[1])
k_sample=as.numeric(scan(args[2]))

i=sample(1:k_full,max(k_sample))
j=sample(1:k_full,max(k_sample))
x=rnorm(max(k_sample))
dime=c(k_full,k_full)
hash_times=sapply(k_sample, function(m){
  h=hash_table_sparse_matrix(i=i[1:m],j=j[1:m],value=x[1:m],dime=dime)
  start.time <- Sys.time()
  h=multiply_hash(h,h)
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  size=object.size(h, units='kB')
  return(c('time'=time.taken,'size (kB)'=size))
  }
)
sparse_times=sapply(k_sample, function(m){
  start.time <- Sys.time()
  s=sparseMatrix(i=i[1:m],j=j[1:m],x=x[1:m],dims=dime)
  s=s%*%s
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  size=object.size(h, units='kB')
  return(c('time'=time.taken,'size (kB)'=size))
}
)
colnames(hash_times)=k_sample
colnames(sparse_times)=k_sample
write.table(hash_times, file='hash_times.tsv', sep='\t')
write.table(sparse_times, file='sparse_times.tsv', sep='\t')
