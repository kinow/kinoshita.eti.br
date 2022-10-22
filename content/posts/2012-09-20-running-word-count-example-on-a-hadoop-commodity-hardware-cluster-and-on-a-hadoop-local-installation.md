---
categories:
- blog
date: "2012-09-20T00:00:00Z"
tags:
- big data
title: Running word-count example on a Hadoop commodity-hardware cluster and on a
  Hadoop local installation
---

<p>Last weekend I spent some hours assembling old computer parts to create my commodity hardware cluster for running Hadoop. I already had a local installation in my notebook, so I thought it would be cool to run the word-count example in both scenarios to see what would be the results.</p>

<p>But first, let's review the hardware configurations:</p>

<!--more-->

<hr />

<h2>Cluster set up</h2>

<h4>devcluster01 (NameNode)</h4>
<ul>
<li>Intel Core 2 Duo 2.3 GHz</li>
<li>4 GB</li>
<li>200 GB</li>
<li>100 Mbps Full Duplex network card</li>
</ul>

<h4>devcluster02</h4>
<ul>
<li>AMD Athlon 1.6 GHz</li>
<li>500 MB</li>
<li>4 GB</li>
<li>100 Mbps Full Duplex network card</li>
</ul>

<h4>devcluster03</h4>
<ul>
<li>Celeron 1.3 GHz</li>
<li>300MB</li>
<li>10 GB</li>
<li>100 Mbps Full Duplex network card</li>
</ul>

<h4>devcluster04 (TaskTracker)</h4>
<ul>
<li>Celeron 2.26 GHz</li>
<li>512 MB</li>
<li>80 GB</li>
<li>100 Mbps Full Duplex network card</li>
</ul>

<h4>devcluster05</h4>
<ul>
<li>AMD Duron 1.1 GHz</li>
<li>512MB</li>
<li>40 GB</li>
<li>100 Mbps Full Duplex network card</li>
</ul>

<h4>Network</h4>

<ul>
<li>Ethernet 10/100 D-Link hub</li>
</ul>

<hr />

<h2>Standalone installation</h2>

<ul>
<li>Intel Core i5 2.3 GHz (quad core)</li>
<li>6 GB</li>
<li>500 GB</li>
</ul>

<hr />

<p>Notice that there is one NameNode (exclusive) and one JobTracker (exclusive too). I'm following the default for a cluster installation, but will try switching a DataNode/TaskTracker with less computing power for the NameNode or the JobTracker (they were randomly selected), and using both servers as DataNode/TaskTracker too.</p>

<p>The word-count example that I used can be found at <a href="http://www.github.com/kinow/hadoop-wordcount" title="http://www.github.com/kinow/hadoop-wordcount">https://github.com/kinow/hadoop-wordcount</a>. And the data used are free e-books from <a href="http://www.gutenberg.org/" title="Gutenberg">Gutenberg project</a>, saved as text plain UTF-8.</p>

<p>First I used the default data from this <a href="http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-single-node-cluster/#Copy_local_example_data_to_HDFS" title="Hadoop Tutorial">tutorial</a>, that includes only three books. Then I increased to 8 books. Not happy with the result I tried 30, and finally 66 books. You can get the data from the same GitHub repository mentioned above.</p>

<p>Using the web interface I retrieved the total time to execute each job, and using the following R script, plotted the graph below (for more on plotting R graphs, check this <a href="http://www.harding.edu/fmccown/r/" title="Link">link</a>).</p>

```r
a1 = c(73, 75, 132, 248) # time in the cluster
a2 = c(40, 48, 121, 224) # time running locally
files = c(3, 8, 30, 66) # number of files used
plot(x=files, xlab="Number of files", y=a1, ylab="Time (s)", col="red", type="o") # plot cluster line
lines(y= a2, x=files, type="o", pch=22, lty=2, col="blue") # add the local line
title(main="Hadoop Execution in seconds", col.name="black", font.main=2)
g_range < - range(0, a1, files)
legend(2, g_range[2], c("Cluster","Local"), cex=0.8, col=c("red","blue"), pch=21:22, lty=1:2) #legend
```

<p style="text-align: center"><a href="http://www.kinoshita.eti.br/wp-content/uploads/2012/09/Rplot.png"><img src="http://www.kinoshita.eti.br/wp-content/uploads/2012/09/Rplot.png" alt="" title="Graph" width="550" height="400" class="aligncenter size-full wp-image-1019" /></a></p>

<p><strong>The cluster is running slower than the standalone installation</strong>. During this week I'll investigate how to get better results with the cluster. I have three computers running tasks in the distributed cluster (the other two are the NameNode and JobTracker), and my notebook has four cores. It may be influencing the results. There is also the network latency, low memory in some nodes and changing the NameNode and JobTracker.</p>

<p>All in all, it's been fun to configure the cluster and run the experiments. It is good for practicing with Hadoop and HDFS, as well as getting a better idea on how to manage a cluster.</p></code>

<hr />

<p><em>Edit: JobTracker and TaskTracker were mixed up (thanks rretzbach)</em></p>
