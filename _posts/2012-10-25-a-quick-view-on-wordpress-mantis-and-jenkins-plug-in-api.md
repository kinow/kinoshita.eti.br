---
title: 'A quick view on Wordpress, Mantis and Jenkins plug-in API'
id: 1130
author: kinow
tags:
    - jenkins
    - testlink
category: 'blog'
time: '08:49:36'
---
<p>I'm preparing a <em>plug-in API proposal for <a href="http://www.teamst.org" title="TestLink">TestLink</a></em>, and thought that the best way to learn how to write a good plug-in API would be by looking at other application's plug-in API's.</p>

<p style="text-align: center"><img src="{{ assets.testlink_logo_2}} " alt="" title="TestLink" width="283" height="170" class="aligncenter size-full wp-image-1153" /></p>

<p>This post contains information that I gathered for creating this new API, but that may also be useful for other programmers. I used <a href="#wp">Wordpress</a>, <a href="#mantis">Mantis</a> and <a href="#jenkins">Jenkins</a> in this study. Let me know if you find any mistakes or if you have any other suggestions.</p>

<!--more-->

<hr />

<h3><a name="wp">Wordpress</a></h3>

<p><a href="http://www.wordpress.org" title="http://www.wordpress.org">http://www.wordpress.org</a></p>

<p style="text-align: center"><img src="{{ assets.wordpress_logo_notext_rgb_300_300 }}" alt="" title="Wordpress" width="200" height="200" class="aligncenter size-medium wp-image-1156" /></p>

<ul>
	<li>Supported programming languages: PHP</li>
	<li>Configurations available for plug-ins: Yes</li>
	<li>Plug-in packages: Yes (zip)</li>
	<li>Extension points : Action and Filter hooks, and pluggable functions.</li>
</ul>

<h4>Plug-ins installation</h4>

<p>Wordpress has a directory for plug-ins, by default it is <em>$WP_HOME/wp-content/plugins</em>. You can copy the plug-in PHP file, or its directory, or even a zip file to the Wordpress plug-ins folder. Should you copy a zip file, Wordpress decompresses the file for you.</p>

<p>In the Wordpress administration interface you can download and install plug-ins, as well as active, deactivate or uninstall plug-ins. There you can manage plug-in updates, as well as see if the plug-in version is compatible with the current version of Wordpress (users can vote).</p>

<h4>Plug-ins API</h4>

<p>You can get a list of plug-ins in the admin screen of Wordpress. Wordpress can tell whether a plug-in is installed or not, activated or not, using data from database. For each plug-in, Wordpress scans its directory (or include directly a PHP file, if present in the plug-ins folder) and searches for PHP files. What Wordpress is actually looking for, are PHP files that contain comments with information about the plug-in such as name, version, author, etc.</p>

<p>Wordpress provides two hook types, action and filter. The <strong>action hook</strong> is used to execute some action when an event occurs. For instance, you can add an action for when the plug-in is activated.</p>

{% geshi 'php' %}class MyPlugin {
     static function install() {
            // do not generate any output here
     }
}
register_activation_hook( __FILE__, array('MyPlugin', 'install') );{% endgeshi %}

<p>And the <strong>filter hook</strong> is used to modify content. For instance, you could want to modify the title of a post, so you could apply a filter on the function that displays the blog title. This filter could, say, upper case the title.</p>

{% geshi 'php' %}<?php
function theme_slug_filter_the_content( $content ) {
    $custom_content = 'YOUR CONTENT GOES HERE';
    $custom_content .= $content;
    return $custom_content;
}
add_filter( 'the_content', 'theme_slug_filter_the_content' );
?>{% endgeshi %}

<p>There is also the possibility to use <strong>pluggable functions</strong>. With them themes and plug-ins can define functions to be overriden by themes (or child themes) and plug-ins.</p>

{% geshi 'php' %}if ( !function_exists( 'mytheme_nav_menu' ) ) :
function mytheme_nav_menu() {
    if ( current_theme_supports( 'menus' ) ) :
        wp_nav_menu( array( 'theme_location' =&gt; 'primary_nav', 'fallback_cb' =&gt; 'wp_list_pages' ) );
    else :
        wp_list_pages();
    endif;
}
endif;{% endgeshi %}

<h4>Plug-ins configuration</h4>

<p>Plug-in can create tables or use the configurations table in Wordpress. It's also possible to create an admin page to modify these configuration from Wordpress administration section.</p>

<hr />

<h3><a name="mantis">Mantis</a></h3>

<p><a href="http://www.mantisbt.org/" title="http://www.mantisbt.org">http://www.mantisbt.org/</a></p>

<p style="text-align: center"><img src="{{ assets.Mantis_logo }}" alt="" title="Mantis" width="242" height="102" class="aligncenter size-full wp-image-1157" /></p>

<ul>
	<li>Supported programming languages: PHP</li>
	<li>Configurations available for plug-ins: Yes</li>
	<li>Plug-in packages: No</li>
	<li>Extension points : Hooks for events</li>
</ul>

<h4>Plug-ins installation</h4>

<p>The plug-ins installation happens copying the plug-in folder to the plug-ins folder in Mantis. By default, this folder is located at <em>$MANTIS_HOME/plugins</em>.</p>

<h4>Plug-ins API</h4>

<p>Mantis scans the plug-ins folder looking for other folders. For each folder, there should exist a PHP file with the same name of the directory, plus the extension .php. This file must include Mantis plug-ins API (class <em>MantisPlugin.class.php</em>).</p>

<p>The Mantis plug-ins API has general configurations for the plug-in, such as name, description, author, web site, configuration page (optional) among others. As well as functions for initializing and finalizing the plug-in.</p>

<p>By default the plug-in is not persisted in the database, only when installed. During the installation, the initialization functions are called. The plug-in hooks are also registered.</p>

<p>Certain actions in Mantis generate <strong>events</strong> (see: <em>$MANTIS_HOME/core/events_inc.php</em>). A plug-in can register functions for these events. This way, Mantis will call these functions when such event occurs.</p>

{% geshi 'php' %}**
 * requires MantisPlugin.class.php
 */
require_once( config_get( 'class_path' ) . 'MantisPlugin.class.php' );

/**
 * XmlImportExportPlugin Class
 */
class XmlImportExportPlugin extends MantisPlugin {
	
	//...

	/**
	 * Default plugin configuration.
	 */
	function hooks( ) {
		$hooks = array(
			'EVENT_MENU_MANAGE' =&gt; 'import_issues_menu',
			'EVENT_MENU_FILTER' =&gt; 'export_issues_menu',
		);
		return $hooks;
	}
}{% endgeshi %}

<p>There is a plug-in that comes bundled with Mantis, the Core plug-in. This plug-in allows other plug-ins to use it to verify required compatibility with the plug-ins API.</p>

<h4>Plug-ins configuration</h4>

<p>Plug-ins can define a set of configurations, with a default value. If a plug-in provides a configuration page, so it is possible to change these configurations with this page too (the programmer must prepare this page).</p>

<p>If a configuration has a default value, then it is not persisted in the database. But if the administrator changes the configuration, then it is persisted in the database, overriding the default value.</p>

<p>In the database, the configurations are stored in the same table for general configurations, but with the prefix <em>plugin_&lt;pluginname>_&lt;configuration>, e.g.: </em><em>plugin_MantisGraph_font</em> (configuration font of MantisGraph plug-in).</p>

<hr />

<h3><a name="jenkins">Jenkins</a></h3>

<p><a href="http://www.jenkins-ci.org" title="http://www.jenkins-ci.org">http://www.jenkins-ci.org</a></p>

<p style="text-align: center"><img src="{{ assets.Jenkins1_300_224 }}" alt="" title="Jenkins" width="300" height="224" class="aligncenter size-medium wp-image-978" /></p>

<ul>
	<li>Supported programming languages: Java, Ruby, Groovy, Python (work in progress)</li>
	<li>Configurations available for plug-ins: Yes</li>
	<li>Plug-in packages: Yes</li>
	<li>Extension points : An API for plug-ins that combine inheritance, interfaces and annotations</li>
</ul>

<h4>Plug-ins installation</h4>

<p>Plug-ins in Jenkins stay at the <em>$JENKINS_HOME/plugins</em> folder. You can copy the <em>hpi</em> or <em>jpi</em> files into this folder, or copy the plug-in's folder directly in there too. Jenkins will take care of initializing your plug-in, both during Jenkins start up or during runtime.</p>

<p>You can install, update or uninstall using Jenkins interface. You get notifications from the plug-ins updates available and compatibility with Jenkins current version.</p>

<h4>Plug-ins API</h4>

<p>There are several <strong>extension points</strong> in Jenkins (see: <a href="https://wiki.jenkins-ci.org/display/JENKINS/Extension+points" title="Jenkins Wiki page for Extension Points">Jenkins Wiki page for Extension Points</a>). Each one has a goal and is executed at certain point in Jenkins code. Normally your plug-in will have one extension point and one goal, but it is possible too that you use more than one extension point, create your own extension point or use other plug-ins too.</p>

{% geshi 'java' %}public class HelloWorldBuilder extends Builder {

    private final String name;

    // Fields in config.jelly must match the parameter names in the "DataBoundConstructor"
    @DataBoundConstructor
    public HelloWorldBuilder(String name) {
        this.name = name;
    }

    // ...

    @Override
    public boolean perform(AbstractBuild build, Launcher launcher, BuildListener listener) {
        // This is where you 'build' the project.
        // Since this is a dummy, we just say 'hello world' and call that a build.

        // This also shows how you can consult the global configuration of the builder
        if (getDescriptor().getUseFrench())
            listener.getLogger().println(&quot;Bonjour, &quot;+name+&quot;!&quot;);
        else
            listener.getLogger().println(&quot;Hello, &quot;+name+&quot;!&quot;);
        return true;
    }

    // ...

}{% endgeshi %}

<p>When you initialize Jenkins, it scans the plug-ins directory and, for each plug-in found, it prepares a ClassLoader and call the initializion methods (if any) in the plug-in. There are methods for when the plug-in is stopping too.</p>

<p>After that, you can use the plug-ins features from the job configuration screen, or in other parts of the system. In the case of a job, you can use the Builder of a plug-in, for instance, configuring it according to the plug-in requirements, and then during the job execution a method (<em>perform()</em>) is executed for each one of the Builders configured in the job.</p>

<h4>Plug-ins configuration</h4>

<p>Each plug-in can have global of local configurations. It is also possible to modify Jenkins UI and add new screens to configure the plug-in. The configuration screen for the plug-in requires only snippets of <a href="http://commons.apache.org/jelly/" title="Apache Jelly">Jelly</a> or <a href="http://groovy.codehaus.org/" title="Groovy">Groovy</a>, that are embedded by Jenkins in the right configuration screen.</p>

<p>Below is the local (job) configuration for the plug-in shown above.</p>

[xml]&lt;j:jelly xmlns:j=&quot;jelly:core&quot; xmlns:st=&quot;jelly:stapler&quot; xmlns:d=&quot;jelly:define&quot; xmlns:l=&quot;/lib/layout&quot; xmlns:t=&quot;/lib/hudson&quot; xmlns:f=&quot;/lib/form&quot;&gt;
  &lt;f:entry title=&quot;Name&quot; field=&quot;name&quot;&gt;
    &lt;f:textbox /&gt;
  &lt;/f:entry&gt;
&lt;/j:jelly&gt;[/xml]

<hr />

<p>In the next days I'll finish the proposal for TestLink and will post the details here too. And to keep the momentum, I'll investigate an idea posted <a href="http://www.tupilabs.com/2012/10/02/use-jenkins-plug-ins-api-in-apache-nutch.html" title="Use Jenkins plug-ins API in Apache Nutch">here</a>, about enhancing <a href="http://nutch.apache.org" title="Apache Nutch">Apache Nutch</a>'s plug-in API using parts of the Jenkins API.</p>