##network generater
i=c()
j=c()
dims=c(10000,10000)
for (k in 1:100){
  ind=sample(1:100,2,replace = T)
  i=c(i,sample(((ind[1]-1)*100+1):(ind[1]*100),300,replace = T))
  j=c(j,sample(((ind[2]-1)*100+1):(ind[2]*100),300,replace = T))
}

out=cbind(i,j)
write.table(out,'network.csv',sep = ",",col.names = F,row.names = F)