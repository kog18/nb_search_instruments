'''

@author: Alex
'''

import pysolr
import textwrap
import json

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/nb_articles/')
wrapper = textwrap.TextWrapper(width=150)

# Read search terms from a text file

with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instrument_shortName.txt', 'r') as f1:
    search_terms_short = [line.strip() for line in f1]
with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instrument_title.txt', 'r') as f:
    search_terms_title = [line.strip() for line in f]

search_terms = search_terms_short + search_terms_title;

# Search Solr with each term and print results
results_num=0
matches_arr = {}
matches_arr2 = {}
for term in search_terms:
    results = solr.search(f'methods:"{term}"', **{
        'fl': 'id,pmcid,pmid,title',
        'hl': 'true',
        'hl.method': 'unified',
        'hl.fragsize': '50',
        'hl.maxAnalyzedChars': '999999999',
        'hl.snippets': '3',
        'hl.fl': 'methods',
        'hl.simple.pre': ' ****** ',
        'hl.simple.post': ' ****** '
    })
    
    #print(f'Searching for: {term}')

    for result in results:
        results_num += 1 
        print(f'\n\tSearching for: {term}')
        pmcid = result['pmcid']
        pmid = result['pmid']
        title = result['title']
    
        # snippetl = str(results.highlighting[result['id']]['methods'][0].encode('utf8'))
        # snippet = wrapper.fill(snippetl)
        print(f"\t- Document ID: {result['id']}")

        print(f'\t- PMCID: {pmcid}')
        print(f'\t- PMID: {pmid}')
        print(f'\t- Title: {title.encode("utf-8")}')
        
        # instrument-pmcid
        if term in matches_arr:
            if pmcid not in matches_arr[term]:
                matches_arr[term].append(pmcid)
        else:
            matches_arr[term]=[pmcid]   
        
        
        # pmcid-instrument
        if pmcid in matches_arr2:
            if term not in matches_arr2[pmcid]:
                matches_arr2[pmcid].append(term)
        else:
            matches_arr2[pmcid]=[term]      
        #print(f'\t- Snippet: {snippet}')

    
print (f'\n\n\t Searched for {len(search_terms)} terms.')
print (f'\t Found {results_num} matches.')

# print (f'\n {matches_arr}')
# matches_json = json.dumps(matches_arr, indent="")
# print (matches_json)

with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instr_pmcid_matches.json', 'w') as f2:
    json.dump(matches_arr, f2, indent=6)

# with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\pmcid_instr_matches.json', 'w') as f2:
#     #matches_pmcid_instr_arr = {y: x for x, y in matches_arr.items()}
#     #matches_pmcid_instr_arr = dict(map(reversed, matches_arr.items()))
#     matches_pmcid_instr_arr = dict((v1, k) for k, v in matches_arr.items() for v1 in v)  # Reverse terms and pmcids
#     json.dump(matches_pmcid_instr_arr, f2, indent=6)

with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\pmcid_instr_matches.json', 'w') as f2:
    json.dump(matches_arr2, f2, indent=6)
