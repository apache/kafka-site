---
title: API
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

We are in the process of rewritting the JVM clients for Kafka. As of 0.8.2 Kafka includes a newly rewritten Java producer. The next release will include an equivalent Java consumer. These new clients are meant to supplant the existing Scala clients, but for compatability they will co-exist for some time. These clients are available in a seperate jar with minimal dependencies, while the old Scala clients remain packaged with the server. 

# Producer API

As of the 0.8.2 release we encourage all new development to use the new Java producer. This client is production tested and generally both faster and more fully featured than the previous Scala client. You can use this client by adding a dependency on the client jar using the following maven co-ordinates: 
    
    
    	<dependency>
    	    <groupId>org.apache.kafka</groupId>
    	    <artifactId>kafka-clients</artifactId>
    	    <version>0.8.2.0</version>
    	</dependency>
    

Examples showing how to use the producer are given in the [javadocs](/http://kafka.apache.org/082/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html "Kafka 0.8.2 Javadoc"). 

For those interested in the legacy Scala producer api, information can be found [ here](http://kafka.apache.org/081/documentation.html#producerapi). 

# High Level Consumer API
    
    
    class Consumer {
      /**
       *  Create a ConsumerConnector
       *
       *  @param config  at the minimum, need to specify the groupid of the consumer and the zookeeper
       *                 connection string zookeeper.connect.
       */
      public static kafka.javaapi.consumer.ConsumerConnector createJavaConsumerConnector(ConsumerConfig config);
    }
    
    /**
     *  V: type of the message
     *  K: type of the optional key assciated with the message
     */
    public interface kafka.javaapi.consumer.ConsumerConnector {
      /**
       *  Create a list of message streams of type T for each topic.
       *
       *  @param topicCountMap  a map of (topic, #streams) pair
       *  @param decoder a decoder that converts from Message to T
       *  @return a map of (topic, list of  KafkaStream) pairs.
       *          The number of items in the list is #streams. Each stream supports
       *          an iterator over message/metadata pairs.
       */
      public <K,V> Map<String, List<KafkaStream<K,V>>>
        createMessageStreams(Map<String, Integer> topicCountMap, Decoder<K> keyDecoder, Decoder<V> valueDecoder);
    
      /**
       *  Create a list of message streams of type T for each topic, using the default decoder.
       */
      public Map<String, List<KafkaStream<byte[], byte[]>>> createMessageStreams(Map<String, Integer> topicCountMap);
    
      /**
       *  Create a list of message streams for topics matching a wildcard.
       *
       *  @param topicFilter a TopicFilter that specifies which topics to
       *                    subscribe to (encapsulates a whitelist or a blacklist).
       *  @param numStreams the number of message streams to return.
       *  @param keyDecoder a decoder that decodes the message key
       *  @param valueDecoder a decoder that decodes the message itself
       *  @return a list of KafkaStream. Each stream supports an
       *          iterator over its MessageAndMetadata elements.
       */
      public <K,V> List<KafkaStream<K,V>>
        createMessageStreamsByFilter(TopicFilter topicFilter, int numStreams, Decoder<K> keyDecoder, Decoder<V> valueDecoder);
    
      /**
       *  Create a list of message streams for topics matching a wildcard, using the default decoder.
       */
      public List<KafkaStream<byte[], byte[]>> createMessageStreamsByFilter(TopicFilter topicFilter, int numStreams);
    
      /**
       *  Create a list of message streams for topics matching a wildcard, using the default decoder, with one stream.
       */
      public List<KafkaStream<byte[], byte[]>> createMessageStreamsByFilter(TopicFilter topicFilter);
    
      /**
       *  Commit the offsets of all topic/partitions connected by this connector.
       */
      public void commitOffsets();
    
      /**
       *  Shut down the connector
       */
      public void shutdown();
    }
    
    

You can follow [this example](https://cwiki.apache.org/confluence/display/KAFKA/Consumer+Group+Example "Kafka 0.8 consumer example") to learn how to use the high level consumer api. 

# Simple Consumer API
    
    
    class kafka.javaapi.consumer.SimpleConsumer {
      /**
       *  Fetch a set of messages from a topic.
       *
       *  @param request specifies the topic name, topic partition, starting byte offset, maximum bytes to be fetched.
       *  @return a set of fetched messages
       */
      public FetchResponse fetch(kafka.javaapi.FetchRequest request);
    
      /**
       *  Fetch metadata for a sequence of topics.
       *
       *  @param request specifies the versionId, clientId, sequence of topics.
       *  @return metadata for each topic in the request.
       */
      public kafka.javaapi.TopicMetadataResponse send(kafka.javaapi.TopicMetadataRequest request);
    
      /**
       *  Get a list of valid offsets (up to maxSize) before the given time.
       *
       *  @param request a [[kafka.javaapi.OffsetRequest]] object.
       *  @return a [[kafka.javaapi.OffsetResponse]] object.
       */
      public kafka.javaapi.OffsetResponse getOffsetsBefore(OffsetRequest request);
    
      /**
       * Close the SimpleConsumer.
       */
      public void close();
    }
    

For most applications, the high level consumer Api is good enough. Some applications want features not exposed to the high level consumer yet (e.g., set initial offset when restarting the consumer). They can instead use our low level SimpleConsumer Api. The logic will be a bit more complicated and you can follow the example in [here](https://cwiki.apache.org/confluence/display/KAFKA/0.8.0+SimpleConsumer+Example "Kafka 0.8 SimpleConsumer example"). 

# Kafka Hadoop Consumer API

Providing a horizontally scalable solution for aggregating and loading data into Hadoop was one of our basic use cases. To support this use case, we provide a Hadoop-based consumer which spawns off many map tasks to pull data from the Kafka cluster in parallel. This provides extremely fast pull-based Hadoop data load capabilities (we were able to fully saturate the network with only a handful of Kafka servers). 

Usage information on the hadoop consumer can be found [here](https://github.com/linkedin/camus/). 
