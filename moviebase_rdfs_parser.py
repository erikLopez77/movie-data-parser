import json
from rdflib import RDF, RDFS, XSD, Graph, SDO, Namespace, Literal

EXA = Namespace("http://exmaple.org/abox#")
EXT = Namespace("http://example.org/tbox#")
DBO = Namespace("http://dbpedia.org/ontology/")


def create_rdf_from_json(json_data):
    g = Graph()

    g.bind("xsd", XSD)
    g.bind("xsd", SDO)
    g.bind("xsd", EXA)
    g.bind("xsd", DBO)

    for film in json_data:
        film_uri = EXA[film["Title"].replace(" ", "_")]
        g.add((film_uri, RDF.type, DBO.Film))
        g.add((film_uri, RDFS.label, Literal(film["Title"], lang="en")))

        director_uri = EXA[film["Director"].replace(" ", "_")]
        g.add((film_uri, DBO.director, director_uri))
        g.add((director_uri, RDF.type, EXT.Director))

        for actor in film["Starring"].split(", "):
            actor_uri = EXA[actor.replace(" ", "_")]
            g.add((film_uri, DBO.starring, actor_uri))
            g.add((actor_uri, RDF.type, EXT.Actor))


if __name__ == "__main__":
    data_input = input("Enter the file name of the input data: ")

    with open(data_input, "r") as file:
        json_data = json.load(file)

    rdf_graph = create_rdf_from_json(json_data)
