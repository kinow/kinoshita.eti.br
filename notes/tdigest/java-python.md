# t-digest: Java & Python implementations

## Java implementation

The original t-digest implementation is written in Java by
Ted Dunning: <https://github.com/tdunning/t-digest> (Apache License).

<img src="./tdigest.png" alt="t-digest UML class diagram" style="width: 600px;" />

<img src="./tdigest2.png" alt="t-digest UML class diagram with fields" style="width: 600px;" />

## Python implementation

The Python t-digest implementation used here is this one:
<https://github.com/CamDavidsonPilon/tdigest> (MIT License).

<img src="./py-tdigest.png" alt="Python t-digest UML class diagram" style="width: 600px;" />

<img src="./py-tdigest2.png" alt="Python t-digest UML class diagram with fields" style="width: 600px;" />

## Main differences

> WIP: first pass over the code, still pending practical comparison
>      to confirm the findings here.

### Backing data structures

The Java implementation has two t-digest types: `AVLTreeDigest`, and
`MergingDigest`, while the Python implementation has just one.

`AVLTreeDigest` uses an [AVL Tree](https://en.wikipedia.org/wiki/AVL_tree)
that has centroids as node values. Centroids are
[weighted averages](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean).

`MergingDigest` has a comment on its Javadoc saying it's “generally
the best known implementation right now”. It accumulates points into
a buffer and occasionally sorts and merges these points into a sorted
array. It amortizes the sort-merge operation.

The Python implementation is more similar to the `AVLTreeDigest`. It
uses an `AccumulationTree` object as base data structure, from a
[Python library created especifically for this t-digest](https://github.com/tkluck/accumulation_tree),
that uses a [Red Black Tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
modified to have partial aggregations as values (to speed up calculating
the sums of bins/segments). Red Black Trees are not strictly balanced,
with faster insertion, but slower search times than the AVL Tree,
so the Python library has probably some disadvantage for using
a Red Black Tree (it's also not clear if the complexity is the same
since it is a Red Black Tree modified to have aggregated values instead
of simple values as the textbook implementations).

### Application Programming Interface (API)

The interface and operations are not identical. With Java you would
call `add` to add another instance of t-digest, or to add a new `double`
value. With Python, it uses `__add__` to add another instance, and `update()`
to add a new `double` value.

The Java implementation also has more validation (like checking `min`, `max` values),
while the Python version skips it.

Both the Java and Python implementations support compression and calculating
the [cumulative distribution function (cdf)](https://en.wikipedia.org/wiki/Cumulative_distribution_function).

#### Sample code

This t-digest Java code,

```java
class Test {
    public static void main(String[] args) {
        AVLTreeDigest tdigest = new AVLTreeDigest(3);
        tdigest.recordAllData();
        Random r = new Random(42);
        for (int i = 0; i < 100; i += 1) {
            tdigest.add(r.nextDouble() * 100);
        }
        System.out.printf("Min is %f, max is %f%n", tdigest.min, tdigest.max);
        System.out.printf("Count is %d, there are %d centroids%n", tdigest.count, tdigest.summary.size());
        for (Centroid c : tdigest.summary) {
            System.out.printf("Centroid %d, mean %f, data is %s%n", c.id(), c.mean(), c.data());
        }
    }
}
```

produces something similar to

```bash
Min is 2.702987, max is 97.603447
Count is 100, there are 16 centroids
Centroid 2, mean 2.702987, data is [2.702986688213338]
Centroid 4, mean 2.731417, data is [2.7314166285965835]
Centroid 6, mean 6.687712, data is [3.141823882658079, 3.6484516690249658, 7.7085112935252, 9.6450915880824, 9.294681694145556]
Centroid 8, mean 14.732423, data is [17.221793768785243, 15.103155452875827, 12.625782329876534, 13.978959528686087]
Centroid 10, mean 17.583722, data is [17.737847790937835, 17.927344087491736, 17.085973788289756]
Centroid 12, mean 20.062628, data is [20.976756886633208, 19.5964207423156, 19.614707188185154]
Centroid 14, mean 27.728519, data is [27.574806944170238, 27.88223024987677]
Centroid 16, mean 30.252662, data is [27.707849007413664, 29.16564974118041, 28.05719916728102, 31.532845005767296, 30.557915566744885, 33.232427838474855, 31.51474713673178]
Centroid 18, mean 42.109372, data is [30.871945533265976, 36.87829134113056, 46.36535758091534, 43.64909744232865, 38.65668743593487, 35.791991947712866, 41.76875467529187, 48.05745165564343, 36.91214939418974, 36.02548753661351, 43.466108514061034, 45.73170944447694, 47.26884208758554, 46.90225206155686, 46.030637266116116, 48.659066182619405, 42.097170663102865, 37.10122896837609, 37.43593560890043, 46.33992710283451, 49.732689247592056, 48.384385495430514, 39.576628017124214, 38.46108439172914, 37.38361436205424, 43.13095551354611, 44.273594208622036]
Centroid 20, mean 62.039376, data is [68.32234717598455, 66.55489517945736, 59.43499108896842, 58.74273817862956, 57.104034841486715, 58.002488450206066, 63.6644547856282, 63.286979135327904, 69.9858645067172, 57.16203055299766, 61.62136850351787, 69.72487292697295, 62.79332754134727, 53.99094342593693, 63.51110144563881, 65.50533811098211, 64.62319787976428, 59.88370371450177, 54.83346917317515]
Centroid 22, mean 78.317633, data is [72.75636800328681, 78.29017787900358, 74.99061812554476, 82.5965871887821, 75.12804067674601, 75.2509948590651, 81.77969308356393, 71.3406257823229, 82.04918233863467, 82.7322424014995, 83.38662354441657, 80.5730942661998, 80.91248167277394, 77.0465637773941, 77.51206959271755, 74.51533062153855, 80.53907199213823]
Centroid 24, mean 88.372911, data is [90.33722646721782, 86.56867963273523, 87.18145959648386, 89.40427958184088]
Centroid 26, mean 90.904923, data is [91.93277828687168, 90.8614580207571, 89.92053297295577]
Centroid 28, mean 94.501630, data is [94.98601346594666, 94.0172465685381]
Centroid 30, mean 97.403568, data is [97.40356814958814]
Centroid 32, mean 97.603447, data is [97.60344716184083]
```

### Maths.... other... precision... etc...

WIP
