library(hash)
hash_table_sparse_matrix=function(i,j,value,dime){
  index=paste(as.character(i),as.character(j),sep=",")
  h=hash(index,value)
  .set(h,"posi"=index)
  .set(h,"dime"=dime)
  return (h)
}

convert_hash=function(h){
  dime=h[["dime"]]$dime
  index=paste(as.character(rep(1:dime[1],dime[2])),as.character(rep(1:dime[2],each=dime[1])),sep=",")
  array=has.key(index,h)
  int_ar=as.integer(array)
  mat=matrix(int_ar,nrow=dime[1],ncol=dime[2])
  position=which(mat==1)
  ind=paste(as.character(position%%dime[1]),as.character(ceiling(position/dime[1])),sep=",")
  mat[position]=values(h,ind)
  return (mat)
}

plus=function(h1,h2){
  posi1=h1[["posi"]]$posi
  posi2=h2[["posi"]]$posi
  h3=copy(h2)
  haskey=has.key(posi1,h2)
  value=values(h1,posi1)
  pos=which(haskey)
  value[pos]=value[pos]+values(h2,posi1[pos])
  .set(h3,posi1,value)
  return (h3)
}
  
  
  
  
