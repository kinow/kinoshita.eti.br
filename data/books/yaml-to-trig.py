#!/usr/bin/env python3

from ruamel.yaml import YAML
from html import unescape
import schema_salad.main

from rdflib.graph import Dataset, URIRef, RDF, BNode, Literal, Namespace

BOOKS_FILE='../../_data/books.yml'

def main():
    yaml = YAML(typ='safe')
    prefix = 'https://kinoshita.eti.br/books#'
    dataset = Dataset()
    # @prefix : <https://kinoshita.eti.br/books#>
    dataset.bind("", Namespace(prefix))

    # :books { ... }
    graph = URIRef(prefix)
    dataset.graph(identifier=graph)

    # schema-salad-ify, validating the doc

    assert 0 == schema_salad.main.main(argsl=['Books-schema.yml', BOOKS_FILE])

    with open(BOOKS_FILE) as doc:
        books = yaml.load(doc)

        for book in books:
            blank_node = BNode()
            title = unescape(book['title'].strip())
            author = unescape(book['author'].strip())
            dataset.add(
                (
                    blank_node, RDF.type, URIRef(f'{prefix}book'), graph
                )
            )
            dataset.add(
                (
                    blank_node, URIRef(f'{prefix}title'), Literal(title), graph
                )
            )
            dataset.add(
                (
                    blank_node, URIRef(f'{prefix}author'), Literal(author), graph
                )
            )
            dataset.add(
                (
                    blank_node, URIRef(f'{prefix}link'), Literal(book.get('link', '').strip()), graph
                )
            )

    print(dataset.serialize(format="trig"))

if __name__ == '__main__':
    main()
