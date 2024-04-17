# How to preview documentation changes locally?

The documentation can be hosted on a local webserver via httpd.

You can run it with the following command, note that it requires docker:

```shell
./start-preview.sh
```

Then you can open [localhost:8080](http://localhost:8080) on your browser and browse the documentation.

To kill the process, just type ctrl + c.

## How to preview the latest documentation changes in Kafka repository?

1. Generating document from kafka repository:

```shell
# change directory into kafka repository
cd KAFKA_REPO
./gradlew clean siteDocTar
# supposing built with scala 2.13
tar zxvf core/build/distributions/kafka_2.13-$(./gradlew properties | grep version: | awk '{print $NF}' | head -n 1)-site-docs.tgz
```

2. Copying the generated documents from Kafka repository into kafka-site, and preview them (note that it requires docker):

```shell
# change directory into kafka-site repository
cd KAFKA_SITE_REPO
# copy the generated documents into dev folder
rm -rf dev
mkdir dev
cp -r KAFKA_REPO/site-docs/* dev
# preview it
./start-preview.sh
```

Then you can open [http://localhost:8080/dev/documentation/](http://localhost:8080/dev/documentation/) on your browser and browse the generated documentation.
