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
