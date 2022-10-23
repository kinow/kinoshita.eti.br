#!/usr/bin/env bash

docker run -p 3030:3030 \
  -e JVM_ARGS=-Xmx2g \
  -e TDB=2 \
  -e FUSEKI_DATASET_1=kinow \
  -e ADMIN_PASSWORD=admin \
  -v $(pwd -P)/fuseki:/fuseki \
  --name kinow-fuseki \
  -d \
  stain/jena-fuseki:4.0.0
