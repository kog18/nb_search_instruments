'''
Created on Mar 7, 2023

@author: Alex
'''
import requests
import json

# URL of the Solr instance
solr_url = "http://localhost:8983/solr/nb_articles/select"

# Query parameters
query_params = {
    "q": "file_content:(METHODS AND 98)",  # search for the string "search_string" in the field "file_content", but only in paragraphs that start with "METHODS"
    "wt": "json",  # response format
    "rows": 100,  # number of rows to return in the response
    "hl": "true",  # enable highlighting
    "hl.fl": "file_content",  # specify the field to highlight
    "hl.snippets": 3,  # return a 3 line snippet of the text where the terms were found
    "hl.fragsize": 100  # specify the maximum size of each snippet in characters
}

# Send the request to Solr
response = requests.get(solr_url, params=query_params)

# Check the response status code
if response.status_code == 200:
    # Parse the response as JSON
    response_json = json.loads(response.text)
    # Extract the results from the response
    results = response_json["response"]["docs"]
    # Extract the highlighting information from the response
    highlighting = response_json["highlighting"]
    # Iterate over the results and print the contents of each result
    for result in results:
        doc_id = result["id"]
        file_content = result["file_content"]
        # Print the highlighting information for this result
        for highlight in highlighting[doc_id]["file_content"]:
            print(highlight)
else:
    # Print an error message if the request fails
    print("Request failed with status code {}".format(response.status_code))

