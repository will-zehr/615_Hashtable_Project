# 615_Hashtable_Project
Implementing a sparse hash table matrix design
## 1. Install package 'reticulate' in R
## 2. Put hash_matrix.py, hash_matrix_transitive_closure.py and convert.py to the current working directory.
## 3. Include the following code at the beginning of R script:
```R
	library('reticulate')
	use_python("/usr/local/bin/python")
	source_python("hash_matrix.py",convert = F)
	source_python("transitive_closure.py",convert = F)
	source_python("convert.py",convert = F)
```

## 4. hash matrix:
```R
# both 10 by 10 matrix
m1=read.csv("M1.csv",header = F)
m2=read.csv("M2.csv",header = F)
```
### 1). function hash_matrix(i,j.value,dims):
	Similar to sparsematrix() function in R, i is the row index, j is the column index, value is the corresponding non-zero number, dims is the dimension of the matrix. And this function outputs the corresponding sparse matrix in hash datatype.
	If the same pair of (i,j) is repeatedly given the first pair will be used.
```R
# hash_matrix
m1_hash=hash_matrix(m1[,1],m1[,2],m1[,3],c(10,10))
m2_hash=hash_matrix(m2[,1],m2[,2],m2[,3],c(10,10))
```
### 2). function plus(h1,h2):
	h1 and h2 must be hash_matrix datatype generated by hash_matrix(i,j.value,dims) above. And this function outputs the sum of these two matrix in the same datatype.
```R
#hash_plus
hash_plus_result=plus(m1_hash,m2_hash)
```
### 3). function multiply(h1,h2):
  h1 and h2 must be hash_matrix datatype generated by hash_matrix(i,j.value,dims) above. And this function outputs the crossproduct of these two matrix in the same datatype.
```R
#hash_multiply
hash_multiply_result=multiply(m1_hash,m2_hash)
```
## 5. Transitive closure:
```R
# read in network, it have 10000 nodes and around 30000 edges
NW=read.table("theoretical_network.csv",header = F)
dims=c(10000,10000)
```
### 1). function hash_matrix_tc(i,j,dims):
	This function outputs the hash datatype adjacent matrix. i is the beginning nodes of edges, j is the ending nodes of edges, dims takes value of a vector the first element is the number of potential beginning nodes and the second element is the number of potential ending nodes.
```R
#adjacent matrix
adj=hash_matrix_tc(NW[,1],NW[,2],dims=dims)
```
### 2). function multiply_tc(h1,h2):
	h1 and h2 must be hash_matrix_tc datatype generated by hash_matrix_tc(i,j,dims). And this function outputs the transitive relationship between h1 and h2
### 3). function transitive_closure(adj):
	adj is the adjacent matrix of a network and must be hash_matrix_tc datatype generated by hash_matrix_tc(i,j,dims). This function outputs the transitive_closure of a given network.
```R
#calculate the transitive closure
TC=transitive_closure(adj)
```
## convert
### 1). function convert(h):
	h can be either hash_matrix_tc datatype or hash_matrix datatype. This function converts the sparse matrix to dense matrix. Be careful when the dimension of the matrix is too large, the memory may overflow. When used in R, this function should be combined with py_to_r() to get the R dense matrix.
```R
#convert hash matrix to dense matrix
c_hash_multiply=py_to_r(convert(hash_multiply_result))
c_hash_plus=py_to_r(convert(hash_plus_result))
```
