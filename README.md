# 615_Hashtable_Project
Implementing a sparse hash table matrix design

Our goal is to beat existing sparse matrix classes in R.
#### Step 1: load packages
```R
library(hash)
library(reticulate)
```

#### Step 2: Make row & column indeces, values, and dimensions
```R
i=sample(1:10,5)
j=sample(1:10,5)
x=rnorm(5,mean=3,sd=7)
dime=c(10,10)
```

#### Step 3: load python script
```R
use_python("/usr/local/bin/python")
source_python('hash_table.py')
```


#### Step 4: make sparse matrix
```R
h_R=hash_table_sparse_matrix(i=i,j=j,value=x,dime=dime)

h_py=hash_matrix(i=i,j=j,value=x,dime=dime)
```

## Testing time efficiency across a range of k values
```R
k_full=10000000
k_sample=c(1e4,5e4,1e5,5e5,1e6,1e7)
sapply(k_sample, function(m){
  i=sample(1:k_full,m)
  j=sample(1:k_full, m)
  x=rnorm(m)
  dime=c(k_full,k_full)
  h=hash_table_sparse_matrix(i=i,j=j,value=x,dime=dime)
  return(system.time(multiply_hash(h,h)))}
)
```
