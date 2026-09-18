In São Paulo, floors with mosaics of ceramic shards, in red, yellow and brown
was popular in the 50s, 60s. It was made with remnants of ceramics, and quickly
became a part of the city.

The script `main.py` will fill an area `width` by `height` with these shards.
The type of polygon (3, 4, 5 sides) will be chosen at random. The colours
chosen are 95% red, 3% brown, and 2% yellow -- the % indicates proportion.

It was created for a piece to be installed at Carrer de Loreto, Les Corts,
Barcelona. And made at the studio of [Natália Dametto](https://www.instagram.com/vitrales.natdametto/).

The code is licensed under CC 4.0.

Example:

```bash
$ pip install -e .[stained-glass]
$ cd ./args/stained_glass/caquinhos_de_ceramica/
$ python3 main.py \
    --width 58 \
    --height 40 \
    --pieces 180 \
    --min-size 3 \
    --max-size 5 \
    --gap 1.5 \
    --red "#8B4513" \
    --yellow "#FFD700" \
    --black "#000000" < ~/Downloads/vitral_inkscape.svg > ~/Desktop/test.svg
```
