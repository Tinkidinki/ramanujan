import requests

url = 'https://query.wikidata.org/sparql'
query = """
PREFIX entity: <http://www.wikidata.org/entity/>
#partial results

SELECT ?propUrl ?propLabel ?valUrl ?valLabel ?picture
WHERE
{
	hint:Query hint:optimizer 'None' .
	{	BIND(entity:Q83163 AS ?valUrl) .
		BIND("N/A" AS ?propUrl ) .
		BIND("identity"@en AS ?propLabel ) .
	}
	UNION
	{	entity:Q83163 ?propUrl ?valUrl .
		?property ?ref ?propUrl .
		?property rdf:type wikibase:Property .
		?property rdfs:label ?propLabel
	}
	
  	?valUrl rdfs:label ?valLabel
	FILTER (LANG(?valLabel) = 'hi') .
	OPTIONAL{ ?valUrl wdt:P18 ?picture .}
	FILTER (lang(?propLabel) = 'hi' )
}
ORDER BY ?propUrl ?valUrl

"""
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()
with open("ram.json", "w") as f:
    f.write(str(data))

info = {}
for item in data['results']['bindings']:
    info[item['propLabel']['value']] = item['valLabel']['value']

with open("ramanujan_page", "w") as f:
    for key in info.keys():
        f.write("रामानुजन का "+key+" "+info[key]+" है|\n")
# print(info)

l2_items = set()
for item in data['results']['bindings']:
    data_item = item['valUrl']['value'].split('/')[-1]
    val = item['valLabel']['value']
    l2_items.add((data_item, val))

for di in l2_items:
    query = """
PREFIX entity: <http://www.wikidata.org/entity/>
#partial results

SELECT ?propUrl ?propLabel ?valUrl ?valLabel ?picture
WHERE
{
	hint:Query hint:optimizer 'None' .
	{	BIND(entity:"""+di[0]+""" AS ?valUrl) .
		BIND("N/A" AS ?propUrl ) .
		BIND("identity"@en AS ?propLabel ) .
	}
	UNION
	{	entity:"""+di[0]+""" ?propUrl ?valUrl .
		?property ?ref ?propUrl .
		?property rdf:type wikibase:Property .
		?property rdfs:label ?propLabel
	}
	
  	?valUrl rdfs:label ?valLabel
	FILTER (LANG(?valLabel) = 'hi') .
	OPTIONAL{ ?valUrl wdt:P18 ?picture .}
	FILTER (lang(?propLabel) = 'hi' )
}
ORDER BY ?propUrl ?valUrl

"""
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()
    print(data)
    print("-"*50)

    info = {}
    for item in data['results']['bindings']:
        info[item['propLabel']['value']] = item['valLabel']['value']

    with open("ramanujan_page", "a") as f:
        for key in info.keys():
            f.write(di[1]+ " का "+key+" "+info[key]+" है|\n")
        f.write("\n")
        

