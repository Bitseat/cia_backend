import pandas as pd
import re
import sys, json
import os
def read_in():
        lines = sys.stdin.readlines()
        # Since our input would only be having one line, parse our JSON data from that
        return json.loads(lines[0])
# value = input("Please enter issue id:\n")
lines = read_in()
# print(lines)
user_value = [int(s) for s in re.findall(r'\d+', lines)]

#print(user_value)
df = pd.read_csv(os.path.abspath("new_input.csv"))


# Create an empty list 
Row_list =[] 
  
# Iterate over each row 
for index,rows in df.iterrows(): 
    # Create list for the current row 
    my_list =rows.Issue_key
      
    # append the list to the final list 
    Row_list.append(my_list) 
  
 

# Extracting numbers
num_list = [int(i.split('-')[1]) for i in Row_list]

num_list.sort()

if user_value[0] < num_list[-1]:
    print(f' {lines} exists',f'Please enter id greater than {num_list[-1]}')
elif user_value[0] >= num_list[-1]:
    pass

###### after this the field on the web would be cleared out and the user will be able to enter new id####
####or do we need other way of doing it#########







