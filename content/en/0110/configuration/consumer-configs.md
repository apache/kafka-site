---
title: Consumer Configs
description: 
weight: 4
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


In 0.9.0.0 we introduced the new Java consumer as a replacement for the older Scala-based simple and high-level consumers. The configs for both new and old consumers are described below. 

## New Consumer Configs

Below is the configuration for the new consumer: {{< include-html file="/static/0110/generated/consumer_config.html" >}} 

## Old Consumer Configs

The essential old consumer configurations are the following: 

  * `group.id`
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

group.id
</td>  
<td>


</td>  
<td>

A string that uniquely identifies the group of consumer processes to which this consumer belongs. By setting the same group id multiple processes indicate that they are all part of the same consumer group.
</td> </tr>  
<tr>  
<td>

zookeeper.connect
</td>  
<td>


</td>  
<td>

Specifies the ZooKeeper connection string in the form `hostname:port` where host and port are the host and port of a ZooKeeper server. To allow connecting through other ZooKeeper nodes when that ZooKeeper machine is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`. 

The server may also have a ZooKeeper chroot path as part of its ZooKeeper connection string which puts its data under some path in the global ZooKeeper namespace. If so the consumer should use the same chroot path in its connection string. For example to give a chroot path of `/chroot/path` you would give the connection string as `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path`.
</td> </tr>  
<tr>  
<td>

consumer.id
</td>  
<td>

null
</td>  
<td>



Generated automatically if not set.


</td> </tr>  
<tr>  
<td>

socket.timeout.ms
</td>  
<td>

30 * 1000
</td>  
<td>

The socket timeout for network requests. The actual timeout set will be max.fetch.wait + socket.timeout.ms.
</td> </tr>  
<tr>  
<td>

socket.receive.buffer.bytes
</td>  
<td>

64 * 1024
</td>  
<td>

The socket receive buffer for network requests
</td> </tr>  
<tr>  
<td>

fetch.message.max.bytes
</td>  
<td>

1024 * 1024
</td>  
<td>

The number of bytes of messages to attempt to fetch for each topic-partition in each fetch request. These bytes will be read into memory for each partition, so this helps control the memory used by the consumer. The fetch request size must be at least as large as the maximum message size the server allows or else it is possible for the producer to send messages larger than the consumer can fetch.
</td> </tr>  
<tr>  
<td>

num.consumer.fetchers
</td>  
<td>

1
</td>  
<td>

The number fetcher threads used to fetch data.
</td> </tr>  
<tr>  
<td>

auto.commit.enable
</td>  
<td>

true
</td>  
<td>

If true, periodically commit to ZooKeeper the offset of messages already fetched by the consumer. This committed offset will be used when the process fails as the position from which the new consumer will begin.
</td> </tr>  
<tr>  
<td>

auto.commit.interval.ms
</td>  
<td>

60 * 1000
</td>  
<td>

The frequency in ms that the consumer offsets are committed to zookeeper.
</td> </tr>  
<tr>  
<td>

queued.max.message.chunks
</td>  
<td>

2
</td>  
<td>

Max number of message chunks buffered for consumption. Each chunk can be up to fetch.message.max.bytes.
</td> </tr>  
<tr>  
<td>

rebalance.max.retries
</td>  
<td>

4
</td>  
<td>

When a new consumer joins a consumer group the set of consumers attempt to "rebalance" the load to assign partitions to each consumer. If the set of consumers changes while this assignment is taking place the rebalance will fail and retry. This setting controls the maximum number of attempts before giving up.
</td> </tr>  
<tr>  
<td>

fetch.min.bytes
</td>  
<td>

1
</td>  
<td>

The minimum amount of data the server should return for a fetch request. If insufficient data is available the request will wait for that much data to accumulate before answering the request.
</td> </tr>  
<tr>  
<td>

fetch.wait.max.ms
</td>  
<td>

100
</td>  
<td>

The maximum amount of time the server will block before answering the fetch request if there isn't sufficient data to immediately satisfy fetch.min.bytes
</td> </tr>  
<tr>  
<td>

rebalance.backoff.ms
</td>  
<td>

2000
</td>  
<td>

Backoff time between retries during rebalance. If not set explicitly, the value in zookeeper.sync.time.ms is used. 
</td> </tr>  
<tr>  
<td>

refresh.leader.backoff.ms
</td>  
<td>

200
</td>  
<td>

Backoff time to wait before trying to determine the leader of a partition that has just lost its leader.
</td> </tr>  
<tr>  
<td>

auto.offset.reset
</td>  
<td>

largest
</td>  
<td>



What to do when there is no initial offset in ZooKeeper or if an offset is out of range:  
* smallest : automatically reset the offset to the smallest offset  
* largest : automatically reset the offset to the largest offset  
* anything else: throw exception to the consumer


</td> </tr>  
<tr>  
<td>

consumer.timeout.ms
</td>  
<td>

-1
</td>  
<td>

Throw a timeout exception to the consumer if no message is available for consumption after the specified interval
</td> </tr>  
<tr>  
<td>

exclude.internal.topics
</td>  
<td>

true
</td>  
<td>

Whether messages from internal topics (such as offsets) should be exposed to the consumer.
</td> </tr>  
<tr>  
<td>

client.id
</td>  
<td>

group id value
</td>  
<td>

The client id is a user-specified string sent in each request to help trace calls. It should logically identify the application making the request.
</td> </tr>  
<tr>  
<td>

zookeeper.session.timeout.ms 
</td>  
<td>

6000
</td>  
<td>

ZooKeeper session timeout. If the consumer fails to heartbeat to ZooKeeper for this period of time it is considered dead and a rebalance will occur.
</td> </tr>  
<tr>  
<td>

zookeeper.connection.timeout.ms
</td>  
<td>

6000
</td>  
<td>

The max time that the client waits while establishing a connection to zookeeper.
</td> </tr>  
<tr>  
<td>

zookeeper.sync.time.ms 
</td>  
<td>

2000
</td>  
<td>

How far a ZK follower can be behind a ZK leader
</td> </tr>  
<tr>  
<td>

offsets.storage
</td>  
<td>

zookeeper
</td>  
<td>

Select where offsets should be stored (zookeeper or kafka).
</td> </tr>  
<tr>  
<td>

offsets.channel.backoff.ms
</td>  
<td>

1000
</td>  
<td>

The backoff period when reconnecting the offsets channel or retrying failed offset fetch/commit requests.
</td> </tr>  
<tr>  
<td>

offsets.channel.socket.timeout.ms
</td>  
<td>

10000
</td>  
<td>

Socket timeout when reading responses for offset fetch/commit requests. This timeout is also used for ConsumerMetadata requests that are used to query for the offset manager.
</td> </tr>  
<tr>  
<td>

offsets.commit.max.retries
</td>  
<td>

5
</td>  
<td>

Retry the offset commit up to this many times on failure. This retry count only applies to offset commits during shut-down. It does not apply to commits originating from the auto-commit thread. It also does not apply to attempts to query for the offset coordinator before committing offsets. i.e., if a consumer metadata request fails for any reason, it will be retried and that retry does not count toward this limit.
</td> </tr>  
<tr>  
<td>

dual.commit.enabled
</td>  
<td>

true
</td>  
<td>

If you are using "kafka" as offsets.storage, you can dual commit offsets to ZooKeeper (in addition to Kafka). This is required during migration from zookeeper-based offset storage to kafka-based offset storage. With respect to any given consumer group, it is safe to turn this off after all instances within that group have been migrated to the new version that commits offsets to the broker (instead of directly to ZooKeeper).
</td> </tr>  
<tr>  
<td>

partition.assignment.strategy
</td>  
<td>

range
</td>  
<td>



Select between the "range" or "roundrobin" strategy for assigning partitions to consumer streams.

The round-robin partition assignor lays out all the available partitions and all the available consumer threads. It then proceeds to do a round-robin assignment from partition to consumer thread. If the subscriptions of all consumer instances are identical, then the partitions will be uniformly distributed. (i.e., the partition ownership counts will be within a delta of exactly one across all consumer threads.) Round-robin assignment is permitted only if: (a) Every topic has the same number of streams within a consumer instance (b) The set of subscribed topics is identical for every consumer instance within the group.

Range partitioning works on a per-topic basis. For each topic, we lay out the available partitions in numeric order and the consumer threads in lexicographic order. We then divide the number of partitions by the total number of consumer streams (threads) to determine the number of partitions to assign to each consumer. If it does not evenly divide, then the first few consumers will have one extra partition.
</td> </tr> </table>

More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.
