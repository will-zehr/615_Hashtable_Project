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

#### step 1: make a range of k values that will be used 
```R
cat(seq(1e1,1e5, by=1000), file='sample_sizes.txt')
```

#### step 2: run command line argument
arguments: 1) full dimension size, 2) vector file with nonzero elements
```console
R --slave --args 1e8 sample_sizes.txt < hash_table.R
```

Outputs 2 tables: hash_times.tsv and sparse_times.tsv

### step 3: parse & plot output files
```R
hashdf<-read.table('hash_times.tsv',header=T)
sparsedf<-read.table('sparse_times.tsv')

colnames(hashdf)=sapply(colnames(hashdf), function(i) as.numeric(str_remove(i, "X")))
colnames(hashdf)=as.numeric(colnames(hashdf))/1e16

hashdf$id=rownames(hashdf)
hashdf$method='hash'


colnames(sparsedf)=sapply(colnames(sparsedf), function(i) as.numeric(str_remove(i, "X")))
colnames(sparsedf)=as.numeric(colnames(sparsedf))/1e16

sparsedf$id=rownames(hashdf)
sparsedf$method='sparse'


df<-rbind(melt(hashdf, id.vars=c('id','method')), melt(sparsedf, id.vars=c('id','method')))
df<-df%>%rename('sparsity'='variable')

time_plot<-df%>%filter(id=='time')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point()+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='computation time (seconds)')+
  ggtitle('time comparison')+
  theme(legend.position='bottom')

memory_plot<-df%>%filter(id=='size')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point()+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='object size (bytes)')+
  theme(legend.position='bottom')+
  ggtitle('memory comparison')

g_legend<-function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}

mylegend<-g_legend(memory_plot)

p3 <- grid.arrange(arrangeGrob(time_plot + theme(legend.position="none"),
                               memory_plot + theme(legend.position="none"),
                               nrow=1),
                   mylegend, nrow=2,heights=c(8, 1))

ggsave(p3, file='grid_plots.png', height=6, width=11)
```
