---
categories:
- blog
date: "2017-03-15T00:00:00Z"
tags:
- aws
- natural language processing
title: Using Google Natural Language API in an AWS Elastic Beanstalk application
---

Besides providing an API for users and developers, Google also provides a series of
(very well-written) client implementation, in several programming languages. That's the
case for Google Storage, Google Vision, and for Google Natural Language API's.

I recently had to use the latter in a POC at work, and ran into an interesting issue with
our AWS Elastic Beanstalk environment.

Google Language API requires that clients authenticate before sending requests. If you use their [google-cloud-java](https://github.com/GoogleCloudPlatform/google-cloud-java), you can define the GOOGLE_APPLICATION_CREDENTIALS. This environment variable must point to a JSON file with the Google Language API credentials.

The issue is that while Google Language API (or more precisely
[google-auth-library-java](https://github.com/google/google-auth-library-java/blob/ae9735c576fd8593636e155ccb26e454576bc2cd/oauth2_http/java/com/google/auth/oauth2/DefaultCredentialsProvider.java#L124))
looks for an environment variable, in Elastic Beanstalk you are able to
specify only system properties (unless you want to try something with ebextensions,
maybe some JNI...).

A workaround for this issue in Google Natural Language API, is to create and pass a
[LanguageServiceSettings](http://googlecloudplatform.github.io/google-cloud-java/0.8.0/apidocs/com/google/cloud/language/spi/v1/LanguageServiceSettings.html)
to your [LanguageServiceClient](http://googlecloudplatform.github.io/google-cloud-java/0.8.0/apidocs/com/google/cloud/language/spi/v1/LanguageServiceClient.html).
This settings object, when created, must be given a
[channel provider](http://googleapis.github.io/gax-java/0.2.0/apidocs/com/google/api/gax/grpc/ChannelProvider.html)
with a [FixedCredentialsProvider](http://googleapis.github.io/gax-java/0.2.0/apidocs/com/google/api/gax/core/FixedCredentialsProvider.html).

Of course reading code is way easier than reading this workaround description.

```java
// File: GoogleNaturalLanguageService.java
// ...
    // envvar or property used to specify the Google Application Credentials
    private final static String GOOGLE_APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS";

    /**
     * Google Natural Language API.
     */
    private LanguageServiceClient languageServiceClient;

    @PostConstruct
    public void init() throws Exception {
        // Elastic Beanstalk supports Properties, not Environment Variables.
        // Google credentials library will load
        // the JSON location for the service to authenticate from an envVar. So
        // we need to fix that here.
        String googleApplicationCredentials = System.getenv(GOOGLE_APPLICATION_CREDENTIALS);
        LOGGER.info(String.format("GOOGLE_APPLICATION_CREDENTIALS in environment variable: %s", googleApplicationCredentials));
        if (StringUtils.isBlank(googleApplicationCredentials)) {
            googleApplicationCredentials = System.getProperty(GOOGLE_APPLICATION_CREDENTIALS);
            LOGGER.info(String.format("GOOGLE_APPLICATION_CREDENTIALS in JVM property: %s", googleApplicationCredentials));
        }

        if (googleApplicationCredentials == null) {
            throw new RuntimeException("Could not locate GOOGLE_APPLICATION_CREDENTIALS variable!");
        }

        final LanguageServiceSettings languageServiceSettings;
        try (InputStream is = new FileInputStream(new File(googleApplicationCredentials))) {
            final GoogleCredentials myCredentials = GoogleCredentials
                    .fromStream(is)
                    .createScoped(
                            Collections.singleton("https://www.googleapis.com/auth/cloud-platform")
                    );
            final CredentialsProvider credentialsProvider = FixedCredentialsProvider.create(myCredentials);

            final InstantiatingChannelProvider channelProvider = LanguageServiceSettings
                    .defaultChannelProviderBuilder()
                    .setCredentialsProvider(credentialsProvider)
                    .build();
            languageServiceSettings = LanguageServiceSettings
                    .defaultBuilder()
                    .setChannelProvider(channelProvider)
                    .build();
        } catch (IOException ioe) {
            LOGGER.error(String.format("IO error creating Google NLP settings: %s", ioe.getMessage()), ioe);
            throw ioe;
        }

        // Create Google API client
        this.languageServiceClient = LanguageServiceClient.create(languageServiceSettings);
    }

    @PreDestroy
    public void destroy() throws Exception {
        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug("Destroying Google NLP API client");
        }
        // Close Google API executors and channels
        this.languageServiceClient.close();
    }
// ...
```

That way you should be able to use the API with AWS Elastic Beanstalk
without having to hack your environment to provide the GOOGLE_APPLICATION_CREDENTIALS
environment variable.

An alternative would be google-auth-library-java to look for an environment variable
*and* a system property. Or maybe Amazon AWS add a way to provide environment variables.

Note also that I included the @PostConstruct and @PreDestroy annotated methods. The
API will start an executor thread pool, so if you do not want to risk to have problems
re-deploying your application, then remember to close your streams.

&hearts; Open Source
