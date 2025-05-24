---
title: Configuring a Streams Application
description: 
weight: 2
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Configuring a Streams Application

Kafka and Kafka Streams configuration options must be configured before using Streams. You can configure Kafka Streams by specifying parameters in a `java.util.Properties` instance.

  1. Create a `java.util.Properties` instance.

  2. Set the parameters. For example:
    
        import java.util.Properties;
    import org.apache.kafka.streams.StreamsConfig;
    
    Properties settings = new Properties();
    // Set a few key parameters
    settings.put(StreamsConfig.APPLICATION_ID_CONFIG, "my-first-streams-application");
    settings.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker1:9092");
    // Any further settings
    settings.put(... , ...);
    




# Configuration parameter reference

This section contains the most common Streams configuration parameters. For a full reference, see the [Streams](/22/javadoc/org/apache/kafka/streams/StreamsConfig.html) Javadocs.

  * Required configuration parameters
    * application.id
    * bootstrap.servers
  * Optional configuration parameters
    * default.deserialization.exception.handler
    * default.production.exception.handler
    * default.key.serde
    * default.value.serde
    * num.standby.replicas
    * num.stream.threads
    * partition.grouper
    * processing.guarantee
    * replication.factor
    * state.dir
    * timestamp.extractor
  * Kafka consumers and producer configuration parameters
    * Naming
    * Default Values
    * enable.auto.commit
    * rocksdb.config.setter
  * Recommended configuration parameters for resiliency
    * acks
    * replication.factor



# Required configuration parameters

Here are the required Streams configuration parameters.

Parameter Name | Importance | Description | Default Value  
---|---|---|---  
application.id | Required | An identifier for the stream processing application. Must be unique within the Kafka cluster. | None  
bootstrap.servers | Required | A list of host/port pairs to use for establishing the initial connection to the Kafka cluster. | None  
  
## application.id

> (Required) The application ID. Each stream processing application must have a unique ID. The same ID must be given to all instances of the application. It is recommended to use only alphanumeric characters, `.` (dot), `-` (hyphen), and `_` (underscore). Examples: `"hello_world"`, `"hello_world-v1.0.0"`
> 
> This ID is used in the following places to isolate resources used by the application from others:
> 
>   * As the default Kafka consumer and producer `client.id` prefix
>   * As the Kafka consumer `group.id` for coordination
>   * As the name of the subdirectory in the state directory (cf. `state.dir`)
>   * As the prefix of internal Kafka topic names
> 

> 
> Tip:
>     When an application is updated, the `application.id` should be changed unless you want to reuse the existing data in internal topics and state stores. For example, you could embed the version information within `application.id`, as `my-app-v1.0.0` and `my-app-v1.0.2`.

## bootstrap.servers

> (Required) The Kafka bootstrap servers. This is the same [setting](http://kafka.apache.org/documentation.html#producerconfigs) that is used by the underlying producer and consumer clients to connect to the Kafka cluster. Example: `"kafka-broker1:9092,kafka-broker2:9092"`.
> 
> Tip:
>     Kafka Streams applications can only communicate with a single Kafka cluster specified by this config value. Future versions of Kafka Streams will support connecting to different Kafka clusters for reading input streams and writing output streams.

# Optional configuration parameters

Here are the optional [Streams](/22/javadoc/org/apache/kafka/streams/StreamsConfig.html) javadocs, sorted by level of importance:

>   * High: These parameters can have a significant impact on performance. Take care when deciding the values of these parameters.
>   * Medium: These parameters can have some impact on performance. Your specific environment will determine how much tuning effort should be focused on these parameters.
>   * Low: These parameters have a less general or less significant impact on performance.
> 


Parameter Name | Importance | Description | Default Value  
---|---|---|---  
application.server | Low | A host:port pair pointing to an embedded user defined endpoint that can be used for discovering the locations of state stores within a single Kafka Streams application. The value of this must be different for each instance of the application. | the empty string  
buffered.records.per.partition | Low | The maximum number of records to buffer per partition. | 1000  
cache.max.bytes.buffering | Medium | Maximum number of memory bytes to be used for record caches across all threads. | 10485760 bytes  
client.id | Medium | An ID string to pass to the server when making requests. (This setting is passed to the consumer/producer clients used internally by Kafka Streams.) | the empty string  
commit.interval.ms | Low | The frequency with which to save the position (offsets in source topics) of tasks. | 30000 milliseconds  
default.deserialization.exception.handler | Medium | Exception handling class that implements the `DeserializationExceptionHandler` interface. | `LogAndContinueExceptionHandler`  
default.production.exception.handler | Medium | Exception handling class that implements the `ProductionExceptionHandler` interface. | `DefaultProductionExceptionHandler`  
key.serde | Medium | Default serializer/deserializer class for record keys, implements the `Serde` interface (see also value.serde). | `Serdes.ByteArray().getClass().getName()`  
metric.reporters | Low | A list of classes to use as metrics reporters. | the empty list  
metrics.num.samples | Low | The number of samples maintained to compute metrics. | 2  
metrics.recording.level | Low | The highest recording level for metrics. | `INFO`  
metrics.sample.window.ms | Low | The window of time a metrics sample is computed over. | 30000 milliseconds  
num.standby.replicas | Medium | The number of standby replicas for each task. | 0  
num.stream.threads | Medium | The number of threads to execute stream processing. | 1  
partition.grouper | Low | Partition grouper class that implements the `PartitionGrouper` interface. | See Partition Grouper  
processing.guarantee | Low | The processing mode. Can be either `"at_least_once"` (default) or `"exactly_once"`. | See Processing Guarantee  
poll.ms | Low | The amount of time in milliseconds to block waiting for input. | 100 milliseconds  
replication.factor | High | The replication factor for changelog topics and repartition topics created by the application. | 1  
retries | Medium | The number of retries for broker requests that return a retryable error.  | 0  
retry.backoff.ms | Medium | The amount of time in milliseconds, before a request is retried. This applies if the `retries` parameter is configured to be greater than 0.  | 100  
state.cleanup.delay.ms | Low | The amount of time in milliseconds to wait before deleting state when a partition has migrated. | 600000 milliseconds  
state.dir | High | Directory location for state stores. | `/tmp/kafka-streams`  
timestamp.extractor | Medium | Timestamp extractor class that implements the `TimestampExtractor` interface. | See Timestamp Extractor  
upgrade.from | Medium | The version you are upgrading from during a rolling upgrade. | See Upgrade From  
value.serde | Medium | Default serializer/deserializer class for record values, implements the `Serde` interface (see also key.serde). | `Serdes.ByteArray().getClass().getName()`  
windowstore.changelog.additional.retention.ms | Low | Added to a windows maintainMs to ensure data is not deleted from the log prematurely. Allows for clock drift. | 86400000 milliseconds = 1 day  
  
## default.deserialization.exception.handler

> The default deserialization exception handler allows you to manage record exceptions that fail to deserialize. This can be caused by corrupt data, incorrect serialization logic, or unhandled record types. The implemented exception handler needs to return a `FAIL` or `CONTINUE` depending on the record and the exception thrown. Returning `FAIL` will signal that Streams should shut down and `CONTINUE` will signal that Streams should ignore the issue and continue processing. The following library built-in exception handlers are available:
> 
>   * [LogAndContinueExceptionHandler](/22/javadoc/org/apache/kafka/streams/errors/LogAndContinueExceptionHandler.html): This handler logs the deserialization exception and then signals the processing pipeline to continue processing more records. This log-and-skip strategy allows Kafka Streams to make progress instead of failing if there are records that fail to deserialize.
>   * [LogAndFailExceptionHandler](/22/javadoc/org/apache/kafka/streams/errors/LogAndFailExceptionHandler.html). This handler logs the deserialization exception and then signals the processing pipeline to stop processing more records.
> 

> 
> You can also provide your own customized exception handler besides the library provided ones to meet your needs. For example, you can choose to forward corrupt records into a quarantine topic (think: a "dead letter queue") for further processing. To do this, use the Producer API to write a corrupted record directly to the quarantine topic. To be more concrete, you can create a separate `KafkaProducer` object outside the Streams client, and pass in this object as well as the dead letter queue topic name into the `Properties` map, which then can be retrieved from the `configure` function call. The drawback of this approach is that "manual" writes are side effects that are invisible to the Kafka Streams runtime library, so they do not benefit from the end-to-end processing guarantees of the Streams API:
>     
>     
>                   public class SendToDeadLetterQueueExceptionHandler implements DeserializationExceptionHandler {
>                       KafkaProducer<byte[], byte[]> dlqProducer;
>                       String dlqTopic;
>     
>                       @Override
>                       public DeserializationHandlerResponse handle(final ProcessorContext context,
>                                                                    final ConsumerRecord<byte[], byte[]> record,
>                                                                    final Exception exception) {
>     
>                           log.warn("Exception caught during Deserialization, sending to the dead queue topic; " +
>                               "taskId: {}, topic: {}, partition: {}, offset: {}",
>                               context.taskId(), record.topic(), record.partition(), record.offset(),
>                               exception);
>     
>                           dlqProducer.send(new ProducerRecord<>(dlqTopic, record.timestamp(), record.key(), record.value(), record.headers())).get();
>     
>                           return DeserializationHandlerResponse.CONTINUE;
>                       }
>     
>                       @Override
>                       public void configure(final Map<String, ?> configs) {
>                           dlqProducer = .. // get a producer from the configs map
>                           dlqTopic = .. // get the topic name from the configs map
>                       }
>                   }
>                   

## default.production.exception.handler

> The default production exception handler allows you to manage exceptions triggered when trying to interact with a broker such as attempting to produce a record that is too large. By default, Kafka provides and uses the [DefaultProductionExceptionHandler](/22/javadoc/org/apache/kafka/streams/errors/DefaultProductionExceptionHandler.html) that always fails when these exceptions occur.
> 
> Each exception handler can return a `FAIL` or `CONTINUE` depending on the record and the exception thrown. Returning `FAIL` will signal that Streams should shut down and `CONTINUE` will signal that Streams should ignore the issue and continue processing. If you want to provide an exception handler that always ignores records that are too large, you could implement something like the following:
>     
>     
>                 import java.util.Properties;
>                 import org.apache.kafka.streams.StreamsConfig;
>                 import org.apache.kafka.common.errors.RecordTooLargeException;
>                 import org.apache.kafka.streams.errors.ProductionExceptionHandler;
>                 import org.apache.kafka.streams.errors.ProductionExceptionHandler.ProductionExceptionHandlerResponse;
>     
>                 public class IgnoreRecordTooLargeHandler implements ProductionExceptionHandler {
>                     public void configure(Map<String, Object> config) {}
>     
>                     public ProductionExceptionHandlerResponse handle(final ProducerRecord<byte[], byte[]> record,
>                                                                      final Exception exception) {
>                         if (exception instanceof RecordTooLargeException) {
>                             return ProductionExceptionHandlerResponse.CONTINUE;
>                         } else {
>                             return ProductionExceptionHandlerResponse.FAIL;
>                         }
>                     }
>                 }
>     
>                 Properties settings = new Properties();
>     
>                 // other various kafka streams settings, e.g. bootstrap servers, application id, etc
>     
>                 settings.put(StreamsConfig.DEFAULT_PRODUCTION_EXCEPTION_HANDLER_CLASS_CONFIG,
>                              IgnoreRecordTooLargeHandler.class);

## default.key.serde

> The default Serializer/Deserializer class for record keys. Serialization and deserialization in Kafka Streams happens whenever data needs to be materialized, for example:
>
>>   * Whenever data is read from or written to a _Kafka topic_ (e.g., via the `StreamsBuilder#stream()` and `KStream#to()` methods).
>>   * Whenever data is read from or written to a _state store_.
>> 

>> 
>> This is discussed in more detail in [Data types and serialization](datatypes.html#streams-developer-guide-serdes).

## default.value.serde

> The default Serializer/Deserializer class for record values. Serialization and deserialization in Kafka Streams happens whenever data needs to be materialized, for example:
> 
>   * Whenever data is read from or written to a _Kafka topic_ (e.g., via the `StreamsBuilder#stream()` and `KStream#to()` methods).
>   * Whenever data is read from or written to a _state store_.
> 

> 
> This is discussed in more detail in [Data types and serialization](datatypes.html#streams-developer-guide-serdes).

## num.standby.replicas

> The number of standby replicas. Standby replicas are shadow copies of local state stores. Kafka Streams attempts to create the specified number of replicas per store and keep them up to date as long as there are enough instances running. Standby replicas are used to minimize the latency of task failover. A task that was previously running on a failed instance is preferred to restart on an instance that has standby replicas so that the local state store restoration process from its changelog can be minimized. Details about how Kafka Streams makes use of the standby replicas to minimize the cost of resuming tasks on failover can be found in the [State](../architecture.html#streams_architecture_state) section.

Note

If you enable n standby tasks, you need to provision n+1 `KafkaStreams` instances.

## num.stream.threads

> This specifies the number of stream threads in an instance of the Kafka Streams application. The stream processing code runs in these thread. For more information about Kafka Streams threading model, see [Threading Model](../architecture.html#streams_architecture_threads).

## partition.grouper

> A partition grouper creates a list of stream tasks from the partitions of source topics, where each created task is assigned with a group of source topic partitions. The default implementation provided by Kafka Streams is [DefaultPartitionGrouper](/22/javadoc/org/apache/kafka/streams/processor/DefaultPartitionGrouper.html). It assigns each task with one partition for each of the source topic partitions. The generated number of tasks equals the largest number of partitions among the input topics. Usually an application does not need to customize the partition grouper.

## processing.guarantee

> The processing guarantee that should be used. Possible values are `"at_least_once"` (default) and `"exactly_once"`. Note that if exactly-once processing is enabled, the default for parameter `commit.interval.ms` changes to 100ms. Additionally, consumers are configured with `isolation.level="read_committed"` and producers are configured with `retries=Integer.MAX_VALUE`, `enable.idempotence=true`, and `max.in.flight.requests.per.connection=1` per default. Note that by default exactly-once processing requires a cluster of at least three brokers what is the recommended setting for production. For development you can change this, by adjusting broker setting `transaction.state.log.replication.factor` and `transaction.state.log.min.isr` to the number of broker you want to use. For more details see [Processing Guarantees](../core-concepts#streams_processing_guarantee). 

## replication.factor

> This specifies the replication factor of internal topics that Kafka Streams creates when local states are used or a stream is repartitioned for aggregation. Replication is important for fault tolerance. Without replication even a single broker failure may prevent progress of the stream processing application. It is recommended to use a similar replication factor as source topics.
> 
> Recommendation:
>     Increase the replication factor to 3 to ensure that the internal Kafka Streams topic can tolerate up to 2 broker failures. Note that you will require more storage space as well (3 times more with the replication factor of 3).

## state.dir

> The state directory. Kafka Streams persists local states under the state directory. Each application has a subdirectory on its hosting machine that is located under the state directory. The name of the subdirectory is the application ID. The state stores associated with the application are created under this subdirectory.

## timestamp.extractor

> A timestamp extractor pulls a timestamp from an instance of [ConsumerRecord](/22/javadoc/org/apache/kafka/clients/consumer/ConsumerRecord.html). Timestamps are used to control the progress of streams.
> 
> The default extractor is [FailOnInvalidTimestamp](/22/javadoc/org/apache/kafka/streams/processor/FailOnInvalidTimestamp.html). This extractor retrieves built-in timestamps that are automatically embedded into Kafka messages by the Kafka producer client since [Kafka version 0.10](https://cwiki.apache.org/confluence/display/KAFKA/KIP-32+-+Add+timestamps+to+Kafka+message). Depending on the setting of Kafka's server-side `log.message.timestamp.type` broker and `message.timestamp.type` topic parameters, this extractor provides you with:
> 
>   * **event-time** processing semantics if `log.message.timestamp.type` is set to `CreateTime` aka "producer time" (which is the default). This represents the time when a Kafka producer sent the original message. If you use Kafka's official producer client, the timestamp represents milliseconds since the epoch.
>   * **ingestion-time** processing semantics if `log.message.timestamp.type` is set to `LogAppendTime` aka "broker time". This represents the time when the Kafka broker received the original message, in milliseconds since the epoch.
> 

> 
> The `FailOnInvalidTimestamp` extractor throws an exception if a record contains an invalid (i.e. negative) built-in timestamp, because Kafka Streams would not process this record but silently drop it. Invalid built-in timestamps can occur for various reasons: if for example, you consume a topic that is written to by pre-0.10 Kafka producer clients or by third-party producer clients that don't support the new Kafka 0.10 message format yet; another situation where this may happen is after upgrading your Kafka cluster from `0.9` to `0.10`, where all the data that was generated with `0.9` does not include the `0.10` message timestamps.
> 
> If you have data with invalid timestamps and want to process it, then there are two alternative extractors available. Both work on built-in timestamps, but handle invalid timestamps differently.
> 
>   * [LogAndSkipOnInvalidTimestamp](/22/javadoc/org/apache/kafka/streams/processor/LogAndSkipOnInvalidTimestamp.html): This extractor logs a warn message and returns the invalid timestamp to Kafka Streams, which will not process but silently drop the record. This log-and-skip strategy allows Kafka Streams to make progress instead of failing if there are records with an invalid built-in timestamp in your input data.
>   * [UsePreviousTimeOnInvalidTimestamp](/22/javadoc/org/apache/kafka/streams/processor/UsePreviousTimeOnInvalidTimestamp.html). This extractor returns the record's built-in timestamp if it is valid (i.e. not negative). If the record does not have a valid built-in timestamps, the extractor returns the previously extracted valid timestamp from a record of the same topic partition as the current record as a timestamp estimation. In case that no timestamp can be estimated, it throws an exception.
> 

> 
> Another built-in extractor is [WallclockTimestampExtractor](/22/javadoc/org/apache/kafka/streams/processor/WallclockTimestampExtractor.html). This extractor does not actually "extract" a timestamp from the consumed record but rather returns the current time in milliseconds from the system clock (think: `System.currentTimeMillis()`), which effectively means Streams will operate on the basis of the so-called **processing-time** of events.
> 
> You can also provide your own timestamp extractors, for instance to retrieve timestamps embedded in the payload of messages. If you cannot extract a valid timestamp, you can either throw an exception, return a negative timestamp, or estimate a timestamp. Returning a negative timestamp will result in data loss - the corresponding record will not be processed but silently dropped. If you want to estimate a new timestamp, you can use the value provided via `previousTimestamp` (i.e., a Kafka Streams timestamp estimation). Here is an example of a custom `TimestampExtractor` implementation:
>     
>     
>     import org.apache.kafka.clients.consumer.ConsumerRecord;
>     import org.apache.kafka.streams.processor.TimestampExtractor;
>     
>     // Extracts the embedded timestamp of a record (giving you "event-time" semantics).
>     public class MyEventTimeExtractor implements TimestampExtractor {
>     
>       @Override
>       public long extract(final ConsumerRecord<Object, Object> record, final long previousTimestamp) {
>         // `Foo` is your own custom class, which we assume has a method that returns
>         // the embedded timestamp (milliseconds since midnight, January 1, 1970 UTC).
>         long timestamp = -1;
>         final Foo myPojo = (Foo) record.value();
>         if (myPojo != null) {
>           timestamp = myPojo.getTimestampInMillis();
>         }
>         if (timestamp < 0) {
>           // Invalid timestamp!  Attempt to estimate a new timestamp,
>           // otherwise fall back to wall-clock time (processing-time).
>           if (previousTimestamp >= 0) {
>             return previousTimestamp;
>           } else {
>             return System.currentTimeMillis();
>           }
>         }
>       }
>     
>     }
>     
> 
> You would then define the custom timestamp extractor in your Streams configuration as follows:
>     
>     
>     import java.util.Properties;
>     import org.apache.kafka.streams.StreamsConfig;
>     
>     Properties streamsConfiguration = new Properties();
>     streamsConfiguration.put(StreamsConfig.DEFAULT_TIMESTAMP_EXTRACTOR_CLASS_CONFIG, MyEventTimeExtractor.class);
>     

## upgrade.from

> The version you are upgrading from. It is important to set this config when performing a rolling upgrade to certain versions, as described in the upgrade guide. You should set this config to the appropriate version before bouncing your instances and upgrading them to the newer version. Once everyone is on the newer version, you should remove this config and do a second rolling bounce. It is only necessary to set this config and follow the two-bounce upgrade path when upgrading from below version 2.0. 

# Kafka consumers, producer and admin client configuration parameters

You can specify parameters for the Kafka [consumers](/22/javadoc/org/apache/kafka/clients/consumer/package-summary.html), [producers](/22/javadoc/org/apache/kafka/clients/producer/package-summary.html), and [admin client](/22/javadoc/org/apache/kafka/kafka/clients/admin/package-summary.html) that are used internally. The consumer, producer and admin client settings are defined by specifying parameters in a `StreamsConfig` instance.

In this example, the Kafka [consumer session timeout](/22/javadoc/org/apache/kafka/clients/consumer/ConsumerConfig.html#SESSION_TIMEOUT_MS_CONFIG) is configured to be 60000 milliseconds in the Streams settings:
    
    
    Properties streamsSettings = new Properties();
    // Example of a "normal" setting for Kafka Streams
    streamsSettings.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker-01:9092");
    // Customize the Kafka consumer settings of your Streams application
    streamsSettings.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 60000);
    

## Naming

Some consumer, producer and admin client configuration parameters use the same parameter name, and Kafka Streams library itself also uses some parameters that share the same name with its embedded client. For example, `send.buffer.bytes` and `receive.buffer.bytes` are used to configure TCP buffers; `request.timeout.ms` and `retry.backoff.ms` control retries for client request; `retries` are used to configure how many retries are allowed when handling retriable errors from broker request responses. You can avoid duplicate names by prefix parameter names with `consumer.`, `producer.`, or `admin.` (e.g., `consumer.send.buffer.bytes` and `producer.send.buffer.bytes`).
    
    
    Properties streamsSettings = new Properties();
    // same value for consumer, producer, and admin client
    streamsSettings.put("PARAMETER_NAME", "value");
    // different values for consumer and producer
    streamsSettings.put("consumer.PARAMETER_NAME", "consumer-value");
    streamsSettings.put("producer.PARAMETER_NAME", "producer-value");
    streamsSettings.put("admin.PARAMETER_NAME", "admin-value");
    // alternatively, you can use
    streamsSettings.put(StreamsConfig.consumerPrefix("PARAMETER_NAME"), "consumer-value");
    streamsSettings.put(StreamsConfig.producerPrefix("PARAMETER_NAME"), "producer-value");
    streamsSettings.put(StreamsConfig.adminClientPrefix("PARAMETER_NAME"), "admin-value");
    

You could further separate consumer configuration by adding different prefixes:

  * `main.consumer.` for main consumer which is the default consumer of stream source.
  * `restore.consumer.` for restore consumer which is in charge of state store recovery.
  * `global.consumer.` for global consumer which is used in global KTable construction.



For example, if you only want to set restore consumer config without touching other consumers' settings, you could simply use `restore.consumer.` to set the config.
    
    
    Properties streamsSettings = new Properties();
    // same config value for all consumer types
    streamsSettings.put("consumer.PARAMETER_NAME", "general-consumer-value");
    // set a different restore consumer config. This would make restore consumer take restore-consumer-value,
    // while main consumer and global consumer stay with general-consumer-value
    streamsSettings.put("restore.consumer.PARAMETER_NAME", "restore-consumer-value");
    // alternatively, you can use
    streamsSettings.put(StreamsConfig.restoreConsumerPrefix("PARAMETER_NAME"), "restore-consumer-value");
    

Same applied to `main.consumer.` and `main.consumer.`, if you only want to specify one consumer type config.

Additionally, to configure the internal repartition/changelog topics, you could use the `topic.` prefix, followed by any of the standard topic configs.
    
    
    Properties streamsSettings = new Properties();
    // Override default for both changelog and repartition topics
    streamsSettings.put("topic.PARAMETER_NAME", "topic-value");
    // alternatively, you can use
    streamsSettings.put(StreamsConfig.topicPrefix("PARAMETER_NAME"), "topic-value");
    

## Default Values

Kafka Streams uses different default values for some of the underlying client configs, which are summarized below. For detailed descriptions of these configs, see [Producer Configs](http://kafka.apache.org/0100/documentation.html#producerconfigs) and [Consumer Configs](http://kafka.apache.org/0100/documentation.html#newconsumerconfigs).

Parameter Name | Corresponding Client | Streams Default  
---|---|---  
auto.offset.reset | Global Consumer | none (cannot be changed)  
auto.offset.reset | Restore Consumer | none (cannot be changed)  
auto.offset.reset | Consumer | earliest  
enable.auto.commit | Consumer | false  
linger.ms | Producer | 100  
max.poll.interval.ms | Consumer | Integer.MAX_VALUE  
max.poll.records | Consumer | 1000  
rocksdb.config.setter | Consumer |    
  
## enable.auto.commit

> The consumer auto commit. To guarantee at-least-once processing semantics and turn off auto commits, Kafka Streams overrides this consumer config value to `false`. Consumers will only commit explicitly via _commitSync_ calls when the Kafka Streams library or a user decides to commit the current processing state.

## rocksdb.config.setter

> The RocksDB configuration. Kafka Streams uses RocksDB as the default storage engine for persistent stores. To change the default configuration for RocksDB, implement `RocksDBConfigSetter` and provide your custom class via [rocksdb.config.setter](/22/javadoc/org/apache/kafka/streams/state/RocksDBConfigSetter.html).
> 
> Here is an example that adjusts the memory size consumed by RocksDB.
>     
>     
>         public static class CustomRocksDBConfig implements RocksDBConfigSetter {
>     
>            @Override
>            public void setConfig(final String storeName, final Options options, final Map<String, Object> configs) {
>              // See #1 below.
>              BlockBasedTableConfig tableConfig = new org.rocksdb.BlockBasedTableConfig();
>              tableConfig.setBlockCacheSize(16 * 1024 * 1024L);
>              // See #2 below.
>              tableConfig.setBlockSize(16 * 1024L);
>              // See #3 below.
>              tableConfig.setCacheIndexAndFilterBlocks(true);
>              options.setTableFormatConfig(tableConfig);
>              // See #4 below.
>              options.setMaxWriteBufferNumber(2);
>            }
>         }
>     
>     Properties streamsSettings = new Properties();
>     streamsConfig.put(StreamsConfig.ROCKSDB_CONFIG_SETTER_CLASS_CONFIG, CustomRocksDBConfig.class);
>     
> 
> Notes for example:
>     
> 
>   1. `BlockBasedTableConfig tableConfig = new org.rocksdb.BlockBasedTableConfig();` Reduce block cache size from the default, shown [here](https://github.com/apache/kafka/blob/1.0/streams/src/main/java/org/apache/kafka/streams/state/internals/RocksDBStore.java#L81), as the total number of store RocksDB databases is partitions (40) * segments (3) = 120.
>   2. `tableConfig.setBlockSize(16 * 1024L);` Modify the default [block size](https://github.com/apache/kafka/blob/1.0/streams/src/main/java/org/apache/kafka/streams/state/internals/RocksDBStore.java#L82) per these instructions from the [RocksDB GitHub](https://github.com/facebook/rocksdb/wiki/Memory-usage-in-RocksDB#indexes-and-filter-blocks).
>   3. `tableConfig.setCacheIndexAndFilterBlocks(true);` Do not let the index and filter blocks grow unbounded. For more information, see the [RocksDB GitHub](https://github.com/facebook/rocksdb/wiki/Block-Cache#caching-index-and-filter-blocks).
>   4. `options.setMaxWriteBufferNumber(2);` See the advanced options in the [RocksDB GitHub](https://github.com/facebook/rocksdb/blob/8dee8cad9ee6b70fd6e1a5989a8156650a70c04f/include/rocksdb/advanced_options.h#L103).
> 


# Recommended configuration parameters for resiliency

There are several Kafka and Kafka Streams configuration options that need to be configured explicitly for resiliency in face of broker failures:

Parameter Name | Corresponding Client | Default value | Consider setting to  
---|---|---|---  
acks | Producer | `acks=1` | `acks=all`  
replication.factor | Streams | `1` | `3`  
min.insync.replicas | Broker | `1` | `2`  
  
Increasing the replication factor to 3 ensures that the internal Kafka Streams topic can tolerate up to 2 broker failures. Changing the acks setting to "all" guarantees that a record will not be lost as long as one replica is alive. The tradeoff from moving to the default values to the recommended ones is that some performance and more storage space (3x with the replication factor of 3) are sacrificed for more resiliency.

## acks

> The number of acknowledgments that the leader must have received before considering a request complete. This controls the durability of records that are sent. The possible values are:
> 
>   * `acks=0` The producer does not wait for acknowledgment from the server and the record is immediately added to the socket buffer and considered sent. No guarantee can be made that the server has received the record in this case, and the `retries` configuration will not take effect (as the client won't generally know of any failures). The offset returned for each record will always be set to `-1`.
>   * `acks=1` The leader writes the record to its local log and responds without waiting for full acknowledgement from all followers. If the leader immediately fails after acknowledging the record, but before the followers have replicated it, then the record will be lost.
>   * `acks=all` The leader waits for the full set of in-sync replicas to acknowledge the record. This guarantees that the record will not be lost if there is at least one in-sync replica alive. This is the strongest available guarantee.
> 

> 
> For more information, see the [Kafka Producer documentation](/#producerconfigs).

## replication.factor

> See the description here.
    
    
    Properties streamsSettings = new Properties();
    streamsSettings.put(StreamsConfig.REPLICATION_FACTOR_CONFIG, 3);
    streamsSettings.put(StreamsConfig.topicPrefix(TopicConfig.MIN_IN_SYNC_REPLICAS_CONFIG), 2);
    streamsSettings.put(StreamsConfig.producerPrefix(ProducerConfig.ACKS_CONFIG), "all");
    

[Previous](/22/streams/developer-guide/write-streams) [Next](/22/streams/developer-guide/dsl-api)

  * [Documentation](/documentation)
  * [Kafka Streams](/streams)
  * [Developer Guide](/streams/developer-guide/)


