---
title: Broker Configs
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->


The essential configurations are the following: 

  * `broker.id`
  * `log.dirs`
  * `zookeeper.connect` 
  
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

Each broker is uniquely identified by a non-negative integer id. This id serves as the brokers "name" and allows the broker to be moved to a different host/port without confusing consumers. You can choose any number you like so long as it is unique. 
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

6667
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

Specifies the zookeeper connection string in the form `hostname:port`, where hostname and port are the host and port for a node in your zookeeper cluster. To allow connecting through other zookeeper nodes when that host is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`. 

Zookeeper also allows you to add a "chroot" path which will make all kafka data for this cluster appear under a particular path. This is a way to setup multiple Kafka clusters or other applications on the same zookeeper cluster. To do this give a connection string in the form `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path` which would put all this cluster's data under the path `/chroot/path`. Note that you must create this path yourself prior to starting the broker and consumers must use the same connection string.
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

The default number of partitions per topic.
</td> </tr>  
<tr>  
<td>

log.segment.bytes
</td>  
<td>

1024 * 1024 * 1024
</td>  
<td>

The log for a topic partition is stored as a directory of segment files. This setting controls the size to which a segment file will grow before a new segment is rolled over in the log.
</td> </tr>  
<tr>  
<td>

log.segment.bytes.per.topic
</td>  
<td>

""
</td>  
<td>

This setting allows overriding log.segment.bytes on a per-topic basis.
</td> </tr>  
<tr>  
<td>

log.roll.hours
</td>  
<td>

24 * 7
</td>  
<td>

This setting will force Kafka to roll a new log segment even if the log.segment.bytes size has not been reached.
</td> </tr>  
<tr>  
<td>

log.roll.hours.per.topic
</td>  
<td>

""
</td>  
<td>

This setting allows overriding log.roll.hours on a per-topic basis.
</td> </tr>  
<tr>  
<td>

log.retention.hours
</td>  
<td>

24 * 7
</td>  
<td>

The number of hours to keep a log segment before it is deleted, i.e. the default data retention window for all topics. Note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded.
</td> </tr>  
<tr>  
<td>

log.retention.hours.per.topic
</td>  
<td>

""
</td>  
<td>

A per-topic override for log.retention.hours.
</td> </tr>  
<tr>  
<td>

log.retention.bytes
</td>  
<td>

-1
</td>  
<td>

The amount of data to retain in the log for each topic-partitions. Note that this is the limit per-partition so multiply by the number of partitions to get the total data retained for the topic. Also note that if both log.retention.hours and log.retention.bytes are both set we delete a segment when either limit is exceeded.
</td> </tr>  
<tr>  
<td>

log.retention.bytes.per.topic
</td>  
<td>

""
</td>  
<td>

A per-topic override for log.retention.bytes.
</td> </tr>  
<tr>  
<td>

log.retention.check.interval.ms
</td>  
<td>

300000
</td>  
<td>

The frequency in milliseconds that the log cleaner checks whether any log segment is eligible for deletion to meet the retention policies.
</td> </tr>  
<tr>  
<td>

log.index.size.max.bytes
</td>  
<td>

10 * 1024 * 1024
</td>  
<td>

The maximum size in bytes we allow for the offset index for each log segment. Note that we will always pre-allocate a sparse file with this much space and shrink it down when the log rolls. If the index fills up we will roll a new log segment even if we haven't reached the log.segment.bytes limit.
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

10000
</td>  
<td>

The number of messages written to a log partition before we force an fsync on the log. Setting this higher will improve performance a lot but will increase the window of data at risk in the event of a crash (though that is usually best addressed through replication). If both this setting and log.flush.interval.ms are both used the log will be flushed when either criteria is met.
</td> </tr>  
<tr>  
<td>

log.flush.interval.ms.per.topic
</td>  
<td>

""
</td>  
<td>

The per-topic override for log.flush.interval.messages, e.g., topic1:3000,topic2:6000
</td> </tr>  
<tr>  
<td>

log.flush.scheduler.interval.ms
</td>  
<td>

3000
</td>  
<td>

The frequency in ms that the log flusher checks whether any log is eligible to be flushed to disk.
</td> </tr>  
<tr>  
<td>

log.flush.interval.ms
</td>  
<td>

3000 
</td>  
<td>

The maximum time between fsync calls on the log. If used in conjuction with log.flush.interval.messages the log will be flushed when either criteria is met.
</td> </tr>  
<tr>  
<td>

auto.create.topics.enable
</td>  
<td>

true
</td>  
<td>

Enable auto creation of topic on the server. If this is set to true then attempts to produce, consume, or fetch metadata for a non-existent topic will automatically create it with the default replication factor and number of partitions.
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

10
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

10000
</td>  
<td>

The purge interval (in number of requests) of the fetch request purgatory.
</td> </tr>  
<tr>  
<td>

producer.purgatory.purge.interval.requests
</td>  
<td>

10000
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

Zookeeper session timeout. If the server fails to heartbeat to zookeeper within this period of time it is considered dead. If you set this too low the server may be falsely considered dead; if you set it too high it may take too long to recognize a truly dead server.
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

false
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
</td> </tr> </table>

More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.
