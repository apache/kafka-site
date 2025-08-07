---
title: API Design
description: API Design
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# API Design

## Producer APIs

The Producer API that wraps the 2 low-level producers - `kafka.producer.SyncProducer` and `kafka.producer.async.AsyncProducer`. 
    
    
    class Producer {
    	
      /* Sends the data, partitioned by key to the topic using either the */
      /* synchronous or the asynchronous producer */
      public void send(kafka.javaapi.producer.ProducerData<K,V> producerData);
    
      /* Sends a list of data, partitioned by key to the topic using either */
      /* the synchronous or the asynchronous producer */
      public void send(java.util.List<kafka.javaapi.producer.ProducerData<K,V>> producerData);
    
      /* Closes the producer and cleans up */	
      public void close();
    
    }
    

The goal is to expose all the producer functionality through a single API to the client. The new producer - 

  * can handle queueing/buffering of multiple producer requests and asynchronous dispatch of the batched data - 

`kafka.producer.Producer` provides the ability to batch multiple produce requests (`producer.type=async`), before serializing and dispatching them to the appropriate kafka broker partition. The size of the batch can be controlled by a few config parameters. As events enter a queue, they are buffered in a queue, until either `queue.time` or `batch.size` is reached. A background thread (`kafka.producer.async.ProducerSendThread`) dequeues the batch of data and lets the `kafka.producer.EventHandler` serialize and send the data to the appropriate kafka broker partition. A custom event handler can be plugged in through the `event.handler` config parameter. At various stages of this producer queue pipeline, it is helpful to be able to inject callbacks, either for plugging in custom logging/tracing code or custom monitoring logic. This is possible by implementing the `kafka.producer.async.CallbackHandler` interface and setting `callback.handler` config parameter to that class. 

  * handles the serialization of data through a user-specified `Encoder` \- 
    
        interface Encoder<T> {
      public Message toMessage(T data);
    }
    

The default is the no-op `kafka.serializer.DefaultEncoder`

  * provides software load balancing through an optionally user-specified `Partitioner` \- 

The routing decision is influenced by the `kafka.producer.Partitioner`. 
    
        interface Partitioner<T> {
       int partition(T key, int numPartitions);
    }
    

The partition API uses the key and the number of available broker partitions to return a partition id. This id is used as an index into a sorted list of broker_ids and partitions to pick a broker partition for the producer request. The default partitioning strategy is `hash(key)%numPartitions`. If the key is null, then a random broker partition is picked. A custom partitioning strategy can also be plugged in using the `partitioner.class` config parameter. 




## Consumer APIs

We have 2 levels of consumer APIs. The low-level "simple" API maintains a connection to a single broker and has a close correspondence to the network requests sent to the server. This API is completely stateless, with the offset being passed in on every request, allowing the user to maintain this metadata however they choose. 

The high-level API hides the details of brokers from the consumer and allows consuming off the cluster of machines without concern for the underlying topology. It also maintains the state of what has been consumed. The high-level API also provides the ability to subscribe to topics that match a filter expression (i.e., either a whitelist or a blacklist regular expression). 

### Low-level API
    
    
    class SimpleConsumer {
    	
      /* Send fetch request to a broker and get back a set of messages. */ 
      public ByteBufferMessageSet fetch(FetchRequest request);
    
      /* Send a list of fetch requests to a broker and get back a response set. */ 
      public MultiFetchResponse multifetch(List<FetchRequest> fetches);
    
      /**
       * Get a list of valid offsets (up to maxSize) before the given time.
       * The result is a list of offsets, in descending order.
       * @param time: time in millisecs,
       *              if set to OffsetRequest$.MODULE$.LATIEST_TIME(), get from the latest offset available.
       *              if set to OffsetRequest$.MODULE$.EARLIEST_TIME(), get from the earliest offset available.
       */
      public long[] getOffsetsBefore(String topic, int partition, long time, int maxNumOffsets);
    }
    

The low-level API is used to implement the high-level API as well as being used directly for some of our offline consumers (such as the hadoop consumer) which have particular requirements around maintaining state. 

### High-level API
    
    
    
    /* create a connection to the cluster */ 
    ConsumerConnector connector = Consumer.create(consumerConfig);
    
    interface ConsumerConnector {
    	
      /**
       * This method is used to get a list of KafkaStreams, which are iterators over
       * MessageAndMetadata objects from which you can obtain messages and their
       * associated metadata (currently only topic).
       *  Input: a map of <topic, #streams>
       *  Output: a map of <topic, list of message streams>
       */
      public Map<String,List<KafkaStream>> createMessageStreams(Map<String,Int> topicCountMap); 
    
      /**
       * You can also obtain a list of KafkaStreams, that iterate over messages
       * from topics that match a TopicFilter. (A TopicFilter encapsulates a
       * whitelist or a blacklist which is a standard Java regex.)
       */
      public List<KafkaStream> createMessageStreamsByFilter(
          TopicFilter topicFilter, int numStreams);
    
      /* Commit the offsets of all messages consumed so far. */
      public commitOffsets()
      
      /* Shut down the connector */
      public shutdown()
    }
    

This API is centered around iterators, implemented by the KafkaStream class. Each KafkaStream represents the stream of messages from one or more partitions on one or more servers. Each stream is used for single threaded processing, so the client can provide the number of desired streams in the create call. Thus a stream may represent the merging of multiple server partitions (to correspond to the number of processing threads), but each partition only goes to one stream. 

The createMessageStreams call registers the consumer for the topic, which results in rebalancing the consumer/broker assignment. The API encourages creating many topic streams in a single call in order to minimize this rebalancing. The createMessageStreamsByFilter call (additionally) registers watchers to discover new topics that match its filter. Note that each stream that createMessageStreamsByFilter returns may iterate over messages from multiple topics (i.e., if multiple topics are allowed by the filter). 
