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
Topic-level configurations and defaults are discussed in more detail below.  Property | Default | Description  
---|---|---  
broker.id |  | Each broker is uniquely identified by a non-negative integer id. This id serves as the broker's "name" and allows the broker to be moved to a different host/port without confusing consumers. You can choose any number you like so long as it is unique.   
log.dirs | /tmp/kafka-logs | A comma-separated list of one or more directories in which Kafka data is stored. Each new partition that is created will be placed in the directory which currently has the fewest partitions.  
port | 9092 | The port on which the server accepts client connections.  
zookeeper.connect | null | Specifies the ZooKeeper connection string in the form `hostname:port`, where hostname and port are the host and port for a node in your ZooKeeper cluster. To allow connecting through other ZooKeeper nodes when that host is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`.  ZooKeeper also allows you to add a "chroot" path which will make all kafka data for this cluster appear under a particular path. This is a way to setup multiple Kafka clusters or other applications on the same ZooKeeper cluster. To do this give a connection string in the form `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path` which would put all this cluster's data under the path `/chroot/path`. Note that consumers must use the same connection string.  
message.max.bytes | 1000000 | The maximum size of a message that the server can receive. It is important that this property be in sync with the maximum fetch size your consumers use or else an unruly producer will be able to publish messages too large for consumers to consume.  
num.network.threads | 3 | The number of network threads that the server uses for handling network requests. You probably don't need to change this.  
num.io.threads | 8 | The number of I/O threads that the server uses for executing requests. You should have at least as many threads as you have disks.  
background.threads | 10 | The number of threads to use for various background processing tasks such as file deletion. You should not need to change this.  
queued.max.requests | 500 | The number of requests that can be queued up for processing by the I/O threads before the network threads stop reading in new requests.  
host.name | null |  Hostname of broker. If this is set, it will only bind to this address. If this is not set, it will bind to all interfaces, and publish one to ZK.  
advertised.host.name | null |  If this is set this is the hostname that will be given out to producers, consumers, and other brokers to connect to.  
advertised.port | null |  The port to give out to producers, consumers, and other brokers to use in establishing connections. This only needs to be set if this port is different from the port the server should bind to.  
socket.send.buffer.bytes | 100 * 1024 | The SO_SNDBUFF buffer the server prefers for socket connections.  
socket.receive.buffer.bytes | 100 * 1024 | The SO_RCVBUFF buffer the server prefers for socket connections.  
socket.request.max.bytes | 100 * 1024 * 1024 | The maximum request size the server will allow. This prevents the server from running out of memory and should be smaller than the Java heap size.  
num.partitions | 1 | The default number of partitions per topic if a partition count isn't given at topic creation time.  
log.segment.bytes | 1024 * 1024 * 1024 | The log for a topic partition is stored as a directory of segment files. This setting controls the size to which a segment file will grow before a new segment is rolled over in the log. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.roll.{ms,hours} | 24 * 7 hours | This setting will force Kafka to roll a new log segment even if the log.segment.bytes size has not been reached. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.cleanup.policy | delete | This can take either the value _delete_ or _compact_. If _delete_ is set, log segments will be deleted when they reach the size or time limits set. If _compact_ is set log compaction will be used to clean out obsolete records. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.retention.{ms,minutes,hours} | 7 days | The amount of time to keep a log segment before it is deleted, i.e. the default data retention window for all topics. Note that if both log.retention.minutes and log.retention.bytes are both set we delete a segment when either limit is exceeded. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.retention.bytes | -1 | The amount of data to retain in the log for each topic-partitions. Note that this is the limit per-partition so multiply by the number of partitions to get the total data retained for the topic. Also note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.retention.check.interval.ms | 5 minutes | The period with which we check whether any log segment is eligible for deletion to meet the retention policies.  
log.cleaner.enable | false | This configuration must be set to true for log compaction to run.  
log.cleaner.threads | 1 | The number of threads to use for cleaning logs in log compaction.  
log.cleaner.io.max.bytes.per.second | Double.MaxValue | The maximum amount of I/O the log cleaner can do while performing log compaction. This setting allows setting a limit for the cleaner to avoid impacting live request serving.  
log.cleaner.dedupe.buffer.size | 500*1024*1024 | The size of the buffer the log cleaner uses for indexing and deduplicating logs during cleaning. Larger is better provided you have sufficient memory.  
log.cleaner.io.buffer.size | 512*1024 | The size of the I/O chunk used during log cleaning. You probably don't need to change this.  
log.cleaner.io.buffer.load.factor | 0.9 | The load factor of the hash table used in log cleaning. You probably don't need to change this.  
log.cleaner.backoff.ms | 15000 | The interval between checks to see if any logs need cleaning.  
log.cleaner.min.cleanable.ratio | 0.5 | This configuration controls how frequently the log compactor will attempt to clean the log (assuming log compaction is enabled). By default we will avoid cleaning a log where more than 50% of the log has been compacted. This ratio bounds the maximum space wasted in the log by duplicates (at 50% at most 50% of the log could be duplicates). A higher ratio will mean fewer, more efficient cleanings but will mean more wasted space in the log. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.cleaner.delete.retention.ms | 1 day | The amount of time to retain delete tombstone markers for log compacted topics. This setting also gives a bound on the time in which a consumer must complete a read if they begin from offset 0 to ensure that they get a valid snapshot of the final stage (otherwise delete tombstones may be collected before they complete their scan). This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.index.size.max.bytes | 10 * 1024 * 1024 | The maximum size in bytes we allow for the offset index for each log segment. Note that we will always pre-allocate a sparse file with this much space and shrink it down when the log rolls. If the index fills up we will roll a new log segment even if we haven't reached the log.segment.bytes limit. This setting can be overridden on a per-topic basis (see the per-topic configuration section).  
log.index.interval.bytes | 4096 | The byte interval at which we add an entry to the offset index. When executing a fetch request the server must do a linear scan for up to this many bytes to find the correct position in the log to begin and end the fetch. So setting this value to be larger will mean larger index files (and a bit more memory usage) but less scanning. However the server will never add more than one index entry per log append (even if more than log.index.interval worth of messages are appended). In general you probably don't need to mess with this value.  
log.flush.interval.messages | Long.MaxValue | The number of messages written to a log partition before we force an fsync on the log. Setting this lower will sync data to disk more often but will have a major impact on performance. We generally recommend that people make use of replication for durability rather than depending on single-server fsync, however this setting can be used to be extra certain.  
log.flush.scheduler.interval.ms | Long.MaxValue | The frequency in ms that the log flusher checks whether any log is eligible to be flushed to disk.  
log.flush.interval.ms | Long.MaxValue | The maximum time between fsync calls on the log. If used in conjuction with log.flush.interval.messages the log will be flushed when either criteria is met.  
log.delete.delay.ms | 60000 | The period of time we hold log files around after they are removed from the in-memory segment index. This period of time allows any in-progress reads to complete uninterrupted without locking. You generally don't need to change this.  
log.flush.offset.checkpoint.interval.ms | 60000 | The frequency with which we checkpoint the last flush point for logs for recovery. You should not need to change this.  
log.segment.delete.delay.ms | 60000 | the amount of time to wait before deleting a file from the filesystem.  
auto.create.topics.enable | true | Enable auto creation of topic on the server. If this is set to true then attempts to produce data or fetch metadata for a non-existent topic will automatically create it with the default replication factor and number of partitions.  
controller.socket.timeout.ms | 30000 | The socket timeout for commands from the partition management controller to the replicas.  
controller.message.queue.size | Int.MaxValue | The buffer size for controller-to-broker-channels  
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
fetch.purgatory.purge.interval.requests | 1000 | The purge interval (in number of requests) of the fetch request purgatory.  
producer.purgatory.purge.interval.requests | 1000 | The purge interval (in number of requests) of the producer request purgatory.  
zookeeper.session.timeout.ms | 6000 | ZooKeeper session timeout. If the server fails to heartbeat to ZooKeeper within this period of time it is considered dead. If you set this too low the server may be falsely considered dead; if you set it too high it may take too long to recognize a truly dead server.  
zookeeper.connection.timeout.ms | 6000 | The maximum amount of time that the client waits to establish a connection to zookeeper.  
zookeeper.sync.time.ms | 2000 | How far a ZK follower can be behind a ZK leader.  
controlled.shutdown.enable | true | Enable controlled shutdown of the broker. If enabled, the broker will move all leaders on it to some other brokers before shutting itself down. This reduces the unavailability window during shutdown.  
controlled.shutdown.max.retries | 3 | Number of retries to complete the controlled shutdown successfully before executing an unclean shutdown.  
controlled.shutdown.retry.backoff.ms | 5000 | Backoff time between shutdown retries.  
auto.leader.rebalance.enable | true | If this is enabled the controller will automatically try to balance leadership for partitions among the brokers by periodically returning leadership to the "preferred" replica for each partition if it is available.  
leader.imbalance.per.broker.percentage | 10 | The percentage of leader imbalance allowed per broker. The controller will rebalance leadership if this ratio goes above the configured value per broker.  
leader.imbalance.check.interval.seconds | 300 | The frequency with which to check for leader imbalance.  
offset.metadata.max.bytes | 4096 | The maximum amount of metadata to allow clients to save with their offsets.  
max.connections.per.ip | Int.MaxValue | The maximum number of connections that a broker allows from each ip address.  
max.connections.per.ip.overrides |  | Per-ip or hostname overrides to the default maximum number of connections.  
connections.max.idle.ms | 600000 | Idle connections timeout: the server socket processor threads close the connections that idle more than this.  
log.roll.jitter.{ms,hours} | 0 | The maximum jitter to subtract from logRollTimeMillis.  
num.recovery.threads.per.data.dir | 1 | The number of threads per data directory to be used for log recovery at startup and flushing at shutdown.  
unclean.leader.election.enable | true | Indicates whether to enable replicas not in the ISR set to be elected as leader as a last resort, even though doing so may result in data loss.  
delete.topic.enable | false | Enable delete topic.  
offsets.topic.num.partitions | 50 | The number of partitions for the offset commit topic. Since changing this after deployment is currently unsupported, we recommend using a higher setting for production (e.g., 100-200).  
offsets.topic.retention.minutes | 1440 | Offsets that are older than this age will be marked for deletion. The actual purge will occur when the log cleaner compacts the offsets topic.  
offsets.retention.check.interval.ms | 600000 | The frequency at which the offset manager checks for stale offsets.  
offsets.topic.replication.factor | 3 | The replication factor for the offset commit topic. A higher setting (e.g., three or four) is recommended in order to ensure higher availability. If the offsets topic is created when fewer brokers than the replication factor then the offsets topic will be created with fewer replicas.  
offsets.topic.segment.bytes | 104857600 | Segment size for the offsets topic. Since it uses a compacted topic, this should be kept relatively low in order to facilitate faster log compaction and loads.  
offsets.load.buffer.size | 5242880 | An offset load occurs when a broker becomes the offset manager for a set of consumer groups (i.e., when it becomes a leader for an offsets topic partition). This setting corresponds to the batch size (in bytes) to use when reading from the offsets segments when loading offsets into the offset manager's cache.  
offsets.commit.required.acks | -1 | The number of acknowledgements that are required before the offset commit can be accepted. This is similar to the producer's acknowledgement setting. In general, the default should not be overridden.  
offsets.commit.timeout.ms | 5000 | The offset commit will be delayed until this timeout or the required number of replicas have received the offset commit. This is similar to the producer request timeout.  
  
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
min.insync.replicas | 1 | min.insync.replicas | When a producer sets request.required.acks to -1, min.insync.replicas specifies the minimum number of replicas that must acknowledge a write for the write to be considered successful. If this minimum cannot be met, then the producer will raise an exception (either NotEnoughReplicas or NotEnoughReplicasAfterAppend).  When used together, min.insync.replicas and request.required.acks allow you to enforce greater durability guarantees. A typical scenario would be to create a topic with a replication factor of 3, set min.insync.replicas to 2, and produce with request.required.acks of -1. This will ensure that the producer raises an exception if a majority of replicas do not receive a write.  
retention.bytes | None | log.retention.bytes | This configuration controls the maximum size a log can grow to before we will discard old log segments to free up space if we are using the "delete" retention policy. By default there is no size limit only a time limit.  
retention.ms | 7 days | log.retention.minutes | This configuration controls the maximum time we will retain a log before we will discard old log segments to free up space if we are using the "delete" retention policy. This represents an SLA on how soon consumers must read their data.  
segment.bytes | 1 GB | log.segment.bytes | This configuration controls the segment file size for the log. Retention and cleaning is always done a file at a time so a larger segment size means fewer files but less granular control over retention.  
segment.index.bytes | 10 MB | log.index.size.max.bytes | This configuration controls the size of the index that maps offsets to file positions. We preallocate this index file and shrink it only after log rolls. You generally should not need to change this setting.  
segment.ms | 7 days | log.roll.hours | This configuration controls the period of time after which Kafka will force the log to roll even if the segment file isn't full to ensure that retention can delete or compact old data.  
segment.jitter.ms | 0 | log.roll.jitter.{ms,hours} | The maximum jitter to subtract from logRollTimeMillis.  
  