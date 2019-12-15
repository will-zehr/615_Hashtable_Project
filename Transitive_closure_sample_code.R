library('reticulate')
use_python("/usr/local/bin/python")
source_python("hash_matrix_transitive_closure.py",convert = F)
source_python("convert.py",convert = F)

# read in network, it have 10000 nodes and around 30000 edges
NW=read.table("theoretical_network.csv",header = F)
dims=c(10000,10000)

#adjacent matrix
adj=hash_matrix_tc(NW[,1],NW[,2],dims=dims)
#calculate the transitive closure
TC=transitive_closure(adj)
