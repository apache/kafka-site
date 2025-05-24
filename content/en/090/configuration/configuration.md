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
Topic-level configurations and defaults are discussed in more detail below. {{< include-html file="/static/0110/generated/kafka_config.html" >}} 

More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.

Topic-level configuration Configurations pertinent to topics have both a global default as well an optional per-topic override. If no per-topic configuration is given the global default is used. The override can be set at topic creation time by giving one or more `--config` options. This example creates a topic named _my-topic_ with a custom max message size and flush rate: 
    
    
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
min.insync.replicas | 1 | min.insync.replicas | When a producer sets request.required.acks to -1, min.insync.replicas specifies the minimum number of replicas that must acknowledge a write for the write to be considered successful. If this minimum cannot be met, then the producer will raise an exception (either NotEnoughReplicas or NotEnoughReplicasAfterAppend). When used together, min.insync.replicas and request.required.acks allow you to enforce greater durability guarantees. A typical scenario would be to create a topic with a replication factor of 3, set min.insync.replicas to 2, and produce with request.required.acks of -1. This will ensure that the producer raises an exception if a majority of replicas do not receive a write.  
retention.bytes | None | log.retention.bytes | This configuration controls the maximum size a log can grow to before we will discard old log segments to free up space if we are using the "delete" retention policy. By default there is no size limit only a time limit.  
retention.ms | 7 days | log.retention.minutes | This configuration controls the maximum time we will retain a log before we will discard old log segments to free up space if we are using the "delete" retention policy. This represents an SLA on how soon consumers must read their data.  
segment.bytes | 1 GB | log.segment.bytes | This configuration controls the segment file size for the log. Retention and cleaning is always done a file at a time so a larger segment size means fewer files but less granular control over retention.  
segment.index.bytes | 10 MB | log.index.size.max.bytes | This configuration controls the size of the index that maps offsets to file positions. We preallocate this index file and shrink it only after log rolls. You generally should not need to change this setting.  
segment.ms | 7 days | log.roll.hours | This configuration controls the period of time after which Kafka will force the log to roll even if the segment file isn't full to ensure that retention can delete or compact old data.  
segment.jitter.ms | 0 | log.roll.jitter.{ms,hours} | The maximum jitter to subtract from logRollTimeMillis.  
  
# Producer Configs

Below is the configuration of the Java producer: {{< include-html file="/static/0110/generated/producer_config.html" >}} 

For those interested in the legacy Scala producer configs, information can be found [ here](http://kafka.apache.org/082/documentation.html#producerconfigs). 

# Consumer Configs

We introduce both the old 0.8 consumer configs and the new consumer configs respectively below. 

## Old Consumer Configs

The essential old consumer configurations are the following: 

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
num.consumer.fetchers | 1 | The number fetcher threads used to fetch data.  
auto.commit.enable | true | If true, periodically commit to ZooKeeper the offset of messages already fetched by the consumer. This committed offset will be used when the process fails as the position from which the new consumer will begin.  
auto.commit.interval.ms | 60 * 1000 | The frequency in ms that the consumer offsets are committed to zookeeper.  
queued.max.message.chunks | 2 | Max number of message chunks buffered for consumption. Each chunk can be up to fetch.message.max.bytes.  
rebalance.max.retries | 4 | When a new consumer joins a consumer group the set of consumers attempt to "rebalance" the load to assign partitions to each consumer. If the set of consumers changes while this assignment is taking place the rebalance will fail and retry. This setting controls the maximum number of attempts before giving up.  
fetch.min.bytes | 1 | The minimum amount of data the server should return for a fetch request. If insufficient data is available the request will wait for that much data to accumulate before answering the request.  
fetch.wait.max.ms | 100 | The maximum amount of time the server will block before answering the fetch request if there isn't sufficient data to immediately satisfy fetch.min.bytes  
rebalance.backoff.ms | 2000 | Backoff time between retries during rebalance. If not set explicitly, the value in zookeeper.sync.time.ms is used.   
refresh.leader.backoff.ms | 200 | Backoff time to wait before trying to determine the leader of a partition that has just lost its leader.  
auto.offset.reset | largest |  What to do when there is no initial offset in ZooKeeper or if an offset is out of range:  
* smallest : automatically reset the offset to the smallest offset  
* largest : automatically reset the offset to the largest offset  
* anything else: throw exception to the consumer  
consumer.timeout.ms | -1 | Throw a timeout exception to the consumer if no message is available for consumption after the specified interval  
exclude.internal.topics | true | Whether messages from internal topics (such as offsets) should be exposed to the consumer.  
client.id | group id value | The client id is a user-specified string sent in each request to help trace calls. It should logically identify the application making the request.  
zookeeper.session.timeout.ms  | 6000 | ZooKeeper session timeout. If the consumer fails to heartbeat to ZooKeeper for this period of time it is considered dead and a rebalance will occur.  
zookeeper.connection.timeout.ms | 6000 | The max time that the client waits while establishing a connection to zookeeper.  
zookeeper.sync.time.ms  | 2000 | How far a ZK follower can be behind a ZK leader  
offsets.storage | zookeeper | Select where offsets should be stored (zookeeper or kafka).  
offsets.channel.backoff.ms | 1000 | The backoff period when reconnecting the offsets channel or retrying failed offset fetch/commit requests.  
offsets.channel.socket.timeout.ms | 10000 | Socket timeout when reading responses for offset fetch/commit requests. This timeout is also used for ConsumerMetadata requests that are used to query for the offset manager.  
offsets.commit.max.retries | 5 | Retry the offset commit up to this many times on failure. This retry count only applies to offset commits during shut-down. It does not apply to commits originating from the auto-commit thread. It also does not apply to attempts to query for the offset coordinator before committing offsets. i.e., if a consumer metadata request fails for any reason, it will be retried and that retry does not count toward this limit.  
dual.commit.enabled | true | If you are using "kafka" as offsets.storage, you can dual commit offsets to ZooKeeper (in addition to Kafka). This is required during migration from zookeeper-based offset storage to kafka-based offset storage. With respect to any given consumer group, it is safe to turn this off after all instances within that group have been migrated to the new version that commits offsets to the broker (instead of directly to ZooKeeper).  
partition.assignment.strategy | range | Select between the "range" or "roundrobin" strategy for assigning partitions to consumer streams.The round-robin partition assignor lays out all the available partitions and all the available consumer threads. It then proceeds to do a round-robin assignment from partition to consumer thread. If the subscriptions of all consumer instances are identical, then the partitions will be uniformly distributed. (i.e., the partition ownership counts will be within a delta of exactly one across all consumer threads.) Round-robin assignment is permitted only if: (a) Every topic has the same number of streams within a consumer instance (b) The set of subscribed topics is identical for every consumer instance within the group. Range partitioning works on a per-topic basis. For each topic, we lay out the available partitions in numeric order and the consumer threads in lexicographic order. We then divide the number of partitions by the total number of consumer streams (threads) to determine the number of partitions to assign to each consumer. If it does not evenly divide, then the first few consumers will have one extra partition.  
  
More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.

## New Consumer Configs

Since 0.9.0.0 we have been working on a replacement for our existing simple and high-level consumers. The code is considered beta quality. Below is the configuration for the new consumer: {{< include-html file="/static/0110/generated/consumer_config.html" >}} 

# Kafka Connect Configs

{{< include-html file="/static/0110/generated/connect_config.html" >}} 
