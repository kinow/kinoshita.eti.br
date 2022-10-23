# Data

The most valuable resource. Or maybe it was time?

The data in this directory is intended to be temporarily used to create a new
static site built on top of linked data.

The data is stored as TriG files. Each file may contain none, one, or more
graphs. These are supposed to be loaded into a server that supports SPARQL.

## Serving

```bash
docker run -p 3030:3030 \
  -e JVM_ARGS=-Xmx2g \
  -e TDB=2 \
  -e FUSEKI_DATASET_1=kinow \
  -v $(pwd -P)/fuseki:/fuseki \
  --name kinow-fuseki \
  stain/jena-fuseki
```

Useful commands:

```bash
docker logs fuseki
docker stop fuseki
docker restart fuseki
```
