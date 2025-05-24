---
title: Configuration
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

Kafka uses key-value pairs in the [property file format](http://en.wikipedia.org/wiki/.properties) for configuration. These values can be supplied either from a file or programmatically. 

# Broker Configs

The essential configurations are the following: 

  * `broker.id`
  * `log.dirs`
  * `zookeeper.connect` 
Topic-level configurations and defaults are discussed in more detail below.  Property | Default | Description  
---|---|---  
broker.id |  | Each broker is uniquely identified by a non-negative integer id. This id serves as the broker's "name" and allows the broker to be moved to a different host/port without confusing consumers. You can choose any number you like so long as it is unique.   
log.dirs | /tmp/kafka-logs | A comma-separated list of one or more directories in which Kafka data is stored. Each new partition that is created will be placed in the directory which currently has the fewest partitions.  
port | 6667 | The port on which the server accepts client connections.  
zookeeper.connect | null | Specifies the ZooKeeper connection string in the form `hostname:port`, where hostname and port are the host and port for a node in your ZooKeeper cluster. To allow connecting through other ZooKeeper nodes when that host is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`.  ZooKeeper also allows you to add a "chroot" path which will make all kafka data for this cluster appear under a particular path. This is a way to setup multiple Kafka clusters or other applications on the same ZooKeeper cluster. To do this give a connection string in the form `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path` which would put all this cluster's data under the path `/chroot/path`. Note that you must create this path yourself prior to starting the broker and consumers must use the same connection string.  
message.max.bytes | 1000000 | The maximum size of a message that the server can receive. It is important that this property be in sync with the maximum fetch size your consumers use or else an unruly producer will be able to publish messages too large for consumers to consume.  
num.network.threads | 3 | The number of network threads that the server uses for handling network requests. You probably don't need to change this.  
num.io.threads | 8 | The number of I/O threads that the server uses for executing requests. You should have at least as many threads as you have disks.  
background.threads | 4 | The number of threads to use for various background processing tasks such as file deletion. You should not need to change this.  
queued.max.requests | 500 | The number of requests that can be queued up for processing by the I/O threads before the network threads stop reading in new requests.  
host.name | null |  Hostname of broker. If this is set, it will only bind to this address. If this is not set, it will bind to all interfaces, and publish one to ZK.  
advertised.host.name | null |  If this is set this is the hostname that will be given out to producers, consumers, and other brokers to connect to.  
advertised.port | null |  The port to give out to producers, consumers, and other brokers to use in establishing connections. This only needs to be set if this port is different from the port the server should bind to.  
socket.send.buffer.bytes | 100 * 1024 | The SO_SNDBUFF buffer the server prefers for socket connections.  
socket.receive.buffer.bytes | 100 * 1024 | The SO_RCVBUFF buffer the server prefers for socket connections.  
socket.request.max.bytes | 100 * 1024 * 1024 | The maximum request size the server will allow. This prevents the server from running out of memory and should be smaller than the Java heap size.  
num.partitions | 1 | The default number of partitions per topic if a partition count isn't given at topic creation time.  
log.segment.bytes | 1024 * 1024 * 1024 | The log for a topic partition is stored as a directory of segment files. This setting controls the size to which a segment file will grow before a new segment is rolled over in the log. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.roll.hours | 24 * 7 | This setting will force Kafka to roll a new log segment even if the log.segment.bytes size has not been reached. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.cleanup.policy | delete | This can take either the value _delete_ or _compact_. If _delete_ is set, log segments will be deleted when they reach the size or time limits set. If _compact_ is set log compaction will be used to clean out obsolete records. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.retention.{minutes,hours} | 7 days | The amount of time to keep a log segment before it is deleted, i.e. the default data retention window for all topics. Note that if both log.retention.minutes and log.retention.bytes are both set we delete a segment when either limit is exceeded. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.retention.bytes | -1 | The amount of data to retain in the log for each topic-partitions. Note that this is the limit per-partition so multiply by the number of partitions to get the total data retained for the topic. Also note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.retention.check.interval.ms | 5 minutes | The period with which we check whether any log segment is eligible for deletion to meet the retention policies.  
log.cleaner.enable | false | This configuration must be set to true for log compaction to run.  
log.cleaner.threads | 1 | The number of threads to use for cleaning logs in log compaction.  
log.cleaner.io.max.bytes.per.second | None | The maximum amount of I/O the log cleaner can do while performing log compaction. This setting allows setting a limit for the cleaner to avoid impacting live request serving.  
log.cleaner.dedupe.buffer.size | 500*1024*1024 | The size of the buffer the log cleaner uses for indexing and deduplicating logs during cleaning. Larger is better provided you have sufficient memory.  
log.cleaner.io.buffer.size | 512*1024 | The size of the I/O chunk used during log cleaning. You probably don't need to change this.  
log.cleaner.io.buffer.load.factor | 0.9 | The load factor of the hash table used in log cleaning. You probably don't need to change this.  
log.cleaner.backoff.ms | 15000 | The interval between checks to see if any logs need cleaning.  
log.cleaner.min.cleanable.ratio | 0.5 | This configuration controls how frequently the log compactor will attempt to clean the log (assuming log compaction is enabled). By default we will avoid cleaning a log where more than 50% of the log has been compacted. This ratio bounds the maximum space wasted in the log by duplicates (at 50% at most 50% of the log could be duplicates). A higher ratio will mean fewer, more efficient cleanings but will mean more wasted space in the log. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.cleaner.delete.retention.ms | 1 day | The amount of time to retain delete tombstone markers for log compacted topics. This setting also gives a bound on the time in which a consumer must complete a read if they begin from offset 0 to ensure that they get a valid snapshot of the final stage (otherwise delete tombstones may be collected before they complete their scan). This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.index.size.max.bytes | 10 * 1024 * 1024 | The maximum size in bytes we allow for the offset index for each log segment. Note that we will always pre-allocate a sparse file with this much space and shrink it down when the log rolls. If the index fills up we will roll a new log segment even if we haven't reached the log.segment.bytes limit. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.index.interval.bytes | 4096 | The byte interval at which we add an entry to the offset index. When executing a fetch request the server must do a linear scan for up to this many bytes to find the correct position in the log to begin and end the fetch. So setting this value to be larger will mean larger index files (and a bit more memory usage) but less scanning. However the server will never add more than one index entry per log append (even if more than log.index.interval worth of messages are appended). In general you probably don't need to mess with this value.  
log.flush.interval.messages | None | The number of messages written to a log partition before we force an fsync on the log. Setting this lower will sync data to disk more often but will have a major impact on performance. We generally recommend that people make use of replication for durability rather than depending on single-server fsync, however this setting can be used to be extra certain.  
log.flush.scheduler.interval.ms | 3000 | The frequency in ms that the log flusher checks whether any log is eligible to be flushed to disk.  
log.flush.interval.ms | None | The maximum time between fsync calls on the log. If used in conjuction with log.flush.interval.messages the log will be flushed when either criteria is met.  
log.delete.delay.ms | 60000 | The period of time we hold log files around after they are removed from the in-memory segment index. This period of time allows any in-progress reads to complete uninterrupted without locking. You generally don't need to change this.  
log.flush.offset.checkpoint.interval.ms | 60000 | The frequency with which we checkpoint the last flush point for logs for recovery. You should not need to change this.  
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
zookeeper.session.timeout.ms | 6000 | ZooKeeper session timeout. If the server fails to heartbeat to ZooKeeper within this period of time it is considered dead. If you set this too low the server may be falsely considered dead; if you set it too high it may take too long to recognize a truly dead server.  
zookeeper.connection.timeout.ms | 6000 | The maximum amount of time that the client waits to establish a connection to zookeeper.  
zookeeper.sync.time.ms | 2000 | How far a ZK follower can be behind a ZK leader.  
controlled.shutdown.enable | false | Enable controlled shutdown of the broker. If enabled, the broker will move all leaders on it to some other brokers before shutting itself down. This reduces the unavailability window during shutdown.  
controlled.shutdown.max.retries | 3 | Number of retries to complete the controlled shutdown successfully before executing an unclean shutdown.  
controlled.shutdown.retry.backoff.ms | 5000 | Backoff time between shutdown retries.  
auto.leader.rebalance.enable | false | If this is enabled the controller will automatically try to balance leadership for partitions among the brokers by periodically returning leadership to the "preferred" replica for each partition if it is available.  
leader.imbalance.per.broker.percentage | 10 | The percentage of leader imbalance allowed per broker. The controller will rebalance leadership if this ratio goes above the configured value per broker.  
leader.imbalance.check.interval.seconds | 300 | The frequency with which to check for leader imbalance.  
offset.metadata.max.bytes | 1024 | The maximum amount of metadata to allow clients to save with their offsets.  
  
More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.

## Topic-level configuration

Configurations pertinent to topics have both a global default as well an optional per-topic override. If no per-topic configuration is given the global default is used. The override can be set at topic creation time by giving one or more `--config` options. This example creates a topic named _my-topic_ with a custom max message size and flush rate: 
    
    
    ** > bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic my-topic --partitions 1 
            --replication-factor 1 --config max.message.bytes=64000 --config flush.messages=1**
    

Overrides can also be changed or set later using the alter topic command. This example updates the max message size for _my-topic_ : 
    
    
    ** > bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic my-topic 
        --config max.message.bytes=128000**
    

To remove an override you can do 
    
    
    ** > bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic my-topic 
        --deleteConfig max.message.bytes**
    

The following are the topic-level configurations. The server's default configuration for this property is given under the Server Default Property heading, setting this default in the server config allows you to change the default given to topics that have no override specified.  Property | Default | Server Default Property | Description  
---|---|---|---  
cleanup.policy | delete | log.cleanup.policy | A string that is either "delete" or "compact". This string designates the retention policy to use on old log segments. The default policy ("delete") will discard old segments when their retention time or size limit has been reached. The "compact" setting will enable log compaction on the topic.  
delete.retention.ms | 86400000 (24 hours) | log.cleaner.delete.retention.ms | The amount of time to retain delete tombstone markers for log compacted topics. This setting also gives a bound on the time in which a consumer must complete a read if they begin from offset 0 to ensure that they get a valid snapshot of the final stage (otherwise delete tombstones may be collected before they complete their scan).  
flush.messages | None | log.flush.interval.messages | This setting allows specifying an interval at which we will force an fsync of data written to the log. For example if this was set to 1 we would fsync after every message; if it were 5 we would fsync after every five messages. In general we recommend you not set this and use replication for durability and allow the operating system's background flush capabilities as it is more efficient. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
flush.ms | None | log.flush.interval.ms | This setting allows specifying a time interval at which we will force an fsync of data written to the log. For example if this was set to 1000 we would fsync after 1000 ms had passed. In general we recommend you not set this and use replication for durability and allow the operating system's background flush capabilities as it is more efficient.  
index.interval.bytes | 4096 | log.index.interval.bytes | This setting controls how frequently Kafka adds an index entry to it's offset index. The default setting ensures that we index a message roughly every 4096 bytes. More indexing allows reads to jump closer to the exact position in the log but makes the index larger. You probably don't need to change this.  
max.message.bytes | 1,000,000 | message.max.bytes | This is largest message size Kafka will allow to be appended to this topic. Note that if you increase this size you must also increase your consumer's fetch size so they can fetch messages this large.  
min.cleanable.dirty.ratio | 0.5 | log.cleaner.min.cleanable.ratio | This configuration controls how frequently the log compactor will attempt to clean the log (assuming log compaction is enabled). By default we will avoid cleaning a log where more than 50% of the log has been compacted. This ratio bounds the maximum space wasted in the log by duplicates (at 50% at most 50% of the log could be duplicates). A higher ratio will mean fewer, more efficient cleanings but will mean more wasted space in the log.  
retention.bytes | None | log.retention.bytes | This configuration controls the maximum size a log can grow to before we will discard old log segments to free up space if we are using the "delete" retention policy. By default there is no size limit only a time limit.  
retention.ms | 7 days | log.retention.minutes | This configuration controls the maximum time we will retain a log before we will discard old log segments to free up space if we are using the "delete" retention policy. This represents an SLA on how soon consumers must read their data.  
segment.bytes | 1 GB | log.segment.bytes | This configuration controls the segment file size for the log. Retention and cleaning is always done a file at a time so a larger segment size means fewer files but less granular control over retention.  
segment.index.bytes | 10 MB | log.index.size.max.bytes | This configuration controls the size of the index that maps offsets to file positions. We preallocate this index file and shrink it only after log rolls. You generally should not need to change this setting.  
segment.ms | 7 days | log.roll.hours | This configuration controls the period of time after which Kafka will force the log to roll even if the segment file isn't full to ensure that retention can delete or compact old data.  
  
# Consumer Configs

The essential consumer configurations are the following: 

  * `group.id`
  * `zookeeper.connect` 
Property | Default | Description  
---|---|---  
group.id |  | A string that uniquely identifies the group of consumer processes to which this consumer belongs. By setting the same group id multiple processes indicate that they are all part of the same consumer group.  
zookeeper.connect |  | Specifies the ZooKeeper connection string in the form `hostname:port` where host and port are the host and port of a ZooKeeper server. To allow connecting through other ZooKeeper nodes when that ZooKeeper machine is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`.  The server may also have a ZooKeeper chroot path as part of it's ZooKeeper connection string which puts its data under some path in the global ZooKeeper namespace. If so the consumer should use the same chroot path in its connection string. For example to give a chroot path of `/chroot/path` you would give the connection string as `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path`.  
consumer.id | null |  Generated automatically if not set.  
socket.timeout.ms | 30 * 1000 | The socket timeout for network requests. The actual timeout set will be max.fetch.wait + socket.timeout.ms.  
socket.receive.buffer.bytes | 64 * 1024 | The socket receive buffer for network requests  
fetch.message.max.bytes | 1024 * 1024 | The number of byes of messages to attempt to fetch for each topic-partition in each fetch request. These bytes will be read into memory for each partition, so this helps control the memory used by the consumer. The fetch request size must be at least as large as the maximum message size the server allows or else it is possible for the producer to send messages larger than the consumer can fetch.  
auto.commit.enable | true | If true, periodically commit to ZooKeeper the offset of messages already fetched by the consumer. This committed offset will be used when the process fails as the position from which the new consumer will begin.  
auto.commit.interval.ms | 60 * 1000 | The frequency in ms that the consumer offsets are committed to zookeeper.  
queued.max.message.chunks | 10 | Max number of message chunks buffered for consumption. Each chunk can be up to fetch.message.max.bytes.  
rebalance.max.retries | 4 | When a new consumer joins a consumer group the set of consumers attempt to "rebalance" the load to assign partitions to each consumer. If the set of consumers changes while this assignment is taking place the rebalance will fail and retry. This setting controls the maximum number of attempts before giving up.  
fetch.min.bytes | 1 | The minimum amount of data the server should return for a fetch request. If insufficient data is available the request will wait for that much data to accumulate before answering the request.  
fetch.wait.max.ms | 100 | The maximum amount of time the server will block before answering the fetch request if there isn't sufficient data to immediately satisfy fetch.min.bytes  
rebalance.backoff.ms | 2000 | Backoff time between retries during rebalance.  
refresh.leader.backoff.ms | 200 | Backoff time to wait before trying to determine the leader of a partition that has just lost its leader.  
auto.offset.reset | largest |  What to do when there is no initial offset in ZooKeeper or if an offset is out of range:  
* smallest : automatically reset the offset to the smallest offset  
* largest : automatically reset the offset to the largest offset  
* anything else: throw exception to the consumer  
consumer.timeout.ms | -1 | Throw a timeout exception to the consumer if no message is available for consumption after the specified interval  
client.id | group id value | The client id is a user-specified string sent in each request to help trace calls. It should logically identify the application making the request.  
zookeeper.session.timeout.ms  | 6000 | ZooKeeper session timeout. If the consumer fails to heartbeat to ZooKeeper for this period of time it is considered dead and a rebalance will occur.  
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

# New Producer Configs

We are working on a replacement for our existing producer. The code is available in trunk now and can be considered beta quality. Below is the configuration for the new producer.  Name | Type | Default | Importance | Description  
---|---|---|---|---  
bootstrap.servers| list| | high| A list of host/port pairs to use for establishing the initial connection to the Kafka cluster. Data will be load balanced over all servers irrespective of which servers are specified here for bootstrapping--this list only impacts the initial hosts used to discover the full set of servers. This list should be in the form `host1:port1,host2:port2,...`. Since these servers are just used for the initial connection to discover the full cluster membership (which may change dynamically), this list need not contain the full set of servers (you may want more than one, though, in case a server is down). If no server in this list is available sending data will fail until on becomes available.  
acks| string| 1| high| The number of acknowledgments the producer requires the leader to have received before considering a request complete. This controls the durability of records that are sent. The following settings are common: 

  * `acks=0` If set to zero then the producer will not wait for any acknowledgment from the server at all. The record will be immediately added to the socket buffer and considered sent. No guarantee can be made that the server has received the record in this case, and the `retries` configuration will not take effect (as the client won't generally know of any failures). The offset given back for each record will always be set to -1. 
  * `acks=1` This will mean the leader will write the record to its local log but will respond without awaiting full acknowledgement from all followers. In this case should the leader fail immediately after acknowledging the record but before the followers have replicated it then the record will be lost. 
  * `acks=all` This means the leader will wait for the full set of in-sync replicas to acknowledge the record. This guarantees that the record will not be lost as long as at least one in-sync replica remains alive. This is the strongest available guarantee. 
  * Other settings such as `acks=2` are also possible, and will require the given number of acknowledgements but this is generally less useful.  
buffer.memory| long| 33554432| high| The total bytes of memory the producer can use to buffer records waiting to be sent to the server. If records are sent faster than they can be delivered to the server the producer will either block or throw an exception based on the preference specified by `block.on.buffer.full`. This setting should correspond roughly to the total memory the producer will use, but is not a hard bound since not all memory the producer uses is used for buffering. Some additional memory will be used for compression (if compression is enabled) as well as for maintaining in-flight requests.  
compression.type| string| none| high| The compression type for all data generated by the producer. The default is none (i.e. no compression). Valid values are `none`, `gzip`, or `snappy`. Compression is of full batches of data, so the efficacy of batching will also impact the compression ratio (more batching means better compression).  
retries| int| 0| high| Setting a value greater than zero will cause the client to resend any record whose send fails with a potentially transient error. Note that this retry is no different than if the client resent the record upon receiving the error. Allowing retries will potentially change the ordering of records because if two records are sent to a single partition, and the first fails and is retried but the second succeeds, then the second record may appear first.  
batch.size| int| 16384| medium| The producer will attempt to batch records together into fewer requests whenever multiple records are being sent to the same partition. This helps performance on both the client and the server. This configuration controls the default batch size in bytes. No attempt will be made to batch records larger than this size. Requests sent to brokers will contain multiple batches, one for each partition with data available to be sent. A small batch size will make batching less common and may reduce throughput (a batch size of zero will disable batching entirely). A very large batch size may use memory a bit more wastefully as we will always allocate a buffer of the specified batch size in anticipation of additional records.  
client.id| string| | medium| The id string to pass to the server when making requests. The purpose of this is to be able to track the source of requests beyond just ip/port by allowing a logical application name to be included with the request. The application can set any string it wants as this has no functional purpose other than in logging and metrics.  
linger.ms| long| 0| medium| The producer groups together any records that arrive in between request transmissions into a single batched request. Normally this occurs only under load when records arrive faster than they can be sent out. However in some circumstances the client may want to reduce the number of requests even under moderate load. This setting accomplishes this by adding a small amount of artificial delay--that is, rather than immediately sending out a record the producer will wait for up to the given delay to allow other records to be sent so that the sends can be batched together. This can be thought of as analogous to Nagle's algorithm in TCP. This setting gives the upper bound on the delay for batching: once we get `batch.size` worth of records for a partition it will be sent immediately regardless of this setting, however if we have fewer than this many bytes accumulated for this partition we will 'linger' for the specified time waiting for more records to show up. This setting defaults to 0 (i.e. no delay). Setting `linger.ms=5`, for example, would have the effect of reducing the number of requests sent but would add up to 5ms of latency to records sent in the absense of load.  
max.request.size| int| 1048576| medium| The maximum size of a request. This is also effectively a cap on the maximum record size. Note that the server has its own cap on record size which may be different from this. This setting will limit the number of record batches the producer will send in a single request to avoid sending huge requests.  
receive.buffer.bytes| int| 32768| medium| The size of the TCP receive buffer to use when reading data  
send.buffer.bytes| int| 131072| medium| The size of the TCP send buffer to use when sending data  
timeout.ms| int| 30000| medium| The configuration controls the maximum amount of time the server will wait for acknowledgments from followers to meet the acknowledgment requirements the producer has specified with the `acks` configuration. If the requested number of acknowledgments are not met when the timeout elapses an error will be returned. This timeout is measured on the server side and does not include the network latency of the request.  
block.on.buffer.full| boolean| true| low| When our memory buffer is exhausted we must either stop accepting new records (block) or throw errors. By default this setting is true and we block, however in some scenarios blocking is not desirable and it is better to immediately give an error. Setting this to `false` will accomplish that: the producer will throw a BufferExhaustedException if a recrord is sent and the buffer space is full.  
metadata.fetch.timeout.ms| long| 60000| low| The first time data is sent to a topic we must fetch metadata about that topic to know which servers host the topic's partitions. This configuration controls the maximum amount of time we will block waiting for the metadata fetch to succeed before throwing an exception back to the client.  
metadata.max.age.ms| long| 300000| low| The period of time in milliseconds after which we force a refresh of metadata even if we haven't seen any partition leadership changes to proactively discover any new brokers or partitions.  
metric.reporters| list| []| low| A list of classes to use as metrics reporters. Implementing the `MetricReporter` interface allows plugging in classes that will be notified of new metric creation. The JmxReporter is always included to register JMX statistics.  
metrics.num.samples| int| 2| low| The number of samples maintained to compute metrics.  
metrics.sample.window.ms| long| 30000| low| The metrics system maintains a configurable number of samples over a fixed window size. This configuration controls the size of the window. For example we might maintain two samples each measured over a 30 second period. When a window expires we erase and overwrite the oldest window.  
reconnect.backoff.ms| long| 10| low| The amount of time to wait before attempting to reconnect to a given host when a connection fails. This avoids a scenario where the client repeatedly attempts to connect to a host in a tight loop.  
retry.backoff.ms| long| 100| low| The amount of time to wait before attempting to retry a failed produce request to a given topic partition. This avoids repeated sending-and-failing in a tight loop.
