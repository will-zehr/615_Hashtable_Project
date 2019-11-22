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
