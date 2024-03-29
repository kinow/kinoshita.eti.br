---
categories:
- blog
date: "2011-12-30T00:00:00Z"
tags:
- jenkins
- test anything protocol
- software quality
title: Testing shell code and producing TAP using Jenkins?
---

Definitely reading <a title="Hacker News" href="http://news.ycombinator.com/">Hacker News</a> before going to bed is a bad idea :-) Same goes for <a title="Reddit" href="http://www.reddit.com">Reddit</a>. So, I found a link about <a title="Bats" href="https://github.com/sstephenson/bats">Bats</a>, a tool to execute tests in Shell and output <a title="Test Anything Protocol" href="http://testanything.org">TAP</a> - Test Anything Protocol. Then I thought; why not ask the author to include Bats under the list of <a title="TAP Producers" href="http://testanything.org/wiki/index.php/TAP_Producers#SH_.2F_Shell_Script">Producers</a> in <a title="Test Anything Protocol" href="http://testanything.org">testanything.org</a>?

But you know what? Why not execute execute locally first to check if that's working... moreover, why not use <a title="Jenkins TAP Plug-in" href="https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin">Jenkins TAP Plug-in</a> and see what happens?

<!--more-->

Here's what is necessary.
<ul>
	<li><a title="Jenkins CI" href="http://www.jenkins-ci.org">Jenkins</a> (duh)</li>
	<li><a title="Jenkins TAP Plug-in" href="https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin">tap plug-in</a></li>
	<li><a title="Jenkins Git Plugin" href="https://wiki.jenkins-ci.org/display/JENKINS/git+Plugin">git plug-in</a></li>
	<li><a title="Bast git repository" href="https://github.com/sstephenson/bats">Bats git repository URL</a></li>
	<li><a title="Baden Baden" href="http://www.badenbaden.com.br/">Baden Baden Red Ale beer</a> (it's Friday, almost new years' eve, c'mon)</li>
</ul>
<!--more-->
Install Jenkins, tap plug-in and git plug-in. Create a new free style build. Add Bats git repository url under SCM. This way Jenkins will retrieve Bats code from Github (you don't need to install it if you don't want to). Add a build step which executes the following shell code: <tt>./bin/bats test/bats.bats &gt; test.t</tt>

{{< showimage
  image="Screenshot_at_2011_12_30_233256.png"
  alt=""
  caption=""
  style=""
>}}

Before executing the build, you have to check the option to publish TAP results in the end of the configuration screen. That's it. Execute your job, chug the remaining of your beer and now you can go to bed... or just refresh Hacker News and Reddit once more...

{{< showimage
  image="Screenshot_at_2011_12_30_233313.png"
  alt=""
  caption=""
  style=""
>}}

{{< showimage
  image="Screenshot_at_2011_12_30_233323.png"
  alt=""
  caption=""
  style=""
>}}

Bats is a very nice TAP producer for Shell. Haven't had time to play with the other producers for Shell, or explore Bats thoroughly, but it looks very promising. Hope to see more people writing tests for shell code.

Cheers -B
