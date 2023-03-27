'''
Created on Jan 26, 2023

@author: Alex
'''
import json

# Files definition
nda_data_json_file='C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\NIMH-NDA-Data-structures.json'
instrument_json='C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instruments.json'
url_stub="https://nda.nih.gov/data_structure.html?short_name="
#instrument_shortName_file='C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\instrument_shortName.txt'
#instrument_title_file='C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\instrument_title.txt'


# Open json file
with open(nda_data_json_file) as jsondata:
    data = json.load(jsondata)

fields=["shortName","title","categories","dataType"] 
 
#print(data)
newdata=[]

count=0
for segment in data:
    count +=1
    newrecord={}
    for item in segment:
        if item in fields:
            newrecord[item]=segment[item]
        else:
            pass    
    newrecord["url"]=url_stub+segment["shortName"]
    newdata.append(newrecord)

print(f"count: {count}")       
        
with open(instrument_json, 'w') as f:
    json.dump(newdata, f, indent=6)

## Writing to two text files
#
# s = open(instrument_shortName_file, 'w')
# t = open(instrument_title_file, 'w')
# count = 0
#
# for segment in data:
#     #print (segment)
#     for i in segment:
#         if i=="shortName":
#             s.write(segment[i]+"\n")
#             count += 1
#
#         if i=="title":
#             t.write(segment[i]+"\n")
# s.close()
# t.close()
# print (count)