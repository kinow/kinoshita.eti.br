#!/usr/bin/env python3

import pandas as pd
from ruamel.yaml import YAML
from rdflib.graph import Dataset, URIRef, RDF, BNode, Literal, Namespace

MOVIES_FILE='movielens-ratings.csv'

def main():
    yaml = YAML(typ='safe')
    prefix = 'https://kinoshita.eti.br/movies#'
    dataset = Dataset()
    # @prefix : <https://kinoshita.eti.br/books#>
    dataset.bind("", Namespace(prefix))

    # :books { ... }
    graph = URIRef(prefix)
    dataset.graph(identifier=graph)

    df = pd.read_csv(MOVIES_FILE, index_col=0)
    for row in df.itertuples():
        blank_node = BNode()
        dataset.add(
            (
                blank_node, RDF.type, URIRef(f'{prefix}movie'), graph
            )
        )
        for attr in df.columns:
            dataset.add(
                (
                    blank_node, URIRef(f'{prefix}{attr}'), Literal(f'{row.__getattribute__(attr)}'.strip()), graph
                )
            )

    print(dataset.serialize(format="trig"))

if __name__ == '__main__':
    main()
