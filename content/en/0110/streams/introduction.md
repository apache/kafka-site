---
title: Introduction
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Kafka Streams API

# The easiest way to write mission-critical real-time applications and microservices with all the benefits of Kafka's server-side cluster technology.

![](/0110/images/streams-welcome.png)

[Write your first app](/0110/streams/tutorial) [Play with demo app](/0110/streams/quickstart)

  * Write standard Java applications
  * Exactly-once processing semantics
  * No seperate processing cluster required
  * Develop on Mac, Linux, Windows
  * Elastic, highly scalable, fault-tolerant
  * Deploy to containers, VMs, bare metal, cloud
  * Equally viable for small, medium, & large use cases
  * Fully integrated with Kafka security



[ ![](/0110/images/icons/documentation.png) ![](/0110/images/icons/documentation--white.png) Developer manual ](/0110/documentation/streams/developer-guide) [ ![](/0110/images/icons/tutorials.png) ![](/0110/images/icons/tutorials--white.png) Tutorials ](/0110/documentation/streams/tutorial) [ ![](/0110/images/icons/architecture.png) ![](/0110/images/icons/architecture--white.png) Concepts ](/0110/documentation/streams/core-concepts)

# Hello Kafka Streams

The code example below implements a WordCount application that is elastic, highly scalable, fault-tolerant, stateful, and ready to run in production at large scale

Java 8+ Java 7 Scala
    
    
                    import org.apache.kafka.common.serialization.Serdes;
                    import org.apache.kafka.streams.KafkaStreams;
                    import org.apache.kafka.streams.StreamsConfig;
                    import org.apache.kafka.streams.kstream.KStream;
                    import org.apache.kafka.streams.kstream.KStreamBuilder;
                    import org.apache.kafka.streams.kstream.KTable;
    
                    import java.util.Arrays;
                    import java.util.Properties;
    
                    public class WordCountApplication {
    
                        public static void main(final String[] args) throws Exception {
                            Properties config = new Properties();
                            config.put(StreamsConfig.APPLICATION_ID_CONFIG, "wordcount-application");
                            config.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker1:9092");
                            config.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
                            config.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    
                            KStreamBuilder builder = new KStreamBuilder();
                            KStream<String, String> textLines = builder.stream("TextLinesTopic");
                            KTable<String, Long> wordCounts = textLines
                                .flatMapValues(textLine -> Arrays.asList(textLine.toLowerCase().split("\W+")))
                                .groupBy((key, word) -> word)
                                .count("Counts");
                            wordCounts.to(Serdes.String(), Serdes.Long(), "WordsWithCountsTopic");
    
                            KafkaStreams streams = new KafkaStreams(builder, config);
                            streams.start();
                        }
    
                    }
                
    
    
                    import org.apache.kafka.common.serialization.Serdes;
                    import org.apache.kafka.streams.KafkaStreams;
                    import org.apache.kafka.streams.StreamsConfig;
                    import org.apache.kafka.streams.kstream.KStream;
                    import org.apache.kafka.streams.kstream.KStreamBuilder;
                    import org.apache.kafka.streams.kstream.KTable;
                    import org.apache.kafka.streams.kstream.KeyValueMapper;
                    import org.apache.kafka.streams.kstream.ValueMapper;
    
                    import java.util.Arrays;
                    import java.util.Properties;
    
                    public class WordCountApplication {
    
                        public static void main(final String[] args) throws Exception {
                            Properties config = new Properties();
                            config.put(StreamsConfig.APPLICATION_ID_CONFIG, "wordcount-application");
                            config.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker1:9092");
                            config.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
                            config.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    
                            KStreamBuilder builder = new KStreamBuilder();
                            KStream<String, String> textLines = builder.stream("TextLinesTopic");
                            KTable<String, Long> wordCounts = textLines
                                .flatMapValues(new ValueMapper<String, Iterable<String>>() {
                                    @Override
                                    public Iterable<String> apply(String textLine) {
                                        return Arrays.asList(textLine.toLowerCase().split("\W+"));
                                    }
                                })
                                .groupBy(new KeyValueMapper<String, String, String>() {
                                    @Override
                                    public String apply(String key, String word) {
                                        return word;
                                    }
                                })
                                .count("Counts");
                            wordCounts.to(Serdes.String(), Serdes.Long(), "WordsWithCountsTopic");
    
                            KafkaStreams streams = new KafkaStreams(builder, config);
                            streams.start();
                        }
    
                    }
                
    
    
                    import java.lang.Long
                    import java.util.Properties
                    import java.util.concurrent.TimeUnit
    
                    import org.apache.kafka.common.serialization._
                    import org.apache.kafka.streams._
                    import org.apache.kafka.streams.kstream.{KStream, KStreamBuilder, KTable}
    
                    import scala.collection.JavaConverters.asJavaIterableConverter
    
                    object WordCountApplication {
    
                        def main(args: Array[String]) {
                            val config: Properties = {
                                val p = new Properties()
                                p.put(StreamsConfig.APPLICATION_ID_CONFIG, "wordcount-application")
                                p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker1:9092")
                                p.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass)
                                p.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass)
                                p
                            }
    
                            val builder: KStreamBuilder = new KStreamBuilder()
                            val textLines: KStream[String, String] = builder.stream("TextLinesTopic")
                            val wordCounts: KTable[String, Long] = textLines
                                .flatMapValues(textLine => textLine.toLowerCase.split("\W+").toIterable.asJava)
                                .groupBy((_, word) => word)
                                .count("Counts")
                            wordCounts.to(Serdes.String(), Serdes.Long(), "WordsWithCountsTopic")
    
                            val streams: KafkaStreams = new KafkaStreams(builder, config)
                            streams.start()
    
                            Runtime.getRuntime.addShutdownHook(new Thread(() => {
                                streams.close(10, TimeUnit.SECONDS)
                            }))
                        }
    
                    }
                

# See how Kafka Streams is being used

![](/0110/images/icons/rabobank.png)

Rabobank is one of the 3 largest banks in the Netherlands. Its digital nervous system, the Business Event Bus, is powered by Apache Kafka and Kafka Streams.  [Learn More](https://www.confluent.io/blog/real-time-financial-alerts-rabobank-apache-kafkas-streams-api/)

![](/0110/images/icons/zalando.png)

As the leading online fashion retailer in Europe, Zalando uses Kafka as an ESB (Enterprise Service Bus), which helps us in transitioning from a monolithic to a micro services architecture. Using Kafka for processing event streams enables our technical team to do near-real time business intelligence. [Learn More](https://kafka-summit.org/sessions/using-kstreams-ktables-calculate-real-time-domain-rankings/)

Previous [Next](/0110/streams/quickstart)

  * [Documentation](/documentation)


