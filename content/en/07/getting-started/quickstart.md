---
title: Quick Start
description: 
weight: 3
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Quick Start

# Step 1: Download the code 

[Download](../downloads.html "Kafka downloads") a recent stable release. 
    
    
    **> tar xzf kafka-<VERSION>.tgz**
    **> cd kafka-<VERSION>**
    **> ./sbt update**
    **> ./sbt package**
    

# Step 2: Start the server

Kafka brokers and consumers use this for co-ordination. 

First start the zookeeper server. You can use the convenience script packaged with kafka to get a quick-and-dirty single-node zookeeper instance. 
    
    
    **> bin/zookeeper-server-start.sh config/zookeeper.properties**
    [2010-11-21 23:45:02,335] INFO Reading configuration from: config/zookeeper.properties
    ...
    

Now start the Kafka server: 
    
    
    **> bin/kafka-server-start.sh config/server.properties**
    jkreps-mn-2:kafka-trunk jkreps$ bin/kafka-server-start.sh config/server.properties
    [2010-11-21 23:51:39,608] INFO starting log cleaner every 60000 ms (kafka.log.LogManager)
    [2010-11-21 23:51:39,628] INFO connecting to ZK: localhost:2181 (kafka.server.KafkaZooKeeper)
    ...
    

# Step 3: Send some messages

Kafka comes with a command line client that will take input from standard in and send it out as messages to the Kafka cluster. By default each line will be sent as a separate message. The topic _test_ is created automatically when messages are sent to it. Omitting logging you should see something like this: 
    
    
    > **bin/kafka-console-producer.sh --zookeeper localhost:2181 --topic test**
    This is a message
    This is another message
    

# Step 4: Start a consumer

Kafka also has a command line consumer that will dump out messages to standard out. 
    
    
    **> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning**
    This is a message
    This is another message
    

If you have each of the above commands running in a different terminal then you should now be able to type messages into the producer terminal and see them appear in the consumer terminal. 

Both of these command line tools have additional options. Running the command with no arguments will display usage information documenting them in more detail. 

# Step 5: Write some code

Below is some very simple examples of using Kafka for sending messages, more complete examples can be found in the Kafka source code in the examples/ directory. 

## Producer Code

### Producer API 

Here are examples of using the producer API - `kafka.producer.Producer<T>` \- 

  1. First, start a local instance of the zookeeper server 
    
        ./bin/zookeeper-server-start.sh config/zookeeper.properties

  2. Next, start a kafka broker 
    
        ./bin/kafka-server-start.sh config/server.properties

  3. Now, create the producer with all configuration defaults and use zookeeper based broker discovery. 
    
        import java.util.Arrays;
    import java.util.List;
    import java.util.Properties;
    import kafka.javaapi.producer.SyncProducer;
    import kafka.javaapi.message.ByteBufferMessageSet;
    import kafka.message.Message;
    import kafka.producer.SyncProducerConfig;
    
    ...
    
    Properties props = new Properties();
    props.put(“zk.connect”, “127.0.0.1:2181”);
    props.put("serializer.class", "kafka.serializer.StringEncoder");
    ProducerConfig config = new ProducerConfig(props);
    Producer<String, String> producer = new Producer<String, String>(config);
    

  4. Send a single message 
    
        // The message is sent to a randomly selected partition registered in ZK
    ProducerData<String, String> data = new ProducerData<String, String>("test-topic", "test-message");
    producer.send(data);
    

  5. Send multiple messages to multiple topics in one request 
    
        List<String> messages = new java.util.ArrayList<String>();
    messages.add("test-message1");
    messages.add("test-message2");
    ProducerData<String, String> data1 = new ProducerData<String, String>("test-topic1", messages);
    ProducerData<String, String> data2 = new ProducerData<String, String>("test-topic2", messages);
    List<ProducerData<String, String>> dataForMultipleTopics = new ArrayList<ProducerData<String, String>>();
    dataForMultipleTopics.add(data1);
    dataForMultipleTopics.add(data2);
    producer.send(dataForMultipleTopics);
    

  6. Send a message with a partition key. Messages with the same key are sent to the same partition 
    
        ProducerData<String, String> data = new ProducerData<String, String>("test-topic", "test-key", "test-message");
    producer.send(data);
    

  7. Use your custom partitioner 

If you are using zookeeper based broker discovery, `kafka.producer.Producer<T>` routes your data to a particular broker partition based on a `kafka.producer.Partitioner<T>`, specified through the `partitioner.class` config parameter. It defaults to `kafka.producer.DefaultPartitioner`. If you don't supply a partition key, then it sends each request to a random broker partition.
    
        class MemberIdPartitioner extends Partitioner[MemberIdLocation] {
      def partition(data: MemberIdLocation, numPartitions: Int): Int = {
        (data.location.hashCode % numPartitions)
      }
    }
    // create the producer config to plug in the above partitioner
    Properties props = new Properties();
    props.put(“zk.connect”, “127.0.0.1:2181”);
    props.put("serializer.class", "kafka.serializer.StringEncoder");
    props.put("partitioner.class", "xyz.MemberIdPartitioner");
    ProducerConfig config = new ProducerConfig(props);
    Producer<String, String> producer = new Producer<String, String>(config);
    

  8. Use custom Encoder 

The producer takes in a required config parameter `serializer.class` that specifies an `Encoder<T>` to convert T to a Kafka Message. Default is the no-op kafka.serializer.DefaultEncoder. Here is an example of a custom Encoder -
    
        class TrackingDataSerializer extends Encoder<TrackingData> {
      // Say you want to use your own custom Avro encoding
      CustomAvroEncoder avroEncoder = new CustomAvroEncoder();
      def toMessage(event: TrackingData):Message = {
    	new Message(avroEncoder.getBytes(event));
      }
    }
    

If you want to use the above Encoder, pass it in to the "serializer.class" config parameter 
    
        Properties props = new Properties();
    props.put("serializer.class", "xyz.TrackingDataSerializer");
    

  9. Using static list of brokers, instead of zookeeper based broker discovery 

Some applications would rather not depend on zookeeper. In that case, the config parameter `broker.list` can be used to specify the list of all brokers in the Kafka cluster.- the list of all brokers in your Kafka cluster in the following format - `broker_id1:host1:port1, broker_id2:host2:port2...`
    
        // you can stop the zookeeper instance as it is no longer required
    ./bin/zookeeper-server-stop.sh
    // create the producer config object 
    Properties props = new Properties();
    props.put(“broker.list”, “0:localhost:9092”);
    props.put("serializer.class", "kafka.serializer.StringEncoder");
    ProducerConfig config = new ProducerConfig(props);
    // send a message using default partitioner 
    Producer<String, String> producer = new Producer<String, String>(config);
    List<String> messages = new java.util.ArrayList<String>();
    messages.add("test-message");
    ProducerData<String, String> data = new ProducerData<String, String>("test-topic", messages);
    producer.send(data);
    

  10. Use the asynchronous producer along with GZIP compression. This buffers writes in memory until either `batch.size` or `queue.time` is reached. After that, data is sent to the Kafka brokers 
    
        Properties props = new Properties();
    props.put("zk.connect"‚ "127.0.0.1:2181");
    props.put("serializer.class", "kafka.serializer.StringEncoder");
    props.put("producer.type", "async");
    props.put("compression.codec", "1");
    ProducerConfig config = new ProducerConfig(props);
    Producer<String, String> producer = new Producer<String, String>(config);
    ProducerData<String, String> data = new ProducerData<String, String>("test-topic", "test-message");
    producer.send(data);
    

  11. Finally, the producer should be closed, through 
    
        producer.close();




### Log4j appender 

Data can also be produced to a Kafka server in the form of a log4j appender. In this way, minimal code needs to be written in order to send some data across to the Kafka server. Here is an example of how to use the Kafka Log4j appender - Start by defining the Kafka appender in your log4j.properties file. 
    
    
    // define the kafka log4j appender config parameters
    log4j.appender.KAFKA=kafka.producer.KafkaLog4jAppender
    // **REQUIRED** : set the hostname of the kafka server
    log4j.appender.KAFKA.Host=localhost
    // **REQUIRED** : set the port on which the Kafka server is listening for connections
    log4j.appender.KAFKA.Port=9092
    // **REQUIRED** : the topic under which the logger messages are to be posted
    log4j.appender.KAFKA.Topic=test
    // the serializer to be used to turn an object into a Kafka message. Defaults to kafka.producer.DefaultStringEncoder
    log4j.appender.KAFKA.Serializer=kafka.test.AppenderStringSerializer
    // do not set the above KAFKA appender as the root appender
    log4j.rootLogger=INFO
    // set the logger for your package to be the KAFKA appender
    log4j.logger.your.test.package=INFO, KAFKA
    

Data can be sent using a log4j appender as follows - 
    
    
    Logger logger = Logger.getLogger([your.test.class])
    logger.info("message from log4j appender");
    

If your log4j appender fails to send messages, please verify that the correct log4j properties file is being used. You can add `-Dlog4j.debug=true` to your VM parameters to verify this. 

## Consumer Code

The consumer code is slightly more complex as it enables multithreaded consumption: 
    
    
    // specify some consumer properties
    Properties props = new Properties();
    props.put("zk.connect", "localhost:2181");
    props.put("zk.connectiontimeout.ms", "1000000");
    props.put("groupid", "test_group");
    
    // Create the connection to the cluster
    ConsumerConfig consumerConfig = new ConsumerConfig(props);
    ConsumerConnector consumerConnector = Consumer.createJavaConsumerConnector(consumerConfig);
    
    // create 4 partitions of the stream for topic “test”, to allow 4 threads to consume
    Map<String, List<KafkaStream<Message>>> topicMessageStreams =
        consumerConnector.createMessageStreams(ImmutableMap.of("test", 4));
    List<KafkaStream<Message>> streams = topicMessageStreams.get("test");
    
    // create list of 4 threads to consume from each of the partitions
    ExecutorService executor = Executors.newFixedThreadPool(4);
    
    // consume the messages in the threads
    for(final KafkaStream<Message> stream: streams) {
      executor.submit(new Runnable() {
        public void run() {
          for(MessageAndMetadata msgAndMetadata: stream) {
            // process message (msgAndMetadata.message())
          }
        }
      });
    }
    

## Hadoop Consumer

Providing a horizontally scalable solution for aggregating and loading data into Hadoop was one of our basic use cases. To support this use case, we provide a Hadoop-based consumer which spawns off many map tasks to pull data from the Kafka cluster in parallel. This provides extremely fast pull-based Hadoop data load capabilities (we were able to fully saturate the network with only a handful of Kafka servers). 

Usage information on the hadoop consumer can be found [here](https://github.com/kafka-dev/kafka/tree/master/contrib/hadoop-consumer). 

## Simple Consumer

Kafka has a lower-level consumer api for reading message chunks directly from servers. Under most circumstances this should not be needed. But just in case, it's usage is as follows: 
    
    
    import kafka.api.FetchRequest;
    import kafka.javaapi.consumer.SimpleConsumer;
    import kafka.javaapi.message.ByteBufferMessageSet;
    import kafka.message.Message;
    import kafka.message.MessageSet;
    import kafka.utils.Utils;
    
    ...
    
    // create a consumer to connect to the kafka server running on localhost, port 9092, socket timeout of 10 secs, socket receive buffer of ~1MB
    SimpleConsumer consumer = new SimpleConsumer("127.0.0.1", 9092, 10000, 1024000);
    
    long offset = 0;
    while (true) {
      // create a fetch request for topic “test”, partition 0, current offset, and fetch size of 1MB
      FetchRequest fetchRequest = new FetchRequest("test", 0, offset, 1000000);
    
      // get the message set from the consumer and print them out
      ByteBufferMessageSet messages = consumer.fetch(fetchRequest);
      for(MessageAndOffset msg : messages) {
        System.out.println("consumed: " + Utils.toString(msg.message.payload(), "UTF-8"));
        // advance the offset after consuming each message
        offset = msg.offset;
      }
    }
    
