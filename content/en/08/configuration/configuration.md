---
title: Configuration
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

Kafka uses the [property file format](http://en.wikipedia.org/wiki/.properties) for configuration. These can be supplied either from a file or programmatically. 

Some configurations have both a default global setting as well as a topic-level overrides. The topic level properties have the format of csv (e.g., "xyz.per.topic=topic1:value1,topic2:value2") and they override the default value for the specified topics. 

# Broker Configs

The essential configurations are the following: 

  * `broker.id`
  * `log.dirs`
  * `zookeeper.connect` 
Property | Default | Description  
---|---|---  
broker.id |  | Each broker is uniquely identified by a non-negative integer id. This id serves as the brokers "name" and allows the broker to be moved to a different host/port without confusing consumers. You can choose any number you like so long as it is unique.   
log.dirs | /tmp/kafka-logs | A comma-separated list of one or more directories in which Kafka data is stored. Each new partition that is created will be placed in the directory which currently has the fewest partitions.  
port | 6667 | The port on which the server accepts client connections.  
zookeeper.connect | null | Specifies the zookeeper connection string in the form `hostname:port`, where hostname and port are the host and port for a node in your zookeeper cluster. To allow connecting through other zookeeper nodes when that host is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`.  Zookeeper also allows you to add a "chroot" path which will make all kafka data for this cluster appear under a particular path. This is a way to setup multiple Kafka clusters or other applications on the same zookeeper cluster. To do this give a connection string in the form `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path` which would put all this cluster's data under the path `/chroot/path`. Note that you must create this path yourself prior to starting the broker and consumers must use the same connection string.  
message.max.bytes | 1000000 | The maximum size of a message that the server can receive. It is important that this property be in sync with the maximum fetch size your consumers use or else an unruly producer will be able to publish messages too large for consumers to consume.  
num.network.threads | 3 | The number of network threads that the server uses for handling network requests. You probably don't need to change this.  
num.io.threads | 8 | The number of I/O threads that the server uses for executing requests. You should have at least as many threads as you have disks.  
queued.max.requests | 500 | The number of requests that can be queued up for processing by the I/O threads before the network threads stop reading in new requests.  
host.name | null |  Hostname of broker. If this is set, it will only bind to this address. If this is not set, it will bind to all interfaces, and publish one to ZK.  
socket.send.buffer.bytes | 100 * 1024 | The SO_SNDBUFF buffer the server prefers for socket connections.  
socket.receive.buffer.bytes | 100 * 1024 | The SO_RCVBUFF buffer the server prefers for socket connections.  
socket.request.max.bytes | 100 * 1024 * 1024 | The maximum request size the server will allow. This prevents the server from running out of memory and should be smaller than the Java heap size.  
num.partitions | 1 | The default number of partitions per topic.  
log.segment.bytes | 1024 * 1024 * 1024 | The log for a topic partition is stored as a directory of segment files. This setting controls the size to which a segment file will grow before a new segment is rolled over in the log.  
log.segment.bytes.per.topic | "" | This setting allows overriding log.segment.bytes on a per-topic basis.  
log.roll.hours | 24 * 7 | This setting will force Kafka to roll a new log segment even if the log.segment.bytes size has not been reached.  
log.roll.hours.per.topic | "" | This setting allows overriding log.roll.hours on a per-topic basis.  
log.retention.hours | 24 * 7 | The number of hours to keep a log segment before it is deleted, i.e. the default data retention window for all topics. Note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded.  
log.retention.hours.per.topic | "" | A per-topic override for log.retention.hours.  
log.retention.bytes | -1 | The amount of data to retain in the log for each topic-partitions. Note that this is the limit per-partition so multiply by the number of partitions to get the total data retained for the topic. Also note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded.  
log.retention.bytes.per.topic | "" | A per-topic override for log.retention.bytes.  
log.retention.check.interval.ms | 300000 | The frequency in milliseconds that the log cleaner checks whether any log segment is eligible for deletion to meet the retention policies.  
log.index.size.max.bytes | 10 * 1024 * 1024 | The maximum size in bytes we allow for the offset index for each log segment. Note that we will always pre-allocate a sparse file with this much space and shrink it down when the log rolls. If the index fills up we will roll a new log segment even if we haven't reached the log.segment.bytes limit.  
log.index.interval.bytes | 4096 | The byte interval at which we add an entry to the offset index. When executing a fetch request the server must do a linear scan for up to this many bytes to find the correct position in the log to begin and end the fetch. So setting this value to be larger will mean larger index files (and a bit more memory usage) but less scanning. However the server will never add more than one index entry per log append (even if more than log.index.interval worth of messages are appended). In general you probably don't need to mess with this value.  
log.flush.interval.messages | 10000 | The number of messages written to a log partition before we force an fsync on the log. Setting this higher will improve performance a lot but will increase the window of data at risk in the event of a crash (though that is usually best addressed through replication). If both this setting and log.flush.interval.ms are both used the log will be flushed when either criteria is met.  
log.flush.interval.ms.per.topic | "" | The per-topic override for log.flush.interval.messages, e.g., topic1:3000,topic2:6000  
log.flush.scheduler.interval.ms | 3000 | The frequency in ms that the log flusher checks whether any log is eligible to be flushed to disk.  
log.flush.interval.ms | 3000  | The maximum time between fsync calls on the log. If used in conjuction with log.flush.interval.messages the log will be flushed when either criteria is met.  
auto.create.topics.enable | true | Enable auto creation of topic on the server. If this is set to true then attempts to produce, consume, or fetch metadata for a non-existent topic will automatically create it with the default replication factor and number of partitions.  
controller.socket.timeout.ms | 30000 | The socket timeout for commands from the partition management controller to the replicas.  
controller.message.queue.size | 10 | The buffer size for controller-to-broker-channels  
default.replication.factor | 1 | The default replication factor for automatically created topics.  
replica.lag.time.max.ms | 10000 | If a follower hasn't sent any fetch requests for this window of time, the leader will remove the follower from ISR (in-sync replicas) and treat it as dead.  
replica.lag.max.messages | 4000 | If a replica falls more than this many messages behind the leader, the leader will remove the follower from ISR and treat it as dead.  
replica.socket.timeout.ms | 30 * 1000 | The socket timeout for network requests to the leader for replicating data.  
replica.socket.receive.buffer.bytes | 64 * 1024 | The socket receive buffer for network requests to the leader for replicating data.  
replica.fetch.max.bytes | 1024 * 1024 | The number of byes of messages to attempt to fetch for each partition in the fetch requests the replicas send to the leader.  
replica.fetch.wait.max.ms | 500 | The maximum amount of time to wait time for data to arrive on the leader in the fetch requests sent by the replicas to the leader.  
replica.fetch.min.bytes | 1 | Minimum bytes expected for each fetch response for the fetch requests from the replica to the leader. If not enough bytes, wait up to replica.fetch.wait.max.ms for this many bytes to arrive.  
num.replica.fetchers | 1 |  Number of threads used to replicate messages from leaders. Increasing this value can increase the degree of I/O parallelism in the follower broker.  
replica.high.watermark.checkpoint.interval.ms | 5000 | The frequency with which each replica saves its high watermark to disk to handle recovery.  
fetch.purgatory.purge.interval.requests | 10000 | The purge interval (in number of requests) of the fetch request purgatory.  
producer.purgatory.purge.interval.requests | 10000 | The purge interval (in number of requests) of the producer request purgatory.  
zookeeper.session.timeout.ms | 6000 | Zookeeper session timeout. If the server fails to heartbeat to zookeeper within this period of time it is considered dead. If you set this too low the server may be falsely considered dead; if you set it too high it may take too long to recognize a truly dead server.  
zookeeper.connection.timeout.ms | 6000 | The maximum amount of time that the client waits to establish a connection to zookeeper.  
zookeeper.sync.time.ms | 2000 | How far a ZK follower can be behind a ZK leader.  
controlled.shutdown.enable | false | Enable controlled shutdown of the broker. If enabled, the broker will move all leaders on it to some other brokers before shutting itself down. This reduces the unavailability window during shutdown.  
controlled.shutdown.max.retries | 3 | Number of retries to complete the controlled shutdown successfully before executing an unclean shutdown.  
controlled.shutdown.retry.backoff.ms | 5000 | Backoff time between shutdown retries.  
  
More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.

# Consumer Configs

The essential consumer configurations are the following: 

  * `group.id`
  * `zookeeper.connect` 
Property | Default | Description  
---|---|---  
group.id |  | A string that uniquely identifies the group of consumer processes to which this consumer belongs. By setting the same group id multiple processes indicate that they are all part of the same consumer group.  
zookeeper.connect |  | Specifies the zookeeper connection string in the form `hostname:port` where host and port are the host and port of a zookeeper server. To allow connecting through other zookeeper nodes when that zookeeper machine is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`.  The server may also have a zookeeper chroot path as part of it's zookeeper connection string which puts its data under some path in the global zookeeper namespace. If so the consumer should use the same chroot path in its connection string. For example to give a chroot path of `/chroot/path` you would give the connection string as `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path`.  
consumer.id | null |  Generated automatically if not set.  
socket.timeout.ms | 30 * 1000 | The socket timeout for network requests. The actual timeout set will be max.fetch.wait + socket.timeout.ms.  
socket.receive.buffer.bytes | 64 * 1024 | The socket receive buffer for network requests  
fetch.message.max.bytes | 1024 * 1024 | The number of byes of messages to attempt to fetch for each topic-partition in each fetch request. These bytes will be read into memory for each partition, so this helps control the memory used by the consumer. The fetch request size must be at least as large as the maximum message size the server allows or else it is possible for the producer to send messages larger than the consumer can fetch.  
auto.commit.enable | true | If true, periodically commit to zookeeper the offset of messages already fetched by the consumer. This committed offset will be used when the process fails as the position from which the new consumer will begin.  
auto.commit.interval.ms | 60 * 1000 | The frequency in ms that the consumer offsets are committed to zookeeper.  
queued.max.message.chunks | 10 | Max number of message chunks buffered for consumption. Each chunk can be up to fetch.message.max.bytes.  
rebalance.max.retries | 4 | When a new consumer joins a consumer group the set of consumers attempt to "rebalance" the load to assign partitions to each consumer. If the set of consumers changes while this assignment is taking place the rebalance will fail and retry. This setting controls the maximum number of attempts before giving up.  
fetch.min.bytes | 1 | The minimum amount of data the server should return for a fetch request. If insufficient data is available the request will wait for that much data to accumulate before answering the request.  
fetch.wait.max.ms | 100 | The maximum amount of time the server will block before answering the fetch request if there isn't sufficient data to immediately satisfy fetch.min.bytes  
rebalance.backoff.ms | 2000 | Backoff time between retries during rebalance.  
refresh.leader.backoff.ms | 200 | Backoff time to wait before trying to determine the leader of a partition that has just lost its leader.  
auto.offset.reset | largest |  What to do when there is no initial offset in Zookeeper or if an offset is out of range:  
* smallest : automatically reset the offset to the smallest offset  
* largest : automatically reset the offset to the largest offset  
* anything else: throw exception to the consumer. If this is set to largest, the consumer may lose some messages when the number of partitions, for the topics it subscribes to, changes on the broker. To prevent data loss during partition addition, set auto.offset.reset to smallest  
consumer.timeout.ms | -1 | Throw a timeout exception to the consumer if no message is available for consumption after the specified interval  
client.id | group id value | The client id is a user-specified string sent in each request to help trace calls. It should logically identify the application making the request.  
zookeeper.session.timeout.ms  | 6000 | Zookeeper session timeout. If the consumer fails to heartbeat to zookeeper for this period of time it is considered dead and a rebalance will occur.  
zookeeper.connection.timeout.ms | 6000 | The max time that the client waits while establishing a connection to zookeeper.  
zookeeper.sync.time.ms  | 2000 | How far a ZK follower can be behind a ZK leader  
  
More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.

# Producer Configs

Essential configuration properties for the producer include: 

  * `metadata.broker.list`
  * `request.required.acks`
  * `producer.type`
  * `serializer.class` 
Property | Default | Description  
---|---|---  
metadata.broker.list |  |  This is for bootstrapping and the producer will only use it for getting metadata (topics, partitions and replicas). The socket connections for sending the actual data will be established based on the broker information returned in the metadata. The format is host1:port1,host2:port2, and the list can be a subset of brokers or a VIP pointing to a subset of brokers.  
request.required.acks | 0 |  This value controls when a produce request is considered completed. Specifically, how many other brokers must have committed the data to their log and acknowledged this to the leader? Typical values are 

  * 0, which means that the producer never waits for an acknowledgement from the broker (the same behavior as 0.7). This option provides the lowest latency but the weakest durability guarantees (some data will be lost when a server fails). 
  * 1, which means that the producer gets an acknowledgement after the leader replica has received the data. This option provides better durability as the client waits until the server acknowledges the request as successful (only messages that were written to the now-dead leader but not yet replicated will be lost). 
  * -1, which means that the producer gets an acknowledgement after all in-sync replicas have received the data. This option provides the best durability, we guarantee that no messages will be lost as long as at least one in sync replica remains. 
  
request.timeout.ms | 10000 | The amount of time the broker will wait trying to meet the request.required.acks requirement before sending back an error to the client.  
producer.type | sync |  This parameter specifies whether the messages are sent asynchronously in a background thread. Valid values are (1) async for asynchronous send and (2) sync for synchronous send. By setting the producer to async we allow batching together of requests (which is great for throughput) but open the possibility of a failure of the client machine dropping unsent data. | serializer.class | kafka.serializer.DefaultEncoder | The serializer class for messages. The default encoder takes a byte[] and returns the same byte[].  
key.serializer.class |  | The serializer class for keys (defaults to the same as for messages if nothing is given).  
partitioner.class | kafka.producer.DefaultPartitioner | The partitioner class for partitioning messages amongst sub-topics. The default partitioner is based on the hash of the key.  
compression.codec | none |  This parameter allows you to specify the compression codec for all data generated by this producer. Valid values are "none", "gzip" and "snappy".  
compressed.topics | null |  This parameter allows you to set whether compression should be turned on for particular topics. If the compression codec is anything other than NoCompressionCodec, enable compression only for specified topics if any. If the list of compressed topics is empty, then enable the specified compression codec for all topics. If the compression codec is NoCompressionCodec, compression is disabled for all topics  
message.send.max.retries | 3 |  This property will cause the producer to automatically retry a failed send request. This property specifies the number of retries when such failures occur. Note that setting a non-zero value here can lead to duplicates in the case of network errors that cause a message to be sent but the acknowledgement to be lost.  
retry.backoff.ms | 100 |  Before each retry, the producer refreshes the metadata of relevant topics to see if a new leader has been elected. Since leader election takes a bit of time, this property specifies the amount of time that the producer waits before refreshing the metadata.  
topic.metadata.refresh.interval.ms | 600 * 1000 |  The producer generally refreshes the topic metadata from brokers when there is a failure (partition missing, leader not available...). It will also poll regularly (default: every 10min so 600000ms). If you set this to a negative value, metadata will only get refreshed on failure. If you set this to zero, the metadata will get refreshed after each message sent (not recommended). Important note: the refresh happen only AFTER the message is sent, so if the producer never sends a message the metadata is never refreshed  
queue.buffering.max.ms | 5000 | Maximum time to buffer data when using async mode. For example a setting of 100 will try to batch together 100ms of messages to send at once. This will improve throughput but adds message delivery latency due to the buffering.  
queue.buffering.max.messages | 10000 | The maximum number of unsent messages that can be queued up the producer when using async mode before either the producer must be blocked or data must be dropped.  
queue.enqueue.timeout.ms | -1 |  The amount of time to block before dropping messages when running in async mode and the buffer has reached queue.buffering.max.messages. If set to 0 events will be enqueued immediately or dropped if the queue is full (the producer send call will never block). If set to -1 the producer will block indefinitely and never willingly drop a send.  
batch.num.messages | 200 | The number of messages to send in one batch when using async mode. The producer will wait until either this number of messages are ready to send or queue.buffer.max.ms is reached.  
send.buffer.bytes | 100 * 1024 | Socket write buffer size  
client.id | "" | The client id is a user-specified string sent in each request to help trace calls. It should logically identify the application making the request.  
  
More details about producer configuration can be found in the scala class `kafka.producer.ProducerConfig`.
