---
title: Configuration
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Configuration 

# Important configuration properties for Kafka broker: 

More details about server configuration can be found in the scala class `kafka.server.KafkaConfig`.

name | default | description  
---|---|---  
`brokerid` | none | Each broker is uniquely identified by an id. This id serves as the brokers "name", and allows the broker to be moved to a different host/port without confusing consumers.  
`enable.zookeeper` | true | enable zookeeper registration in the server  
`log.flush.interval` | 500 | Controls the number of messages accumulated in each topic (partition) before the data is flushed to disk and made available to consumers.  
`log.default.flush.scheduler.interval.ms` | 3000 | Controls the interval at which logs are checked to see if they need to be flushed to disk. A background thread will run at a frequency specified by this parameter and will check each log to see if it has exceeded its flush.interval time, and if so it will flush it.  
`log.default.flush.interval.ms` | log.default.flush.scheduler.interval.ms | Controls the maximum time that a message in any topic is kept in memory before flushed to disk. The value only makes sense if it's a multiple of `log.default.flush.scheduler.interval .ms`  
`topic.flush.intervals.ms` | none | Per-topic overrides for `log.default.flush.interval.ms`. Controls the maximum time that a message in selected topics is kept in memory before flushed to disk. The per-topic value only makes sense if it's a multiple of `log.default.flush.scheduler.interval.ms`. E.g., topic1:1000,topic2:2000  
`log.retention.hours` | 168 | Controls how long a log file is retained.  
`topic.log.retention.hours` | none | Topic-specific retention time that overrides `log.retention.hours`, e.g., topic1:10,topic2:20  
`log.retention.size` | -1 | the maximum size of the log before deleting it. This controls how large a log is allowed to grow  
`log.cleanup.interval.mins` | 10 | Controls how often the log cleaner checks logs eligible for deletion. A log file is eligible for deletion if it hasn't been modified for `log.retention.hours` hours.  
`log.dir` | none | Specifies the root directory in which all log data is kept.  
`log.file.size` | 1*1024*1024*1024 | Controls the maximum size of a single log file.  
`log.roll.hours` | 24 * 7 | The maximum time before a new log segment is rolled out  
`max.socket.request.bytes` | 104857600 | the maximum number of bytes in a socket request  
`monitoring.period.secs` | 600 | the interval in which to measure performance statistics  
`num.threads` | Runtime.getRuntime().availableProcessors | Controls the number of worker threads in the broker to serve requests.  
`num.partitions` | 1 | Specifies the default number of partitions per topic.  
`socket.send.buffer` | 102400 | the SO_SNDBUFF buffer of the socket sever sockets  
`socket.receive.buffer` | 102400 | the SO_RCVBUFF buffer of the socket sever sockets  
`topic.partition.count.map` | none | Override parameter to control the number of partitions for selected topics. E.g., topic1:10,topic2:20  
`zk.connect` | localhost:2182/kafka | Specifies the zookeeper connection string in the form hostname:port/chroot. Here the chroot is a base directory which is prepended to all path operations (this effectively namespaces all kafka znodes to allow sharing with other applications on the same zookeeper cluster)  
`zk.connectiontimeout.ms` | 6000 | Specifies the max time that the client waits to establish a connection to zookeeper.  
`zk.sessiontimeout.ms` | 6000 | The zookeeper session timeout.  
`zk.synctime.ms` | 2000 | Max time for how far a ZK follower can be behind a ZK leader  
  
# Important configuration properties for the high-level consumer: 

More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.

property | default | description  
---|---|---  
`groupid` | groupid | is a string that uniquely identifies a set of consumers within the same consumer group.   
`socket.timeout.ms` | 30000 | controls the socket timeout for network requests   
`socket.buffersize` | 64*1024 | controls the socket receive buffer for network requests  
`fetch.size` | 300 * 1024 | controls the number of bytes of messages to attempt to fetch in one request to the Kafka server  
`backoff.increment.ms` | 1000 | This parameter avoids repeatedly polling a broker node which has no new data. We will backoff every time we get an empty set from the broker for this time period  
`queuedchunks.max` | 100 | the high level consumer buffers the messages fetched from the server internally in blocking queues. This parameter controls the size of those queues  
`autocommit.enable` | true | if set to true, the consumer periodically commits to zookeeper the latest consumed offset of each partition.   
`autocommit.interval.ms` | 10000 | is the frequency that the consumed offsets are committed to zookeeper.   
`autooffset.reset` | smallest | 

  * `smallest`: automatically reset the offset to the smallest offset available on the broker.
  * `largest` : automatically reset the offset to the largest offset available on the broker.
  * `anything else`: throw an exception to the consumer.

  
`consumer.timeout.ms` | -1 | By default, this value is -1 and a consumer blocks indefinitely if no new message is available for consumption. By setting the value to a positive integer, a timeout exception is thrown to the consumer if no message is available for consumption after the specified timeout value.  
`rebalance.retries.max` | 4 | max number of retries during rebalance  
`mirror.topics.whitelist` | "" | Whitelist of topics for this mirror's embedded consumer to consume. At most one of whitelist/blacklist may be specified.  
`mirror.topics.blacklist` | "" | Topics to skip mirroring. At most one of whitelist/blacklist may be specified  
`mirror.consumer.numthreads` | 4 | The number of threads to be used per topic for the mirroring consumer, by default  
  
# Important configuration properties for the producer: 

More details about producer configuration can be found in the scala class `kafka.producer.ProducerConfig`.

property | default | description  
---|---|---  
`serializer.class` | kafka.serializer.DefaultEncoder. This is a no-op encoder. The serialization of data to Message should be handled outside the Producer | class that implements the `kafka.serializer.Encoder<T>` interface, used to encode data of type T into a Kafka message   
`partitioner.class` | `kafka.producer.DefaultPartitioner<T>` \- uses the partitioning strategy `hash(key)%num_partitions`. If key is null, then it picks a random partition.  | class that implements the `kafka.producer.Partitioner<K>`, used to supply a custom partitioning strategy on the message key (of type K) that is specified through the `ProducerData<K, T>` object in the `kafka.producer.Producer<T>` send API  
`producer.type` | sync | this parameter specifies whether the messages are sent asynchronously or not. Valid values are - 

  * `async` for asynchronous batching send through `kafka.producer.AyncProducer`
  * `sync` for synchronous send through `kafka.producer.SyncProducer`

  
`broker.list` | null. Either this parameter or zk.connect needs to be specified by the user. | For bypassing zookeeper based auto partition discovery, use this config to pass in static broker and per-broker partition information. Format-`brokerid1:host1:port1, brokerid2:host2:port2.` If you use this option, the `partitioner.class` will be ignored and each producer request will be routed to a random broker partition.  
`zk.connect` | null. Either this parameter or broker.partition.info needs to be specified by the user | For using the zookeeper based automatic broker discovery, use this config to pass in the zookeeper connection url to the zookeeper cluster where the Kafka brokers are registered.  
`buffer.size` | 102400 | the socket buffer size, in bytes  
`connect.timeout.ms` | 5000 | the maximum time spent by `kafka.producer.SyncProducer` trying to connect to the kafka broker. Once it elapses, the producer throws an ERROR and stops.  
`socket.timeout.ms` | 30000 | The socket timeout in milliseconds  
`reconnect.interval` | 30000 | the number of produce requests after which `kafka.producer.SyncProducer` tears down the socket connection to the broker and establishes it again; this and the following property are mainly used when the producer connects to the brokers through a VIP in a load balancer; they give the producer a chance to pick up the new broker periodically  
`reconnect.time.interval.ms` | 10 * 1000 * 1000 | the amount of time after which `kafka.producer.SyncProducer` tears down the socket connection to the broker and establishes it again; negative reconnect time interval means disabling this time-based reconnect feature  
`max.message.size` | 1000000 | the maximum number of bytes that the kafka.producer.SyncProducer can send as a single message payload  
`compression.codec` | 0 (No compression) | This parameter allows you to specify the compression codec for all data generated by this producer.  
`compressed.topics` | null | This parameter allows you to set whether compression should be turned on for particular topics. If the compression codec is anything other than NoCompressionCodec, enable compression only for specified topics if any. If the list of compressed topics is empty, then enable the specified compression codec for all topics. If the compression codec is NoCompressionCodec, compression is disabled for all topics.   
`zk.read.num.retries` | 3 | The producer using the zookeeper software load balancer maintains a ZK cache that gets updated by the zookeeper watcher listeners. During some events like a broker bounce, the producer ZK cache can get into an inconsistent state, for a small time period. In this time period, it could end up picking a broker partition that is unavailable. When this happens, the ZK cache needs to be updated. This parameter specifies the number of times the producer attempts to refresh this ZK cache.  
Options for Asynchronous Producers (`producer.type=async`)   
`queue.time` | 5000 | maximum time, in milliseconds, for buffering data on the producer queue. After it elapses, the buffered data in the producer queue is dispatched to the `event.handler`.  
`queue.size` | 10000 | the maximum size of the blocking queue for buffering on the ` kafka.producer.AsyncProducer`  
`batch.size` | 200 | the number of messages batched at the producer, before being dispatched to the `event.handler`  
`event.handler` | `kafka.producer.async.EventHandler<T>` | the class that implements `kafka.producer.async.IEventHandler<T>` used to dispatch a batch of produce requests, using an instance of `kafka.producer.SyncProducer`.   
`event.handler.props` | null | the `java.util.Properties()` object used to initialize the custom `event.handler` through its `init()` API  
`callback.handler` | `null` | the class that implements `kafka.producer.async.CallbackHandler<T>` used to inject callbacks at various stages of the `kafka.producer.AsyncProducer` pipeline.   
`callback.handler.props` | null | the `java.util.Properties()` object used to initialize the custom `callback.handler` through its `init()` API
