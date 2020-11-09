import gzip, pickle
import os
from ast import literal_eval
import pandas as pd
import natsort
import csv
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn import model_selection, naive_bayes, svm

import docx 

from docx import Document

import numpy as np



#Import packages
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

import json, sys
# req = input("Enter the requirement description\n")
# test = input("Enter the test description\n")
def read_in():
        lines = sys.stdin.readlines()
        # Since our input would only be having one line, parse our JSON data from that
        return json.loads(lines[0])
data = []
lines = read_in()
for item in lines:
    data.append(item)
    # print(item)
# print(data[0], data[1])
req = data[0]
test = data[1]
tokenized_doc = []
doc = []
doc.append(req.lower())     

for d in doc:
    tokenized_doc.append(word_tokenize(d.lower()))


tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_doc)]
model = Doc2Vec(tagged_data, vector_size=5, window=2, min_count=1, workers=4, epochs = 100)

data = model.docvecs.vectors_docs
# opening the csv file in 'w+' mode 
filereq = open('req_vecs.csv', 'w+', newline ='') 
 
# writing the data into the file 
with filereq: 
    write = csv.writer(filereq) 
    write.writerows(data)

df = pd.read_csv('req_vecs.csv',header = None)

col_size = df.shape[1]


df.columns = ['req'+str(x) for x in range(0,col_size)]

df.applymap('{:.6f}'.format)

df.to_csv("req_with_index.csv", header = True, index = True)


tokenized_doct = []
doct = []
doct.append(test.lower())     

for dt in doct:
    tokenized_doct.append(word_tokenize(dt.lower()))


tagged_datat = [TaggedDocument(dt, [i]) for i, dt in enumerate(tokenized_doct)]
modelt = Doc2Vec(tagged_datat, vector_size=5, window=2, min_count=1, workers=4, epochs = 100)


datat = modelt.docvecs.vectors_docs 
# opening the csv file in 'w+' mode 
filetest = open('test_vecs.csv', 'w+', newline ='') 
 
# writing the data into the file 
with filetest: 
    write = csv.writer(filetest) 
    write.writerows(datat)
df2 = pd.read_csv('test_vecs.csv',header = None)
test_col_size = df2.shape[1]


df2.columns = ['test'+str(x) for x in range(0,test_col_size)]
df2.to_csv("test_with_index.csv", header = True, index = True)



'''
with open('req_vecs.csv','rt') as f1, open('test_vecs.csv','rt') as f2, open('merged_vecs.csv','w') as w:
    writer = csv.writer(w)
    for r1,r2 in zip(csv.reader(f1),csv.reader(f2)):
        writer.writerow(r1+r2)
        #writer.writerow(r1+r2)
'''


a = pd.read_csv("req_with_index.csv")
s = pd.read_csv("test_with_index.csv")

reqntest = pd.merge(a, s)
reqntest.to_csv('merged_vecs.csv', index = None)

new_input = pd.read_csv("merged_vecs.csv")
new_input = new_input.drop(['Unnamed: 0'],axis=1)



new_input = MinMaxScaler().fit_transform(new_input)

pickle_model = pickle.load(open("pickle_model.pkl", "rb"))    

Ypredict = pickle_model.predict(new_input)
# print(Ypredict)
Ypredict = Ypredict.astype('int64')

if Ypredict == 0:
    print("There's strong link between the two.")
else:
    print("The requirement and test cases don't seem to have link.")


