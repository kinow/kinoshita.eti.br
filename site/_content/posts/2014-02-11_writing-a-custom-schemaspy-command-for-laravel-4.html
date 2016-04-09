---
title: 'Writing a custom SchemaSpy command for Laravel 4'
author: kinow
tags:
    - php
category: 'blog'
time: '13:15:33'
---

This week I had to write my first custom command for [Laravel 4](http://laravel.com/). 
In [Nestor-QA](http://nestor-qa.org/), [Peter](https://github.com/tooh) and I thought it would be useful to have 
the database schema being automatically generated with 
[SchemaSpy](http://schemaspy.sourceforge.net/) in our [Jenkins box](http://builds.tupilabs.com/view/Nestor-QA/).

Thanks to [Artisan](http://laravel.com/docs/artisan) this task is much simpler than I thought. 
The following command creates the <code>schemaspy</code> command.

    php artisan command:make SchemaSpyCommand --command=schemaspy

This will create the file <code>app/commands/SchemaSpyCommand.php</code>. And all I had to do was 
just fill in the options and write the exec command as the [Laravel 4 docs](http://laravel.com/docs/commands) explain. 

    $this->info('Creating SchemaSpy');

	$jar = $this->option("jar");
	$dbtype = $this->option("dbtype");
	$output = $this->option("output");

	$commandLine = sprintf("java -jar %s -u none -t %s -o %s", $jar, $dbtype, $output);

	$this->info(sprintf("Command line: [%s]", $commandLine));

	exec($commandLine);

That's how my final command looks. Now the final step is integrate it into the application by adding the line below to 
<code>app/start/artisan.php</code>.

    Artisan::add(new SchemaSpyCommand);

And that's it, running <code>php artisan schemaspy --jar=/opt/schemaspy/schemaSpy_5.0.0.jar 
--dbtype=app/database/sqlite.properties --output=database-schema</code> 
creates the database schema docs in the <code>database-schema</code> directory. 

Check this [gist](https://gist.github.com/kinow/8936667) for the final code.

Happy coding!