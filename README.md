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
R --slave --args 1e7 sample_sizes.txt < time_comparison.R
```

Outputs 9 tables: 

- **time/space information for hash tables methods:** *hash_times_diag.tsv, hash_times_random.tsv, hash_times_square.tsv*


- **time/space information for column-supressed methods:** *sparse_times_diag_dcg.tsv, sparse_times_random_dcg.tsv, sparse_times_square.dcg.tsv*

- **time/space information for triplet methods:** *sparse_times_diag_dgt.tsv, sparse_times_random_dgt.tsv, sparse_times_square.dgt.tsv*


#### step 3: parse & plot output files
```R
x<-scan('~/sample_sizes.txt')
x<-x/1e14

hashdf<-read.table('~/hash_times_diag_dgt.tsv',header=T)
sparsedf1<-read.table('~/sparse_times_diag_dgt.tsv')
sparsedf2<-read.table('~/sparse_times_diag_dcg.tsv')

colnames(hashdf)=x

hashdf$id=rownames(hashdf)
hashdf$method='hash'

colnames(sparsedf1)=x
colnames(sparsedf2)=x

sparsedf1$id=rownames(hashdf)
sparsedf1$method='dgt'
sparsedf2$id=rownames(hashdf)
sparsedf2$method='dcg'


df<-rbind(melt(hashdf, id.vars=c('id','method')), 
          melt(sparsedf1, id.vars=c('id','method')),
          melt(sparsedf2, id.vars=c('id','method')))

df<-df%>%rename('sparsity'='variable')%>%mutate(sparsity=as.numeric(as.character(sparsity)))
df<-df%>%mutate(value=ifelse(id=='size',value/1e8,value))

time_plot_diag<-df%>%filter(id=='time')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point(size=.8, alpha=.6)+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='',x='density')+
  ggtitle('Diagonal Nonzero Values')+
  theme(legend.position='bottom')

memory_plot_diag<-df%>%filter(id=='size')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point(size=.8, alpha=.6)+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='', x='density')+
  theme(legend.position='bottom')

g_legend<-function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}

mylegend<-g_legend(memory_plot_diag)


hashdf<-read.table('~/hash_times_random_dgt.tsv',header=T)
sparsedf1<-read.table('~/sparse_times_random_dgt.tsv')
sparsedf2<-read.table('~/sparse_times_random_dcg.tsv')


colnames(hashdf)=x

hashdf$id=rownames(hashdf)
hashdf$method='hash'

colnames(sparsedf1)=x
colnames(sparsedf2)=x

sparsedf1$id=rownames(hashdf)
sparsedf1$method='dgt'
sparsedf2$id=rownames(hashdf)
sparsedf2$method='dcg'


df<-rbind(melt(hashdf, id.vars=c('id','method')), 
          melt(sparsedf1, id.vars=c('id','method')),
          melt(sparsedf2, id.vars=c('id','method')))

df<-df%>%rename('sparsity'='variable')%>%mutate(sparsity=as.numeric(as.character(sparsity)))
df<-df%>%mutate(value=ifelse(id=='size',value/1e8,value))


time_plot_random<-df%>%filter(id=='time')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point(size=.8, alpha=.6)+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='time (seconds)',x='density')+
  ggtitle('Random Nonzero Values')+
  theme(legend.position='bottom')

memory_plot_random<-df%>%filter(id=='size')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point(size=.8, alpha=.6)+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='object size', x='density')+
  theme(legend.position='bottom')

hashdf<-read.table('~/hash_times_square_dgt.tsv',header=T)
sparsedf1<-read.table('~/sparse_times_square_dgt.tsv')
sparsedf2<-read.table('~/sparse_times_square_dcg.tsv')

colnames(hashdf)=x

hashdf$id=rownames(hashdf)
hashdf$method='hash'

colnames(sparsedf1)=x
colnames(sparsedf2)=x

sparsedf1$id=rownames(hashdf)
sparsedf1$method='dgt'
sparsedf2$id=rownames(hashdf)
sparsedf2$method='dcg'


df<-rbind(melt(hashdf, id.vars=c('id','method')), 
          melt(sparsedf1, id.vars=c('id','method')),
          melt(sparsedf2, id.vars=c('id','method')))

df<-df%>%rename('sparsity'='variable')%>%mutate(sparsity=as.numeric(as.character(sparsity)))
df<-df%>%mutate(value=ifelse(id=='size',value/1e8,value))

time_plot_square<-df%>%filter(id=='time')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point(size=.8, alpha=.6)+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='',x='density')+
  ggtitle('Square Nonzero Values')+
  theme(legend.position='bottom')

memory_plot_square<-df%>%filter(id=='size')%>%ggplot(aes(x=sparsity,y=value,color=method))+
  geom_point(size=.8, alpha=.6)+
  geom_line(aes(group=method))+
  theme_bw()+
  labs(y='', x='density')+
  theme(legend.position='bottom')


p3 <- grid.arrange(arrangeGrob(time_plot_random + theme(legend.position="none"),
                               time_plot_diag + theme(legend.position="none"),
                               time_plot_square + theme(legend.position="none"),
                               memory_plot_random + theme(legend.position="none"),
                               memory_plot_diag + theme(legend.position="none"),
                               memory_plot_square + theme(legend.position="none"),
                               nrow=2),
                   mylegend, nrow=2,heights=c(8, 1))

ggsave(p3, file='~/grid_plots_diagonal.png', height=6, width=9)
```
