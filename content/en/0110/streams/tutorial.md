---
title: Write a streams app
description: 
weight: 3
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Write your own Streams Applications

In this guide we will start from scratch on setting up your own project to write a stream processing application using Kafka's Streams API. It is highly recommended to read the [quickstart](/0110/streams/quickstart) first on how to run a Streams application written in Kafka Streams if you have not done so. 

## Setting up a Maven Project

We are going to use a Kafka Streams Maven Archetype for creating a Streams project structure with the following commands: 
    
    
            mvn archetype:generate \
                -DarchetypeGroupId=org.apache.kafka \
                -DarchetypeArtifactId=streams-quickstart-java \
                -DarchetypeVersion=0.11.0.2 \
                -DgroupId=streams.examples \
                -DartifactId=streams.examples \
                -Dversion=0.1 \
                -Dpackage=myapps
        

You can use a different value for `groupId`, `artifactId` and `package` parameters if you like. Assuming the above parameter values are used, this command will create a project structure that looks like this: 
    
    
            > tree streams.examples
            streams-quickstart
            |-- pom.xml
            |-- src
                |-- main
                    |-- java
                    |   |-- myapps
                    |       |-- LineSplit.java
                    |       |-- Pipe.java
                    |       |-- WordCount.java
                    |-- resources
                        |-- log4j.properties
        

There are already several example programs written with Streams library under `src/main/java`. Since we are going to start writing such programs from scratch, we can now delete these examples: 
    
    
            > cd streams-quickstart
            > rm src/main/java/myapps/*.java
        

## Writing a first Streams application: Pipe

It's coding time now! Feel free to open your favorite IDE and import this Maven project, or simply open a text editor and create a java file under `src/main/java`. Let's name it `Pipe.java`: 
    
    
            package myapps;
    
            public class Pipe {
    
                public static void main(String[] args) throws Exception {
    
                }
            }
        

We are going to fill in the `main` function to write this pipe program. Note that we will not list the import statements as we go since IDEs can usually add them automatically. However if you are using a text editor you need to manually add the imports, and at the end of this section we'll show the complete code snippet with import statement for you. 

The first step to write a Streams application is to create a `java.util.Properties` map to specify different Streams execution configuration values as defined in `StreamsConfig`. A couple of important configuration values you need to set are: `StreamsConfig.BOOTSTRAP_SERVERS_CONFIG`, which specifies a list of host/port pairs to use for establishing the initial connection to the Kafka cluster, and `StreamsConfig.APPLICATION_ID_CONFIG`, which gives the unique identifier of your Streams application to distinguish itself with other applications talking to the same Kafka cluster: 
    
    
            Properties props = new Properties();
            props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
            props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");    // assuming that the Kafka broker this application is talking to runs on local machine with port 9092
        

In addition, you can customize other configurations in the same map, for example, default serialization and deserialization libraries for the record key-value pairs: 
    
    
            props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
            props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        

For a full list of configurations of Kafka Streams please refer to this [table](/0110/#streamsconfigs). 

Next we will define the computational logic of our Streams application. In Kafka Streams this computational logic is defined as a `topology` of connected processor nodes. We can use a topology builder to construct such a topology, 
    
    
            final KStreamBuilder builder = new KStreamBuilder();
        

And then create a source stream from a Kafka topic named `streams-plaintext-input` using this topology builder: 
    
    
            KStream<String, String> source = builder.stream("streams-plaintext-input");
        

Now we get a `KStream` that is continuously generating records from its source Kafka topic `streams-plaintext-input`. The records are organized as `String` typed key-value pairs. The simplest thing we can do with this stream is to write it into another Kafka topic, say it's named `streams-pipe-output`: 
    
    
            source.to("streams-pipe-output");
        

Note that we can also concatenate the above two lines into a single line as: 
    
    
            builder.stream("streams-plaintext-input").to("streams-pipe-output");
        

we can now construct the Streams client with the two components we have just constructed above: the configuration map and the topology builder object (one can also construct a `StreamsConfig` object from the `props` map and then pass that object to the constructor, `KafkaStreams` have overloaded constructor functions to takes either type). 
    
    
            final KafkaStreams streams = new KafkaStreams(builder, props);
        

By calling its `start()` function we can trigger the execution of this client. The execution won't stop until `close()` is called on this client. We can, for example, add a shutdown hook with a countdown latch to capture a user interrupt and close the client upon terminating this program: 
    
    
            final CountDownLatch latch = new CountDownLatch(1);
    
            // attach shutdown handler to catch control-c
            Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
                @Override
                public void run() {
                    streams.close();
                    latch.countDown();
                }
            });
    
            try {
                streams.start();
                latch.await();
            } catch (Throwable e) {
                System.exit(1);
            }
            System.exit(0);
        

The complete code so far looks like this: 
    
    
            package myapps;
    
            import org.apache.kafka.common.serialization.Serdes;
            import org.apache.kafka.streams.KafkaStreams;
            import org.apache.kafka.streams.StreamsConfig;
            import org.apache.kafka.streams.kstream.KStreamBuilder;
    
            import java.util.Properties;
            import java.util.concurrent.CountDownLatch;
    
            public class Pipe {
    
                public static void main(String[] args) throws Exception {
                    Properties props = new Properties();
                    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
                    props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
                    props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
                    props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    
                    final KStreamBuilder builder = new KStreamBuilder();
    
                    builder.stream("streams-plaintext-input").to("streams-pipe-output");
    
                    final KafkaStreams streams = new KafkaStreams(builder, props);
                    final CountDownLatch latch = new CountDownLatch(1);
    
                    // attach shutdown handler to catch control-c
                    Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
                        @Override
                        public void run() {
                            streams.close();
                            latch.countDown();
                        }
                    });
    
                    try {
                        streams.start();
                        latch.await();
                    } catch (Throwable e) {
                        System.exit(1);
                    }
                    System.exit(0);
                }
            }
        

If you already have the Kafka broker up and running at `localhost:9092`, and the topics `streams-plaintext-input` and `streams-pipe-output` created on that broker, you can run this code in your IDE or on the command line, using Maven: 
    
    
            > mvn clean package
            > mvn exec:java -Dexec.mainClass=myapps.Pipe
        

For detailed instructions on how to run a Streams application and observe its computing results, please read the [Play with a Streams Application](/0110/streams/quickstart) section. We will not talk about this in the rest of this section. 

## Writing a second Streams application: Line Split

We have learned how to construct a Streams client with its two key components: the `StreamsConfig` and `TopologyBuilder`. Now let's move on to add some real processing logic by augmenting the current topology. We can first create another program by first copy the existing `Pipe.java` class: 
    
    
            > cp src/main/java/myapps/Pipe.java src/main/java/myapps/LineSplit.java
        

And change its class name as well as the application id config to distinguish with the original program: 
    
    
            public class Pipe {
    
                public static void main(String[] args) throws Exception {
                    Properties props = new Properties();
                    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-linesplit");
                    // ...
                }
            }
        

Since each of the source stream's record is a `String` typed key-value pair, let's treat the value string as a text line and split it into words with a `FlatMapValues` operator: 
    
    
            KStream<String, String> source = builder.stream("streams-plaintext-input");
            KStream<String, String> words = builder.flatMapValues(new ValueMapper<String, Iterable<String>>() {
                        @Override
                        public Iterable<String> apply(String value) {
                            return Arrays.asList(value.split("\W+"));
                        }
                    });
        

The operator will take the `source` stream as its input, and generate a new stream named `words` by processing each record from its source stream in order and breaking its value string into a list of words, and producing each word as a new record to the output `words` stream. This is a stateless operator that does not need to keep track of any previously received records or processed results. Note if you are using JDK 8 you can use lambda expression and simplify the above code as: 
    
    
            KStream<String, String> source = builder.stream("streams-plaintext-input");
            KStream<String, String> words = source.flatMapValues(value -> Arrays.asList(value.split("\W+")));
        

And finally we can write the word stream back into another Kafka topic, say `streams-linesplit-output`. Again, these two steps can be concatenated as the following (assuming lambda expression is used): 
    
    
            KStream<String, String> source = builder.stream("streams-plaintext-input");
            source.flatMapValues(value -> Arrays.asList(value.split("\W+")))
                  .to("streams-linesplit-output");
        

The complete code looks like this (assuming lambda expression is used): 
    
    
            package myapps;
    
            import org.apache.kafka.common.serialization.Serdes;
            import org.apache.kafka.streams.KafkaStreams;
            import org.apache.kafka.streams.StreamsConfig;
            import org.apache.kafka.streams.kstream.KStreamBuilder;
            import org.apache.kafka.streams.kstream.ValueMapper;
    
            import java.util.Arrays;
            import java.util.Properties;
            import java.util.concurrent.CountDownLatch;
    
            public class LineSplit {
    
                public static void main(String[] args) throws Exception {
                    Properties props = new Properties();
                    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-linesplit");
                    props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
                    props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
                    props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    
                    final KStreamBuilder builder = new KStreamBuilder();
    
                    KStream<String, String> source = builder.stream("streams-plaintext-input");
                    source.flatMapValues(value -> Arrays.asList(value.split("\W+")))
                          .to("streams-linesplit-output");
    
                    final KafkaStreams streams = new KafkaStreams(builder, props);
                    final CountDownLatch latch = new CountDownLatch(1);
    
                    // ... same as Pipe.java below
                }
            }
        

## Writing a third Streams application: Wordcount

Let's now take a step further to add some "stateful" computations to the topology by counting the occurrence of the words split from the source text stream. Following similar steps let's create another program based on the `LineSplit.java` class: 
    
    
            public class WordCount {
    
                public static void main(String[] args) throws Exception {
                    Properties props = new Properties();
                    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-wordcount");
                    // ...
                }
            }
        

In order to count the words we can first modify the `flatMapValues` operator to treat all of them as lower case (assuming lambda expression is used): 
    
    
            source.flatMapValues(new ValueMapper<String, Iterable<String>>() {
                        @Override
                        public Iterable<String> apply(String value) {
                            return Arrays.asList(value.toLowerCase(Locale.getDefault()).split("\W+"));
                        }
                    });
        

In order to do the counting aggregation we have to first specify that we want to key the stream on the value string, i.e. the lower cased word, with a `groupBy` operator. This operator generate a new grouped stream, which can then be aggregated by a `count` operator, which generates a running count on each of the grouped keys: 
    
    
            KTable<String, Long> counts =
            source.flatMapValues(new ValueMapper<String, Iterable<String>>() {
                        @Override
                        public Iterable<String> apply(String value) {
                            return Arrays.asList(value.toLowerCase(Locale.getDefault()).split("\W+"));
                        }
                    })
                  .groupBy(new KeyValueMapper<String, String, String>() {
                       @Override
                       public String apply(String key, String value) {
                           return value;
                       }
                    })
                  .count("Counts");
        

Note that the `count` operator has a `String` typed parameter `Counts`, which stores the running counts that keep being updated as more records are piped and processed from the source Kafka topic. This `Counts` store can be queried in real-time, with details described in the [Developer Manual](/0110/streams/developer-guide#streams_interactive_queries). 

We can also write the `counts` KTable's changelog stream back into another Kafka topic, say `streams-wordcount-output`. Note that this time the value type is no longer `String` but `Long`, so the default serialization classes are not viable for writing it to Kafka anymore. We need to provide overridden serialization methods for `Long` types, otherwise a runtime exception will be thrown: 
    
    
            counts.to(Serdes.String(), Serdes.Long(), "streams-wordcount-output");
        

Note that in order to read the changelog stream from topic `streams-wordcount-output`, one needs to set the value deserialization as `org.apache.kafka.common.serialization.LongDeserializer`. Details of this can be found in the [Play with a Streams Application](/0110/streams/quickstart) section. Assuming lambda expression from JDK 8 can be used, the above code can be simplified as: 
    
    
            KStream<String, String> source = builder.stream("streams-plaintext-input");
            source.flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split("\W+")))
                  .groupBy((key, value) -> value)
                  .count("Counts")
                  .to(Serdes.String(), Serdes.Long(), "streams-wordcount-output");
        

The complete code looks like this (assuming lambda expression is used): 
    
    
            package myapps;
    
            import org.apache.kafka.common.serialization.Serdes;
            import org.apache.kafka.streams.KafkaStreams;
            import org.apache.kafka.streams.StreamsConfig;
            import org.apache.kafka.streams.kstream.KeyValueMapper;
            import org.apache.kafka.streams.kstream.KStreamBuilder;
            import org.apache.kafka.streams.kstream.ValueMapper;
    
            import java.util.Arrays;
            import java.util.Locale;
            import java.util.Properties;
            import java.util.concurrent.CountDownLatch;
    
            public class WordCount {
    
                public static void main(String[] args) throws Exception {
                    Properties props = new Properties();
                    props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-wordcount");
                    props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
                    props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
                    props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    
                    final KStreamBuilder builder = new KStreamBuilder();
    
                    KStream<String, String> source = builder.stream("streams-plaintext-input");
                    source.flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split("\W+")))
                          .groupBy((key, value) -> value)
                          .count("Counts")
                          .to(Serdes.String(), Serdes.Long(), "streams-wordcount-output");
    
                    final KafkaStreams streams = new KafkaStreams(builder, props);
                    final CountDownLatch latch = new CountDownLatch(1);
    
                    // ... same as Pipe.java below
                }
            }
        

[Previous](/0110/streams/quickstart) [Next](/0110/streams/developer-guide)

  * [Documentation](/documentation)
  * [Streams](/streams)


