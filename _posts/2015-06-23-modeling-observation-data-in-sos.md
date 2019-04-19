---
title: 'Modeling observation data in SOS (Sensor Observation Service)'
author: kinow
tags:
    - sensor web
category: 'blog'
time: '13:40:03'
---

This week NZ Herald published an [article](http://www.nzherald.co.nz/technology/news/article.cfm?c_id=5&objectid=11469418)
about a device created by an Irish farmer enterpreneur that sends a message to a farmer when the cow is about to give birth.
The device monitors "heightened tail moviment".

In this post I will try to apply what I am learning following the [SOS Tutorial](http://www.ogcnetwork.net/SOS_2_0/tutorial)
(the Open Geospatial Consortium standard for Sensor Observation Service). Feel free to drop me a message via
[@kinow](https://twitter.com/kinow) if you find any mistakes or have any suggestions.

## Modeling the tail moviment observation data in SOS

SOS is a standard designed to provide access to observation data. There are several server implementations, such as Kisters KiWIS, 
istSOS and 52North SOS.

The standard mentions and utilises several other standards, such as SensorML, WFS, XML, WMS, etc. The SOS Tutorial on
how to model your observation data for SOS starts by defining *procedure*, *observed property*, *feature of interest*,
*phenomenon and result times*, and the *result value*.

Let's try to model the data from the tail moviment sensors in the following table.

<table class="table table-bordered">
<thead>
<tr>
<th>Name</th>
<th>Description</th>
<th>Our example</th>
</tr>
</thead>
<tbody>
<tr>
<th>Procedure</th>
<td>The process that has generated the observation, such as a sensor, from the O&M specification. In our example that could be a sensor identification</td>
<td>moocall_001</td>
</tr>
<tr>
<th>Observed Property</th>
<td>A property which is observed (look at NASA SWEET ontology for existing values)</td>
<td>Heightned tail moviment</td>
</tr>
<tr>
<th>Feature of Interest</th>
<td>A feature that carries the property which is observed</td>
<td>Pregnant cow</td>
</tr>
<tr>
<th>Phenomenon and Result Times</th>
<td>The phenomenon time is when the data has been taken, and the result time when it has been created. If both are the same, the resultTime can point to the phenomenonTime</td>
<td>20150623142000</td>
</tr>
<tr>
<th>Result value</th>
<td>This is the result of the observation. Can be a OM_Measurement if numeric, OM_TruthObservation, etc (O&M)</td>
<td>3 (supposing we have a scale from 1 to 5)</td>
</tr>
</tbody>
</table>

In the next post I will try to show how to load this model and some dummy data into a fresh installation of
52North SOS server.
