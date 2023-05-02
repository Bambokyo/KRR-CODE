from flask import Flask,render_template,request
from rdflib import Graph
import pandas as pd
import numpy as np

app = Flask(__name__)
c=0
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/option1')
def option1():
    c=1
    return render_template('option1.html',c1=c)

@app.route('/option2')
def option2():
    c=2
    predicates=["?p",":typesOfCrimes",":hasOrganizedCrime",":hasVictims","dbo:year",":NumberOfVictims",":AreaName"]
    subjects=["?s",":murder",":murderByFireArm",":kidnapping",":rape"]
    objects=["?o","dbo:year","\"2003\"^^xsd:gYear ","\"Bihar\"^^xsd:string "]
    
    return render_template('option2.html',symbols=subjects,symbol1=predicates,symbol2=objects,c1=c)
@app.route('/', methods=["GET",'POST'])
def queryLocalGraph():
    c= request.form['c']
    print("JBSHBXJHZBHJCBJBCJHBCHBHJCBSHBCHSBSHBCSHBHJSCBHCBSHBCSHBCHBCHBCHBCHBSHBHCB",c)
    if(c=="1"):
        qn= request.form['qn']
        print(qn)
        print(type(qn))

        g = Graph()
        g.parse("CrimeOntology_RDF_Graph.ttl", format="ttl")
        
        print("Loaded '" + str(len(g)) + "' triples.")
        
        if(qn=="2"):
            w="""PREFIX : <http://www.krrproject.com/CrimeOntology/>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            select (AVG(?numberofArrests) AS ?AvgArrests)
            WHERE
            {
            ?s :hasArrests ?o.
            ?o dbo:year ?years.
            ?o :NumberOfOffendersArrested ?numberofArrests.
            }
            """

        elif(qn=="4"):
            w="""PREFIX : <http://www.krrproject.com/CrimeOntology/>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT (count(?weapons) AS ?weaponsCount) ?weapons
            WHERE
            {
            :murderByFireArm ?p ?o.
            ?o :TypeOfWeapon ?weapons.
            }
            group by ?weapons
            order by desc(?weaponsCount)
            limit 1

            """
        elif(qn=="5"):
            w="""PREFIX : <http://www.krrproject.com/CrimeOntology/>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            select (SUM(?numMurders) AS ?Murders) ?motive
            WHERE
            {
            :murder :hasMotive ?motive.
            ?motive :hasMotive ?motives.
            ?motives :NumberOfMurders ?numMurders.
            }
            group by ?motive
            order by desc(?Murders)
            limit 1
            """
        elif(qn=="1"):
            w="""PREFIX : <http://www.krrproject.com/CrimeOntology/>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            select (SUM(?rapevictims) AS ?HighestRapeVictim) ?agegroups
            {
            :rape ?l ?agegroups.
            ?agegroups :hasVictims ?victims.
            ?victims :NumberOfVictims ?rapevictims.
            }
            group by ?agegroups
            order by desc(?HighestRapeVictim)
            limit 1"""
        elif(qn=="3"):
            w="""PREFIX : <http://www.krrproject.com/CrimeOntology/>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            select (AVG(?numberofArrests) AS ?Avg_Rape_Victim_sBihar)
            {
            :rape ?l ?o.
            ?o :hasVictims ?vicnum.
            ?vicnum :AreaName "Bihar"^^xsd:string.
            ?vicnum :NumberOfVictims ?numberofArrests.

            }
            limit 1"""

        elif(qn=="6"):
            w="""PREFIX : <http://www.krrproject.com/CrimeOntology/>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            select Distinct ?bs

            {
            :murder ?l ?o.
            ?o :hasMotive ?c.
            ?c rdfs:label ?bs
            }

            """

        qres = g.query(w)
        a=qres
        arr=[]
        for i in a:
            arr.append(np.array(i))
        df=pd.DataFrame(arr,columns=a.vars)
        ac=df.to_html()
        strs="""border="1" class="dataframe\""""
        ac=ac.replace(f"{strs}","")
        strs="""style="text-align: right;\""""
        ac=ac.replace(f"{strs}","")
        print(ac)
        return render_template('pass.html',  tables=[ac])
    elif(c=="2"):
        s=(request.form.get("symbol1"))
        p=(request.form.get("symbol2"))
        o=(request.form.get("symbol3"))
        print(s,p,o)
        graph=Graph()
        graph.parse("CrimeOntology_RDF_Graph.ttl", format="ttl")
        print("Loaded '" + str(len(graph)) + "' triples.")
        # @app.route('/result')
        w = """
                PREFIX dbp: <http://dbpedia.org/property/'>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX : <http://www.krrproject.com/CrimeOntology/>
                prefix owl: <http://www.w3.org/2002/07/owl#> 
                prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            """
        qr = w + """  select * """ +""" WHERE {"""+s+" "+p+" "+o+" "+""" } Limit 10"""
        qres = graph.query(qr)
        a=qres
        arr=[]
        for i in a:
            arr.append(np.array(i))
        df=pd.DataFrame(arr,columns=a.vars)
        ac=df.to_html()
        strs="""border="1" class="dataframe\""""
        ac=ac.replace(f"{strs}","")
        strs="""style="text-align: right;\""""
        ac=ac.replace(f"{strs}","")
        print(ac)
        return render_template('pass.html',  tables=[ac])
# @app.route('/', methods=['POST'])
# def getval():
#     qn= request.form['qn']
#     return render_template('pass.html',n=qn)


if __name__ == "__main__":
    app.run(debug=True,port=800)
