'''
Created on Feb 16, 2023

@author: Alex

Note that you will need to replace "http://localhost:8983/solr/collection_name/update?commit=true" with the URL of your own Solr instance, and "/path/to/directory" with the path to the directory containing the text files you want to ingest. Additionally, you'll need to set the field_name variable to the name of the Solr schema field that each paragraph starts with. Finally, make sure that the text files are encoded in UTF-8, as this code assumes that they are.

'''
import os
import glob
import requests
import json


solr_url = "http://localhost:8983/solr/nb_articles/update?commit=true"


dir_path = "C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\articles\\all"

# Solr schema fields
field_names = ["pmcid","pmid","title","methods"]


for file_path in glob.glob(os.path.join(dir_path, "*.txt")):
    
    with open(file_path, "r", encoding="utf-8") as f:
        contents = f.read()
    # Split the contents into paragraphs
    paragraphs = contents.split("\n")
    # Create a list of documents to send to Solr
    documents = []
    document = {}
    documents.append(document)
    for paragraph in paragraphs:
        # Ignore empty paragraphs
        if not paragraph:
            continue
        # If the paragraph starts with the name of the Solr schema field, create a new document
        for field_name in field_names:
            if paragraph.startswith(field_name.upper()):
                
                
                # Extract the field value from the paragraph and add it to the document
                field_value = paragraph[len(field_name):].strip()
                
                if not field_name in document:
                    document[field_name] = field_value.lower()
                else:
                    document[field_name] = document[field_name] + "\n" + field_value.lower()
            # Otherwise, add the paragraph to the current document
            # else:
            #     # If there is no current document, skip this paragraph
            #     if not documents:
            #         continue
            #     # Add the paragraph to the current document
            #     if "file_content" in document:
            #         document["file_content"] += "\n" + paragraph #.split(' ', 1)[1]
            #     else:
            #         document["file_content"] = paragraph #.split(' ', 1)[1]
    # Send the documents to Solr
    headers = {"Content-type": "application/json"}
    data = json.dumps(documents)
    response = requests.post(solr_url, headers=headers, data=data)
    
    if response.status_code != 200:
        print("Error ingesting file {} into Solr. Response status code: {}".format(file_path, response.status_code))
