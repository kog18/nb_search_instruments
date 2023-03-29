'''

@author: Alex
'''

import pysolr
import textwrap
import json

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/nb_articles/')
wrapper = textwrap.TextWrapper(width=150)

# Read search terms from a jason file

with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instruments.json') as jsondata:
    data = json.load(jsondata)

fields=["shortName","title"]
matches=[]

# Search Solr with each term and print results
for instrument in data:
    for item in instrument:
        if item in fields:
            #print(f'{item}-{instrument[item]}')
            term=instrument[item]
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
                #print(f'{item}-{instrument[item]}')
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
                    
                    
                # If pmcid is not in the matches array    
                if not any(pmcid in d.values() for d in matches):
                    newrecord={}
                    newrecord['pmcid']=result['pmcid']
                    newrecord['matches']=[{"instrument":term, "url":instrument['url']}]
                    print(newrecord)
                    matches.append(newrecord)
                    print(matches)
                # If the pmcid record exists - add another instrument match
                else:
                    for record in matches:
                        if record['pmcid'] == pmcid:        
                            print('existing record: '+record['pmcid'])           
                            record['matches'].append({"instrument":term, "url":instrument['url']})                   
                        
                
with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\matches_fuzzy.json', 'w') as f2:
    json.dump(matches, f2, indent=6)

        
        # instrument-pmcid
        # if term in matches_arr:
        #     if pmcid not in matches_arr[term]:
        #         matches_arr[term].append(pmcid)
        # else:
        #     matches_arr[term]=[pmcid]   
        #
        #
        # # pmcid-instrument
        # if pmcid in matches_arr2:
        #     if term not in matches_arr2[pmcid]:
        #         matches_arr2[pmcid].append(term)
        # else:
        #     matches_arr2[pmcid]=[term]      
        # #print(f'\t- Snippet: {snippet}')

    
# print (f'\n\n\t Searched for {len(search_terms)} terms.')
# print (f'\t Found {results_num} matches.')

# print (f'\n {matches_arr}')
# matches_json = json.dumps(matches_arr, indent="")
# print (matches_json)

# with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instr_pmcid_matches.json', 'w') as f2:
#     json.dump(matches_arr, f2, indent=6)
#
# with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\pmcid_instr_matches.json', 'w') as f2:
#     json.dump(matches_arr2, f2, indent=6)
