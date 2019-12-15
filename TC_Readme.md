# Step 1: Load packages, functions
```R
library('reticulate')
library(hash)
library(Matrix)
use_python("/usr/local/bin/python")
setwd('~')
source_python('hash_table.py',convert=F)



hash_table_sparse_matrix=function(i,j,value,dime){
  index=paste(as.character(i),as.character(j),sep=",")
  h=hash(index,value)
  .set(h,"dime"=dime); .set(h, 'i'=i); .set(h, 'j'=j); .set(h, 'value'=value)
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


multiply_hash=function(h1,h2, convert_to_r=FALSE){ #h1 = h2
  h1=hash_matrix(i=h1$i$i, j=h1$j$j, value=h1$value$value, dims=h1$dime$dime)
  h2=hash_matrix(i=h2$i$i, j=h2$j$j, value=h2$value$value, dims=h2$dime$dime)
  h_mult=multiply(h1,h2)
  if (convert_to_r==TRUE){
    h_mult=hash_py_to_r(h_mult)
    }
  return(h_mult)
}


hash_py_to_r=function(h){
  h=py_to_r(h)
  h=unlist(h)
  dime=h[c('dims1','dims2')]
  vals=h[names(h)!='dims1' & names(h)!='dims2']
  n=length(h)
  j=names(h)
  j=j[j!='dims1' & j!='dims2']
  i=j
  j=sapply(j, function(x) unlist(strsplit(x,"[.]")))[1,]
  i=sapply(i, function(x) unlist(strsplit(x,"[.]")))[2,]
  i=as.numeric(i)
  j=as.numeric(j)
  h=hash_table_sparse_matrix(i=i,j=j,value=vals,dime=dime)
  return(h)
}
```

#Step 2: Read in command args

Want full dimension size, how many nonzero elements to sample

```R
args=commandArgs(trailingOnly=T)
k_full=as.numeric(args[1])
k_sample=as.numeric(scan(args[2]))
```

#Step 3: Set up evaluation functions

```R
hash_time=function(m){
  h=hash_table_sparse_matrix(i=i[1:m],j=j[1:m],value=x[1:m],dime=dime)
  start.time <- Sys.time()
  h=multiply_hash(h,h)
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  size=reticulate::py_to_r(hash_size(h))
  return(c('time'=time.taken,'size'=size))
  }

sparse_time1=function(m){
  s=new("dgTMatrix",
        i = as.integer(i[1:m]-1),
        j = as.integer(j[1:m]-1), 
        x=x[1:m], 
        Dim=as.integer(dime))
  start.time <- Sys.time()
  s=s%*%s
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  size=object.size(s)
  return(c('time'=time.taken,'size'=size))
}


sparse_time2=function(m){
  s=sparseMatrix(i=i[1:m],j=j[1:m],x=x[1:m],dims=dime)
  start.time <- Sys.time()
  s=s%*%s
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  size=object.size(s)
  return(c('time'=time.taken,'size'=size))
}
```
# Step 4: Run under each scenario
```R
i=sample(1:k_full,max(k_sample))
j=sample(1:k_full,max(k_sample))
x=rnorm(max(k_sample))
dime=c(k_full,k_full)

cat('-----------------\n')
cat('Random running\n')
cat('-----------------\n')

hash_times_random=sapply(k_sample, hash_time)

cat('hash done\n')

sparse_times_random1=sapply(k_sample, sparse_time1)
sparse_times_random2=sapply(k_sample, sparse_time2)

cat('sparse done\n')

colnames(hash_times_random)=k_sample
colnames(sparse_times_random1)=k_sample
colnames(sparse_times_random2)=k_sample

write.table(hash_times_random, file='hash_times_random_dgt.tsv', sep='\t')
write.table(sparse_times_random1, file='sparse_times_random_dgt.tsv', sep='\t')
write.table(sparse_times_random2, file='sparse_times_random_dcg.tsv', sep='\t')

cat('random tables written\n')


cat('-----------------\n')
cat('Diagonal running\n')
cat('-----------------\n')

i=sample(1:k_full,max(k_sample))
j=k_full-i
i=i+round(rnorm(max(k_sample),0,500))
j=j+round(rnorm(max(k_sample),0,500))
i[i>=k_full]<-k_full-1
j[j>=k_full]<-k_full-1
i[i<0]<-1
j[j<0]<-1

hash_times_diag=sapply(k_sample, hash_time)
cat('hash done\n')
sparse_times_diag1=sapply(k_sample, sparse_time1)
sparse_times_diag2=sapply(k_sample, sparse_time2)
cat('sparse done\n')

colnames(hash_times_diag)=k_sample
colnames(sparse_times_diag1)=k_sample
colnames(sparse_times_diag2)=k_sample

write.table(hash_times_diag, file='hash_times_diag_dgt.tsv', sep='\t')
write.table(sparse_times_diag1, file='sparse_times_diag_dgt.tsv', sep='\t')
write.table(sparse_times_diag2, file='sparse_times_diag_dcg.tsv', sep='\t')
cat('diagonal tables written\n')


cat('----------------------------\n')
cat('Square in the middle running\n')
cat('----------------------------\n')

i=round(rnorm(max(k_sample),mean=k_full/2, sd=1e3))
j=round(rnorm(max(k_sample),mean=k_full/2, sd=1e3))

hash_times_square=sapply(k_sample, hash_time)
cat('hash done\n')
sparse_times_square1=sapply(k_sample, sparse_time1)
sparse_times_square2=sapply(k_sample, sparse_time2)
cat('sparse done\n')



colnames(hash_times_square)=k_sample
colnames(sparse_times_square1)=k_sample
colnames(sparse_times_square2)=k_sample

write.table(hash_times_square, file='hash_times_square_dgt.tsv', sep='\t')
write.table(sparse_times_square1, file='sparse_times_square_dgt.tsv', sep='\t')
write.table(sparse_times_square2, file='sparse_times_square_dcg.tsv', sep='\t')
cat('square tables written\n')




cat('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
cat('!!!!!!!!!!!!!!!!Done!!!!!!!!!!!!!!!\n')
cat('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
```
