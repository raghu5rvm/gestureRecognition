############################################################################################

library(e1071)
library(ggplot2)
library(amap)

setwd("/home/salt/Desktop/projFiles/cohn-kanade-images croppedLabelled");

# read data from a csv file
# d<-fread("/opt/hadoop/bin/hadoop fs -csv hdfs://10.0.0.222:54310/test/data.csv",
            #  sep = '\t',header = FALSE,stringsAsFactors = TRUE)
d<-read.csv("testFinal.csv",sep='\t',header=FALSE,row.names = NULL,stringsAsFactors = TRUE);
d2<-d[,c(-1,-1026)]

#apply principle component analysis on given data
model<-prcomp(d2)

nSC1<-40
#visiualize classification by PCs which are accessed by model$x[,i] and labels from d[,1] 
features1<-model$x[,1:nSC1];


#append labels at the end of feature matrix
features1<-cbind(features1,d[,1]);

set.seed(2222);

#generate random indexes for training and test data set generation
indexes<-sample(1:nrow(features1),0.8*nrow(features1));
testData<-features1[indexes,];
trainData<-features1[-indexes,];


exprName<-matrix(testData[,(nSC1+1)],ncol=1);
exprValues<-matrix(testData[,-(nSC1+1)],ncol=nSC1);

#apply support vector machine on test data to calssify data
svmModel<-svm(exprName~exprValues);

#print (summary(svmModel))

#use model to verify on test data
predicted<-predict(svmModel,testData[,-(nSC1+1)])

#compare results
result<-cbind(round(predicted),testData[,(nSC1+1)]);
#print (result)
r<-matrix(unlist(result),ncol=2)

smlr<-1
for (i in 1:nrow(r)){
  if(r[i,1]==r[i,2])
    smlr<-smlr+1
}

prnt<-(smlr*100/nrow(r))
paste0(prnt,"% accurate!!!")
set.seed(Sys.time());



###########################################################################################

library(dplyr)
library(sparklyr)
library(data.table)
setwd("/home/salt/Desktop/projFiles/cohn-kanade-images croppedLabelled");


#set SPARK_HOME and establish a spark connection
SPARK_HOME="/home/salt/R/spark";
spark_disconnect_all();
sc<-spark_connect(master="spark://10.0.0.222:7077",spark_home=SPARK_HOME);

#read data from hdfs
system.time(myData<-fread("/opt/hadoop/bin/hadoop fs -text hdfs://10.0.0.222:54310/test/data90.csv",
              sep = '\t',header = FALSE,stringsAsFactors = TRUE))


#read from remote system using ssh
system.time(myData <- read.table(pipe('ssh -l salt 10.0.0.10 "cat /home/salt/Desktop/testFinal.csv"')))




#myData<-read.csv("testFinal90.csv",sep='\t',header=FALSE,row.names = NULL,stringsAsFactors = TRUE);
d300395<-myData[,301:395];
d300395<-matrix(unlist(d300395),ncol=95,byrow = TRUE)
d300395t<-t(d300395)
d300395t<-as.data.frame(d300395t);


#copy data to spark cluster and create a spark_table
face_data<-copy_to(sc,d300395t);

#apply principle component analysis on data using spark ml_pca function
d_pca2<-face_data %>%
  ml_pca();


nPC<-90
#select features after applying pca on data
features2<-d_pca2$components[,1:nPC];

#append labels to features
features2<-cbind(features2,myData[,1]);


set.seed(1234);

#generate random indexes for training and test data set generation
indexes2<-sample(1:nrow(features2),0.8*nrow(features2));
testData2<-features2[indexes2,];
trainData2<-features2[-indexes2,];


exprName2<-matrix(testData2[,nPC+1],ncol=1);
exprValues2<-matrix(testData2[,-(nPC+1)],ncol=nPC);# features is of dimension 90 x 11 where 11>labels 

#generate model using priciple components with svm
svmModel2<-svm(exprName2~exprValues2);

#test model with sample data
predicted2<-predict(svmModel2,testData2[,-(nPC+1)])

#compare results after prediction by model
result2<-cbind(round(predicted2),testData2[,(nPC+1)]);
#print (result)
r2<-matrix(unlist(result2),ncol=2)

smlr2<-1
for (i2 in 1:nrow(r2)){
  if(r2[i2,1]==r2[i2,2])
    smlr2<-smlr2+1
}

prnt2<-(smlr2*100/nrow(r2))
paste0(prnt2,"% accurate!!!-----using spark cluster")
#close spark connection
spark_disconnect(sc);
set.seed(Sys.time())
