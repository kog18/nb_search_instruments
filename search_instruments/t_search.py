'''
Created on Mar 7, 2023

@author: Alex
'''
import pysolr

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/nb_articles')

# Read terms from file
with open('C:\\Users\\Alex\\Documents\\Lei\\Neurobridge\\search\\instrument_shortName_test.txt') as f:
    terms = f.readlines()
terms = [term.strip() for term in terms]

# Query Solr for each term
for term in terms:
    results = solr.search('methods:"%s"' % term, **{
        'fl': 'pmcid,title,methods',
        'hl': 'true',
        'hl.snippets': '3',
        'hl.fragsize': '100'
    })

    # Print results
    print('Results for term "%s":' % term)
    for result in results:
        print('pmcid:', result['pmcid'])
        print('title:', result['title'])
        print('snippet:', result['methods_highlighting']['snippet'][0])
        print()