library('reticulate')
use_python("/usr/local/bin/python")
source_python("hash_matrix.py",convert = F)
source_python("convert.py",convert = F)

# both 10 by 10 matrix
m1=read.csv("M1.csv",header = F)
m2=read.csv("M2.csv",header = F)

# hash_matrix
m1_hash=hash_matrix(m1[,1],m1[,2],m1[,3],c(10,10))
m2_hash=hash_matrix(m2[,1],m2[,2],m2[,3],c(10,10))


#hash_multiply
hash_multiply_result=multiply(m1_hash,m2_hash)
#hash_plus
hash_plus_result=plus(m1_hash,m2_hash)
#convert hash matrix to dense matrix
c_hash_multiply=py_to_r(convert(hash_multiply_result))
c_hash_plus=py_to_r(convert(hash_plus_result))



#use dense matrix to verify
# dense_matrix
dense_m1=py_to_r(convert(m1_hash))
dense_m2=py_to_r(convert(m2_hash))
#dense_matrix
dense_mul=dense_m1%*%dense_m2
dense_plu=dense_m1+dense_m2

#result is the same
dense_mul==c_hash_multiply
dense_plu==c_hash_plus
