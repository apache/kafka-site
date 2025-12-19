---
title: Broker Configs
description: Broker Configs
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

The essential configurations are the following: 

  * `broker.id`
  * `log.dirs`
  * `zookeeper.connect` 
Topic-level configurations and defaults are discussed in more detail below.   
<table>  
<tr>  
<th>

Property
</th>  
<th>

Default
</th>  
<th>

Description
</th> </tr>  
<tr>  
<td>

broker.id
</td>  
<td>


</td>  
<td>

Each broker is uniquely identified by a non-negative integer id. This id serves as the broker's "name" and allows the broker to be moved to a different host/port without confusing consumers. You can choose any number you like so long as it is unique. 
</td> </tr>  
<tr>  
<td>

log.dirs
</td>  
<td>

/tmp/kafka-logs
</td>  
<td>

A comma-separated list of one or more directories in which Kafka data is stored. Each new partition that is created will be placed in the directory which currently has the fewest partitions.
</td> </tr>  
<tr>  
<td>

port
</td>  
<td>

9092
</td>  
<td>

The port on which the server accepts client connections.
</td> </tr>  
<tr>  
<td>

zookeeper.connect
</td>  
<td>

null
</td>  
<td>

Specifies the ZooKeeper connection string in the form `hostname:port`, where hostname and port are the host and port for a node in your ZooKeeper cluster. To allow connecting through other ZooKeeper nodes when that host is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`. 

ZooKeeper also allows you to add a "chroot" path which will make all kafka data for this cluster appear under a particular path. This is a way to setup multiple Kafka clusters or other applications on the same ZooKeeper cluster. To do this give a connection string in the form `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path` which would put all this cluster's data under the path `/chroot/path`. Note that consumers must use the same connection string.
</td> </tr>  
<tr>  
<td>

message.max.bytes
</td>  
<td>

1000000
</td>  
<td>

The maximum size of a message that the server can receive. It is important that this property be in sync with the maximum fetch size your consumers use or else an unruly producer will be able to publish messages too large for consumers to consume.
</td> </tr>  
<tr>  
<td>

num.network.threads
</td>  
<td>

3
</td>  
<td>

The number of network threads that the server uses for handling network requests. You probably don't need to change this.
</td> </tr>  
<tr>  
<td>

num.io.threads
</td>  
<td>

8
</td>  
<td>

The number of I/O threads that the server uses for executing requests. You should have at least as many threads as you have disks.
</td> </tr>  
<tr>  
<td>

background.threads
</td>  
<td>

10
</td>  
<td>

The number of threads to use for various background processing tasks such as file deletion. You should not need to change this.
</td> </tr>  
<tr>  
<td>

queued.max.requests
</td>  
<td>

500
</td>  
<td>

The number of requests that can be queued up for processing by the I/O threads before the network threads stop reading in new requests.
</td> </tr>  
<tr>  
<td>

host.name
</td>  
<td>

null
</td>  
<td>



Hostname of broker. If this is set, it will only bind to this address. If this is not set, it will bind to all interfaces, and publish one to ZK.


</td> </tr>  
<tr>  
<td>

advertised.host.name
</td>  
<td>

null
</td>  
<td>



If this is set this is the hostname that will be given out to producers, consumers, and other brokers to connect to.


</td> </tr>  
<tr>  
<td>

advertised.port
</td>  
<td>

null
</td>  
<td>



The port to give out to producers, consumers, and other brokers to use in establishing connections. This only needs to be set if this port is different from the port the server should bind to.


</td> </tr>  
<tr>  
<td>

socket.send.buffer.bytes
</td>  
<td>

100 * 1024
</td>  
<td>

The SO_SNDBUFF buffer the server prefers for socket connections.
</td> </tr>  
<tr>  
<td>

socket.receive.buffer.bytes
</td>  
<td>

100 * 1024
</td>  
<td>

The SO_RCVBUFF buffer the server prefers for socket connections.
</td> </tr>  
<tr>  
<td>

socket.request.max.bytes
</td>  
<td>

100 * 1024 * 1024
</td>  
<td>

The maximum request size the server will allow. This prevents the server from running out of memory and should be smaller than the Java heap size.
</td> </tr>  
<tr>  
<td>

num.partitions
</td>  
<td>

1
</td>  
<td>

The default number of partitions per topic if a partition count isn't given at topic creation time.
</td> </tr>  
<tr>  
<td>

log.segment.bytes
</td>  
<td>

1024 * 1024 * 1024
</td>  
<td>

The log for a topic partition is stored as a directory of segment files. This setting controls the size to which a segment file will grow before a new segment is rolled over in the log. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.roll.{ms,hours}
</td>  
<td>

24 * 7 hours
</td>  
<td>

This setting will force Kafka to roll a new log segment even if the log.segment.bytes size has not been reached. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.cleanup.policy
</td>  
<td>

delete
</td>  
<td>

This can take either the value _delete_ or _compact_. If _delete_ is set, log segments will be deleted when they reach the size or time limits set. If _compact_ is set log compaction will be used to clean out obsolete records. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.retention.{ms,minutes,hours}
</td>  
<td>

7 days
</td>  
<td>

The amount of time to keep a log segment before it is deleted, i.e. the default data retention window for all topics. Note that if both log.retention.minutes and log.retention.bytes are both set we delete a segment when either limit is exceeded. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.retention.bytes
</td>  
<td>

-1
</td>  
<td>

The amount of data to retain in the log for each topic-partitions. Note that this is the limit per-partition so multiply by the number of partitions to get the total data retained for the topic. Also note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.retention.check.interval.ms
</td>  
<td>

5 minutes
</td>  
<td>

The period with which we check whether any log segment is eligible for deletion to meet the retention policies.
</td> </tr>  
<tr>  
<td>

log.cleaner.enable
</td>  
<td>

false
</td>  
<td>

This configuration must be set to true for log compaction to run.
</td> </tr>  
<tr>  
<td>

log.cleaner.threads
</td>  
<td>

1
</td>  
<td>

The number of threads to use for cleaning logs in log compaction.
</td> </tr>  
<tr>  
<td>

log.cleaner.io.max.bytes.per.second
</td>  
<td>

Double.MaxValue
</td>  
<td>

The maximum amount of I/O the log cleaner can do while performing log compaction. This setting allows setting a limit for the cleaner to avoid impacting live request serving.
</td> </tr>  
<tr>  
<td>

log.cleaner.dedupe.buffer.size
</td>  
<td>

500*1024*1024
</td>  
<td>

The size of the buffer the log cleaner uses for indexing and deduplicating logs during cleaning. Larger is better provided you have sufficient memory.
</td> </tr>  
<tr>  
<td>

log.cleaner.io.buffer.size
</td>  
<td>

512*1024
</td>  
<td>

The size of the I/O chunk used during log cleaning. You probably don't need to change this.
</td> </tr>  
<tr>  
<td>

log.cleaner.io.buffer.load.factor
</td>  
<td>

0.9
</td>  
<td>

The load factor of the hash table used in log cleaning. You probably don't need to change this.
</td> </tr>  
<tr>  
<td>

log.cleaner.backoff.ms
</td>  
<td>

15000
</td>  
<td>

The interval between checks to see if any logs need cleaning.
</td> </tr>  
<tr>  
<td>

log.cleaner.min.cleanable.ratio
</td>  
<td>

0.5
</td>  
<td>

This configuration controls how frequently the log compactor will attempt to clean the log (assuming log compaction is enabled). By default we will avoid cleaning a log where more than 50% of the log has been compacted. This ratio bounds the maximum space wasted in the log by duplicates (at 50% at most 50% of the log could be duplicates). A higher ratio will mean fewer, more efficient cleanings but will mean more wasted space in the log. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.cleaner.delete.retention.ms
</td>  
<td>

1 day
</td>  
<td>

The amount of time to retain delete tombstone markers for log compacted topics. This setting also gives a bound on the time in which a consumer must complete a read if they begin from offset 0 to ensure that they get a valid snapshot of the final stage (otherwise delete tombstones may be collected before they complete their scan). This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.index.size.max.bytes
</td>  
<td>

10 * 1024 * 1024
</td>  
<td>

The maximum size in bytes we allow for the offset index for each log segment. Note that we will always pre-allocate a sparse file with this much space and shrink it down when the log rolls. If the index fills up we will roll a new log segment even if we haven't reached the log.segment.bytes limit. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

log.index.interval.bytes
</td>  
<td>

4096
</td>  
<td>

The byte interval at which we add an entry to the offset index. When executing a fetch request the server must do a linear scan for up to this many bytes to find the correct position in the log to begin and end the fetch. So setting this value to be larger will mean larger index files (and a bit more memory usage) but less scanning. However the server will never add more than one index entry per log append (even if more than log.index.interval worth of messages are appended). In general you probably don't need to mess with this value.
</td> </tr>  
<tr>  
<td>

log.flush.interval.messages
</td>  
<td>

Long.MaxValue
</td>  
<td>

The number of messages written to a log partition before we force an fsync on the log. Setting this lower will sync data to disk more often but will have a major impact on performance. We generally recommend that people make use of replication for durability rather than depending on single-server fsync, however this setting can be used to be extra certain.
</td> </tr>  
<tr>  
<td>

log.flush.scheduler.interval.ms
</td>  
<td>

Long.MaxValue
</td>  
<td>

The frequency in ms that the log flusher checks whether any log is eligible to be flushed to disk.
</td> </tr>  
<tr>  
<td>

log.flush.interval.ms
</td>  
<td>

Long.MaxValue
</td>  
<td>

The maximum time between fsync calls on the log. If used in conjuction with log.flush.interval.messages the log will be flushed when either criteria is met.
</td> </tr>  
<tr>  
<td>

log.delete.delay.ms
</td>  
<td>

60000
</td>  
<td>

The period of time we hold log files around after they are removed from the in-memory segment index. This period of time allows any in-progress reads to complete uninterrupted without locking. You generally don't need to change this.
</td> </tr>  
<tr>  
<td>

log.flush.offset.checkpoint.interval.ms
</td>  
<td>

60000
</td>  
<td>

The frequency with which we checkpoint the last flush point for logs for recovery. You should not need to change this.
</td> </tr>  
<tr>  
<td>

log.segment.delete.delay.ms
</td>  
<td>

60000
</td>  
<td>

the amount of time to wait before deleting a file from the filesystem.
</td> </tr>  
<tr>  
<td>

auto.create.topics.enable
</td>  
<td>

true
</td>  
<td>

Enable auto creation of topic on the server. If this is set to true then attempts to produce data or fetch metadata for a non-existent topic will automatically create it with the default replication factor and number of partitions.
</td> </tr>  
<tr>  
<td>

controller.socket.timeout.ms
</td>  
<td>

30000
</td>  
<td>

The socket timeout for commands from the partition management controller to the replicas.
</td> </tr>  
<tr>  
<td>

controller.message.queue.size
</td>  
<td>

Int.MaxValue
</td>  
<td>

The buffer size for controller-to-broker-channels
</td> </tr>  
<tr>  
<td>

default.replication.factor
</td>  
<td>

1
</td>  
<td>

The default replication factor for automatically created topics.
</td> </tr>  
<tr>  
<td>

replica.lag.time.max.ms
</td>  
<td>

10000
</td>  
<td>

If a follower hasn't sent any fetch requests for this window of time, the leader will remove the follower from ISR (in-sync replicas) and treat it as dead.
</td> </tr>  
<tr>  
<td>

replica.lag.max.messages
</td>  
<td>

4000
</td>  
<td>

If a replica falls more than this many messages behind the leader, the leader will remove the follower from ISR and treat it as dead.
</td> </tr>  
<tr>  
<td>

replica.socket.timeout.ms
</td>  
<td>

30 * 1000
</td>  
<td>

The socket timeout for network requests to the leader for replicating data.
</td> </tr>  
<tr>  
<td>

replica.socket.receive.buffer.bytes
</td>  
<td>

64 * 1024
</td>  
<td>

The socket receive buffer for network requests to the leader for replicating data.
</td> </tr>  
<tr>  
<td>

replica.fetch.max.bytes
</td>  
<td>

1024 * 1024
</td>  
<td>

The number of byes of messages to attempt to fetch for each partition in the fetch requests the replicas send to the leader.
</td> </tr>  
<tr>  
<td>

replica.fetch.wait.max.ms
</td>  
<td>

500
</td>  
<td>

The maximum amount of time to wait time for data to arrive on the leader in the fetch requests sent by the replicas to the leader.
</td> </tr>  
<tr>  
<td>

replica.fetch.min.bytes
</td>  
<td>

1
</td>  
<td>

Minimum bytes expected for each fetch response for the fetch requests from the replica to the leader. If not enough bytes, wait up to replica.fetch.wait.max.ms for this many bytes to arrive.
</td> </tr>  
<tr>  
<td>

num.replica.fetchers
</td>  
<td>

1
</td>  
<td>



Number of threads used to replicate messages from leaders. Increasing this value can increase the degree of I/O parallelism in the follower broker.


</td> </tr>  
<tr>  
<td>

replica.high.watermark.checkpoint.interval.ms
</td>  
<td>

5000
</td>  
<td>

The frequency with which each replica saves its high watermark to disk to handle recovery.
</td> </tr>  
<tr>  
<td>

fetch.purgatory.purge.interval.requests
</td>  
<td>

1000
</td>  
<td>

The purge interval (in number of requests) of the fetch request purgatory.
</td> </tr>  
<tr>  
<td>

producer.purgatory.purge.interval.requests
</td>  
<td>

1000
</td>  
<td>

The purge interval (in number of requests) of the producer request purgatory.
</td> </tr>  
<tr>  
<td>

zookeeper.session.timeout.ms
</td>  
<td>

6000
</td>  
<td>

ZooKeeper session timeout. If the server fails to heartbeat to ZooKeeper within this period of time it is considered dead. If you set this too low the server may be falsely considered dead; if you set it too high it may take too long to recognize a truly dead server.
</td> </tr>  
<tr>  
<td>

zookeeper.connection.timeout.ms
</td>  
<td>

6000
</td>  
<td>

The maximum amount of time that the client waits to establish a connection to zookeeper.
</td> </tr>  
<tr>  
<td>

zookeeper.sync.time.ms
</td>  
<td>

2000
</td>  
<td>

How far a ZK follower can be behind a ZK leader.
</td> </tr>  
<tr>  
<td>

controlled.shutdown.enable
</td>  
<td>

true
</td>  
<td>

Enable controlled shutdown of the broker. If enabled, the broker will move all leaders on it to some other brokers before shutting itself down. This reduces the unavailability window during shutdown.
</td> </tr>  
<tr>  
<td>

controlled.shutdown.max.retries
</td>  
<td>

3
</td>  
<td>

Number of retries to complete the controlled shutdown successfully before executing an unclean shutdown.
</td> </tr>  
<tr>  
<td>

controlled.shutdown.retry.backoff.ms
</td>  
<td>

5000
</td>  
<td>

Backoff time between shutdown retries.
</td> </tr>  
<tr>  
<td>

auto.leader.rebalance.enable
</td>  
<td>

true
</td>  
<td>

If this is enabled the controller will automatically try to balance leadership for partitions among the brokers by periodically returning leadership to the "preferred" replica for each partition if it is available.
</td> </tr>  
<tr>  
<td>

leader.imbalance.per.broker.percentage
</td>  
<td>

10
</td>  
<td>

The percentage of leader imbalance allowed per broker. The controller will rebalance leadership if this ratio goes above the configured value per broker.
</td> </tr>  
<tr>  
<td>

leader.imbalance.check.interval.seconds
</td>  
<td>

300
</td>  
<td>

The frequency with which to check for leader imbalance.
</td> </tr>  
<tr>  
<td>

offset.metadata.max.bytes
</td>  
<td>

4096
</td>  
<td>

The maximum amount of metadata to allow clients to save with their offsets.
</td> </tr>  
<tr>  
<td>

max.connections.per.ip
</td>  
<td>

Int.MaxValue
</td>  
<td>

The maximum number of connections that a broker allows from each ip address.
</td> </tr>  
<tr>  
<td>

max.connections.per.ip.overrides
</td>  
<td>


</td>  
<td>

Per-ip or hostname overrides to the default maximum number of connections.
</td> </tr>  
<tr>  
<td>

connections.max.idle.ms
</td>  
<td>

600000
</td>  
<td>

Idle connections timeout: the server socket processor threads close the connections that idle more than this.
</td> </tr>  
<tr>  
<td>

log.roll.jitter.{ms,hours}
</td>  
<td>

0
</td>  
<td>

The maximum jitter to subtract from logRollTimeMillis.
</td> </tr>  
<tr>  
<td>

num.recovery.threads.per.data.dir
</td>  
<td>

1
</td>  
<td>

The number of threads per data directory to be used for log recovery at startup and flushing at shutdown.
</td> </tr>  
<tr>  
<td>

unclean.leader.election.enable
</td>  
<td>

true
</td>  
<td>

Indicates whether to enable replicas not in the ISR set to be elected as leader as a last resort, even though doing so may result in data loss.
</td> </tr>  
<tr>  
<td>

delete.topic.enable
</td>  
<td>

false
</td>  
<td>

Enable delete topic.
</td> </tr>  
<tr>  
<td>

offsets.topic.num.partitions
</td>  
<td>

50
</td>  
<td>

The number of partitions for the offset commit topic. Since changing this after deployment is currently unsupported, we recommend using a higher setting for production (e.g., 100-200).
</td> </tr>  
<tr>  
<td>

offsets.topic.retention.minutes
</td>  
<td>

1440
</td>  
<td>

Offsets that are older than this age will be marked for deletion. The actual purge will occur when the log cleaner compacts the offsets topic.
</td> </tr>  
<tr>  
<td>

offsets.retention.check.interval.ms
</td>  
<td>

600000
</td>  
<td>

The frequency at which the offset manager checks for stale offsets.
</td> </tr>  
<tr>  
<td>

offsets.topic.replication.factor
</td>  
<td>

3
</td>  
<td>

The replication factor for the offset commit topic. A higher setting (e.g., three or four) is recommended in order to ensure higher availability. If the offsets topic is created when fewer brokers than the replication factor then the offsets topic will be created with fewer replicas.
</td> </tr>  
<tr>  
<td>

offsets.topic.segment.bytes
</td>  
<td>

104857600
</td>  
<td>

Segment size for the offsets topic. Since it uses a compacted topic, this should be kept relatively low in order to facilitate faster log compaction and loads.
</td> </tr>  
<tr>  
<td>

offsets.load.buffer.size
</td>  
<td>

5242880
</td>  
<td>

An offset load occurs when a broker becomes the offset manager for a set of consumer groups (i.e., when it becomes a leader for an offsets topic partition). This setting corresponds to the batch size (in bytes) to use when reading from the offsets segments when loading offsets into the offset manager's cache.
</td> </tr>  
<tr>  
<td>

offsets.commit.required.acks
</td>  
<td>

-1
</td>  
<td>

The number of acknowledgements that are required before the offset commit can be accepted. This is similar to the producer's acknowledgement setting. In general, the default should not be overridden.
</td> </tr>  
<tr>  
<td>

offsets.commit.timeout.ms
</td>  
<td>

5000
</td>  
<td>

The offset commit will be delayed until this timeout or the required number of replicas have received the offset commit. This is similar to the producer request timeout.
</td> </tr> </table>

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
    

The following are the topic-level configurations. The server's default configuration for this property is given under the Server Default Property heading, setting this default in the server config allows you to change the default given to topics that have no override specified.   
<table>  
<tr>  
<th>

Property
</th>  
<th>

Default
</th>  
<th>

Server Default Property
</th>  
<th>

Description
</th> </tr>  
<tr>  
<td>

cleanup.policy
</td>  
<td>

delete
</td>  
<td>

log.cleanup.policy
</td>  
<td>

A string that is either "delete" or "compact". This string designates the retention policy to use on old log segments. The default policy ("delete") will discard old segments when their retention time or size limit has been reached. The "compact" setting will enable log compaction on the topic.
</td> </tr>  
<tr>  
<td>

delete.retention.ms
</td>  
<td>

86400000 (24 hours)
</td>  
<td>

log.cleaner.delete.retention.ms
</td>  
<td>

The amount of time to retain delete tombstone markers for log compacted topics. This setting also gives a bound on the time in which a consumer must complete a read if they begin from offset 0 to ensure that they get a valid snapshot of the final stage (otherwise delete tombstones may be collected before they complete their scan).
</td> </tr>  
<tr>  
<td>

flush.messages
</td>  
<td>

None
</td>  
<td>

log.flush.interval.messages
</td>  
<td>

This setting allows specifying an interval at which we will force an fsync of data written to the log. For example if this was set to 1 we would fsync after every message; if it were 5 we would fsync after every five messages. In general we recommend you not set this and use replication for durability and allow the operating system's background flush capabilities as it is more efficient. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

flush.ms
</td>  
<td>

None
</td>  
<td>

log.flush.interval.ms
</td>  
<td>

This setting allows specifying a time interval at which we will force an fsync of data written to the log. For example if this was set to 1000 we would fsync after 1000 ms had passed. In general we recommend you not set this and use replication for durability and allow the operating system's background flush capabilities as it is more efficient.
</td> </tr>  
<tr>  
<td>

index.interval.bytes
</td>  
<td>

4096
</td>  
<td>

log.index.interval.bytes
</td>  
<td>

This setting controls how frequently Kafka adds an index entry to it's offset index. The default setting ensures that we index a message roughly every 4096 bytes. More indexing allows reads to jump closer to the exact position in the log but makes the index larger. You probably don't need to change this.
</td> </tr>  
<tr>  
<td>

max.message.bytes
</td>  
<td>

1,000,000
</td>  
<td>

message.max.bytes
</td>  
<td>

This is largest message size Kafka will allow to be appended to this topic. Note that if you increase this size you must also increase your consumer's fetch size so they can fetch messages this large.
</td> </tr>  
<tr>  
<td>

min.cleanable.dirty.ratio
</td>  
<td>

0.5
</td>  
<td>

log.cleaner.min.cleanable.ratio
</td>  
<td>

This configuration controls how frequently the log compactor will attempt to clean the log (assuming log compaction is enabled). By default we will avoid cleaning a log where more than 50% of the log has been compacted. This ratio bounds the maximum space wasted in the log by duplicates (at 50% at most 50% of the log could be duplicates). A higher ratio will mean fewer, more efficient cleanings but will mean more wasted space in the log.
</td> </tr>  
<tr>  
<td>

min.insync.replicas
</td>  
<td>

1
</td>  
<td>

min.insync.replicas
</td>  
<td>

When a producer sets request.required.acks to -1, min.insync.replicas specifies the minimum number of replicas that must acknowledge a write for the write to be considered successful. If this minimum cannot be met, then the producer will raise an exception (either NotEnoughReplicas or NotEnoughReplicasAfterAppend).  When used together, min.insync.replicas and request.required.acks allow you to enforce greater durability guarantees. A typical scenario would be to create a topic with a replication factor of 3, set min.insync.replicas to 2, and produce with request.required.acks of -1. This will ensure that the producer raises an exception if a majority of replicas do not receive a write.
</td> </tr>  
<tr>  
<td>

retention.bytes
</td>  
<td>

None
</td>  
<td>

log.retention.bytes
</td>  
<td>

This configuration controls the maximum size a log can grow to before we will discard old log segments to free up space if we are using the "delete" retention policy. By default there is no size limit only a time limit.
</td> </tr>  
<tr>  
<td>

retention.ms
</td>  
<td>

7 days
</td>  
<td>

log.retention.minutes
</td>  
<td>

This configuration controls the maximum time we will retain a log before we will discard old log segments to free up space if we are using the "delete" retention policy. This represents an SLA on how soon consumers must read their data.
</td> </tr>  
<tr>  
<td>

segment.bytes
</td>  
<td>

1 GB
</td>  
<td>

log.segment.bytes
</td>  
<td>

This configuration controls the segment file size for the log. Retention and cleaning is always done a file at a time so a larger segment size means fewer files but less granular control over retention.
</td> </tr>  
<tr>  
<td>

segment.index.bytes
</td>  
<td>

10 MB
</td>  
<td>

log.index.size.max.bytes
</td>  
<td>

This configuration controls the size of the index that maps offsets to file positions. We preallocate this index file and shrink it only after log rolls. You generally should not need to change this setting.
</td> </tr>  
<tr>  
<td>

segment.ms
</td>  
<td>

7 days
</td>  
<td>

log.roll.hours
</td>  
<td>

This configuration controls the period of time after which Kafka will force the log to roll even if the segment file isn't full to ensure that retention can delete or compact old data.
</td> </tr>  
<tr>  
<td>

segment.jitter.ms
</td>  
<td>

0
</td>  
<td>

log.roll.jitter.{ms,hours}
</td>  
<td>

The maximum jitter to subtract from logRollTimeMillis.
</td> </tr> </table>
