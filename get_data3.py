import sys
import subprocess
import csv
import os
import pandas as pd
import re

import pymongo 
import json
from preprocess_and_test import Preprocess
from pathlib import Path

def read_in():
        datas = sys.stdin.readlines()
        # Since our input would only be having one line, parse our JSON data from that
        return json.loads(datas[0])
data = []
datas = read_in()
for item in datas:
    data.append(item)
    
issueid = data[1]

reqtext = data[0]
with open("filename.txt") as file_in:
            
    for line in file_in:
        lines = line
                

print("from py shell"+issueid,reqtext,lines)

pr = Preprocess()
print(issueid, reqtext, lines)
pr.append(issueid,reqtext,lines)

if not os.path.exists('docx'):
    os.makedirs('docx')

if not os.path.exists('txt'):
    os.makedirs('txt')

if not os.path.exists('candidates'):
    os.makedirs('candidates')

path = os.path.abspath("docx")
pr.csvToDocx(lines)
pr.convertDocxToText(path + '/')
filenames = os.listdir(os.path.abspath("txt/"))
pr.docToVec(filenames)
cia_model = "sl_doc2vec.model"
pr.vecToCsv(cia_model)
with open("projectname.txt") as file_in:
            
    for line in file_in:
        proj_name = line
if(proj_name == "Moyo"):
    model_test = "Moyo.pkl"
else:
    model_test = "Connect +.pkl"

vecs = "vecs.csv"
txt_folder = os.path.abspath("txt/")
candidates_fld = os.path.abspath("candidates/")
result2 = pr.cluster(model_test, lines, vecs, txt_folder + '/', candidates_fld + '/', reqtext)
tableValues1 = []
tableValues2 = []

for i in result2[0]:
    tableValues1.append(result2[1][i[0]])
    tableValues2.append(str(i[1]))
print("successfully finished!")

df = pd.read_csv("new_input.csv")  

content = []

for f in df['Issue_key'].values:
    for i in tableValues1:
        if i in df['Issue_key'].values:
            content.append(df.loc[df['Issue_key'] == i,'Requirement'])

from string import digits

res = ''.join(filter(lambda x: not x.isdigit(), content[0]))
res2 = ''.join(filter(lambda x: not x.isdigit(), content[1]))
res3 = ''.join(filter(lambda x: not x.isdigit(), content[2]))
res4 = ''.join(filter(lambda x: not x.isdigit(), content[3]))
res5 = ''.join(filter(lambda x: not x.isdigit(), content[4]))

issue_ids = [tableValues1[0], tableValues1[1], tableValues1[2],tableValues1[3], tableValues1[4]]
similarities = [tableValues2[0], tableValues2[1],tableValues2[2], tableValues2[3], tableValues2[4]]
description =[res,res2,res3,res4,res5]

try: 
    conn = pymongo.MongoClient("mongodb://localhost:27017/") 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
  
# database 
db = conn.angular8mean 
  
# Created or Switched to collection names: my_gfg_collection 
collection = db.ciadata  

collection.remove( { } )
candidate_rec1 = {
        "candidate_name": " ",
        "candidate_email":" ",
        "requirements": [], 
        "issueid":tableValues1[0], 
        "similarity":str(round(float(tableValues2[0])*100))+"%", 
        "description":res
        } 
candidate_rec2 = { 
        "candidate_name": " ",
        "candidate_email":" ",
        "requirements": [],
        "issueid":tableValues1[1], 
        "similarity":str(round(float(tableValues2[1])*100))+"%", 
        "description":res2
        } 
candidate_rec3 = { 
        "candidate_name": " ",
        "candidate_email":" ",
        "requirements": [],
        "issueid":tableValues1[2], 
        "similarity":str(round(float(tableValues2[2])*100))+"%", 
        "description":res3
        } 

candidate_rec4 = { 
        "candidate_name": " ",
        "candidate_email":" ",
        "requirements": [],
        "issueid":tableValues1[3], 
        "similarity":str(round(float(tableValues2[3])*100))+"%", 
        "description":res4
        } 
candidate_rec5 = { 
        "candidate_name": " ",
        "candidate_email":" ",
        "requirements": [],
        "issueid":tableValues1[4], 
        "similarity":str(round(float(tableValues2[4])*100))+"%", 
        "description":res5
        } 
  
# Insert Data 
rec_id1 = collection.insert_one(candidate_rec1) 
rec_id2 = collection.insert_one(candidate_rec2)
rec_id3 = collection.insert_one(candidate_rec3)
rec_id4 = collection.insert_one(candidate_rec4)
rec_id5 = collection.insert_one(candidate_rec5) 
  
print("Data inserted with record ids",rec_id1," ",rec_id2,rec_id3,rec_id4,rec_id5) 
  
# Printing the data inserted 
cursor = collection.find() 
for record in cursor: 
    print(record) 
        