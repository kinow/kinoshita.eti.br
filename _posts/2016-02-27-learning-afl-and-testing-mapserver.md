---
title: 'Learning afl and testing MapServer'
author: kinow
tags:
    - software quality
    - fuzzers
    - security
    - software quality
category: 'blog'
time: '23:21:03'
---

[afl](http://lcamtuf.coredump.cx/afl/) is a fuzzer, an application that combines a series of algorithms
in order to try invoking programs with several different input values. It then analyses the application
execution flow given different test case scenarios. 
You can read more about fuzzing at [this OWASP page](https://www.owasp.org/index.php/Fuzzing), or in other
blogs that I also used while learning about afl [1]("#1") [2]("#2")

At work we are using MapServer for serving WFS and WMS. And I am using it for the
[NZ OpenStreetMap maps](http://maps.nzoss.org.nz) too. MapServer is written in C++ and is normally
exposed as a CGI script, so I thought it was worth learning about afl and trying it on MapServer,
as in case it finds any interesting bug I can submit it to the MapServer project.

<!--more-->

## Download and build MapServer source code

MapServer code is hosted on [GitHub](https://github.com/mapserver/mapserver) and once you have cloned it a look
at the Travis CI configuration file will give you some hints on which dependencies you must have
installed on your operating system in order to build it. I will omit the steps to make this post shorter.

Once you have successfully built mapserv binary you will need to remove the generated files, and execute
CMake again but now using afl's compiler. This way the application will be instrumented and afl can
analyse its execution flow.

You can do that by exporting these two variables before running CMake.

{% geshi 'shell' %}
export CXX=/opt/afl-2.05b/afl-g++
export CC=/opt/afl-2.05b/afl-gcc
{% endgeshi %}

After this you can run CMake and GNU make again. That should create a binary instrumented mapserv,
that can be tested with afl.

{% geshi 'shell' %}
cd /home/kinow/Development/cpp/workspace/mapserver/
mkdir build && cd build
cmake ..
make
./mapserv -v
{% endgeshi %}

## Creating a shapefile mapfile

The easiest way to test MapServer locally, without Postgres or Postgis, is probably by
creating a single layer mapfile. LINZ provides shapefiles for New Zealand
([here's an example](https://data.linz.govt.nz/layer/1153-nz-coastlines-and-islands-polygons-topo-150k/))
that I used for this experiment.

<div class='row'>
<div class="span6 offset3" style='text-align: center;'>
<figure>
<a href="{{assets.qgis_settings}}" rel="prettyPhoto" class="thumbnail" title="QGIS Bounding Area settings">
<img class="span12" src="{{assets.qgis_settings}}" alt="QGIS Bounding Area settings" />
</a>
<figcaption>QGIS Bounding Area settings</i></figcaption>
</figure>
</div>
</div>

I used [QGIS](http://www.qgis.org/en/site/) to load the shapefile, take a look at the map,
and get the bounding area and projection. Here's the final mapfile.

{% geshi 'shell' %}
MAP
  IMAGETYPE      JPEG
  EXTENT         -97.238976 41.619778 -82.122902 49.385620
  SIZE           400 300
  SHAPEPATH      "/home/kinow/Downloads/linz-shp"
  IMAGECOLOR     255 255 255

  WEB
    METADATA
      "wms_title"           "WMS Fake Server"
      "wms_onlineresource"  "http://127.0.0.1/cgi-bin/mapserv?map=wms.map&"
      "wms_srs"             "EPSG:4167"
      "wms_enable_request"  "*"
    END
  END

  PROJECTION
    "init=epsg:4167"
  END

  LAYER # States polygon layer begins here
    NAME         nz-coastlines-and-islands-polygons-topo-150k
    DATA         nz-coastlines-and-islands-polygons-topo-150k
    STATUS       OFF
    TYPE         POLYGON

    CLASS
      NAME       "NZ Topo LINZ map"

      STYLE
        COLOR        232 232 232
        OUTLINECOLOR 32 32 32
      END
    END
  END
END
{% endgeshi %}

Then you can finally execute MapServer binary program and output to a local image file.

{% geshi 'shell' %}
export MS_ERRORFILE="stderr"
export MS_MAPFILE=/home/kinow/Development/cpp/workspace/mapserver/nztopo1.map

./mapserv -nh QUERY_STRING="VERSION=1.1.0&REQUEST=GetMap&LAYERS=nz-coastlines-and-islands-polygons-topo-150k&SRS=EPSG:4167&SERVICE=WMS&TEMPLATE=OpenLayers&BBOX=165.869,-52.6209,183.846,-29.2313&FORMAT=image/jpeg&HEIGHT=800&WIDTH=800" 2>/dev/null > /tmp/nzmap.jpg
{% endgeshi %}

## Running afl

I decided to use a RAM disk while running afl as suggested
[in this blog post](http://www.cipherdyne.org/blog/2014/12/ram-disks-and-saving-your-ssd-from-afl-fuzzing.html)
to avoid a lot of writes in my SSD disk. Then moved MapServer there and fired afl.

{% geshi 'shell' %}
cd /tmp/afl-ramdisk/mapserver
mkdir fuzz-input fuzz-output

/opt/afl-2.05b/afl-fuzz -m 500 -i fuzz-input/ -o fuzz-output/ -t 2000 ./mapserv QUERY_STRING="VERSION=1.1.0&REQUEST=GetMap&LAYERS=nz-coastlines-and-islands-polygons-topo-150k&SRS=EPSG:4167&SERVICE=WMS&TEMPLATE=OpenLayers&BBOX=165.869,-52.6209,183.846,-29.2313&FORMAT=image/jpeg&HEIGHT=800&WIDTH=800"
{% endgeshi %}

<div class='row'>
<div class="span6 offset3" style='text-align: center;'>
<figure>
<a href="{{assets.afl_testing_mapserver}}" rel="prettyPhoto" class="thumbnail" title="afl testing MapServer">
<img class="span12" src="{{assets.afl_testing_mapserver}}" alt="afl testing MapServer" />
</a>
<figcaption>afl testing MapServer</figcaption>
</figure>
</div>
</div>

However, it is not mutating the program input as I didn't use "@@" nor a dictionary. When you use @@, afl will replace
it by the location of a file that it generated. Or by using "-x" you can provide a dictionary used to generate
variations of parameters.

During the next days I will give it another go at work, and will investigate how to test MapServer without having to write
a wrapper in Shell or C/C++. You can still test other programs that are shipped with MapServer though.

{% geshi 'shell' %}
cd /tmp/afl-ramdisk/mapserver

/opt/afl-2.05b/afl-fuzz -m 512 -i fuzz-input -o fuzz-output -f /tmp/afl-ramdisk/input ./shp2img -m @@ -l nz-coastlines-and-islands-polygons-topo-150k -i image/jpeg -o /tmp/afl-ramdisk/nzmap.jpg -e 165.869 -52.6209 183.846 -29.2313
{% endgeshi %}

I hope it helps you get started with afl in case you are learning about it too :-) Happy hacking!

<br/>
<br/>
<sup><a name="1">1</a> 
<a href="https://fuzzing-project.org/tutorial3.html">
https://fuzzing-project.org/tutorial3.html</a></sup>

<sup><a name="2">2</a> 
<a href="https://www.nettitude.co.uk/fuzzing-with-american-fuzzy-lop-afl/">
https://www.nettitude.co.uk/fuzzing-with-american-fuzzy-lop-afl/</a></sup>

