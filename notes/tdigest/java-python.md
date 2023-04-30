# t-digest: Java & Python implementations

The original t-digest implementation is written in Java by
Ted Dunning: <https://github.com/tdunning/t-digest>

The Python t-digest implementation used here is this one:
<https://github.com/CamDavidsonPilon/tdigest>

## Java implementation

<img src="./tdigest.png" alt="t-digest UML class diagram" style="width: 600px;" />

<img src="./tdigest2.png" alt="t-digest UML class diagram with fields" style="width: 600px;" />

## Python implementation

<img src="./py-tdigest.png" alt="Python t-digest UML class diagram" style="width: 600px;" />

<img src="./py-tdigest2.png" alt="Python t-digest UML class diagram with fields" style="width: 600px;" />

## Main differences

The Java implementation has two t-digest types: `AVLTreeDigest`, and
`MergingDigest`, while the Python implementation has just one.

The Java t-digest uses a Fenwick Tree to store the data, whilst
the Python t-digest uses a red/black tree modified to store the
sum of 
