---
title: Consumer Configs
description: Consumer Configs
weight: 2
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


The essential consumer configurations are the following: 

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

The server may also have a ZooKeeper chroot path as part of it's ZooKeeper connection string which puts its data under some path in the global ZooKeeper namespace. If so the consumer should use the same chroot path in its connection string. For example to give a chroot path of `/chroot/path` you would give the connection string as `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path`.
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

The number of byes of messages to attempt to fetch for each topic-partition in each fetch request. These bytes will be read into memory for each partition, so this helps control the memory used by the consumer. The fetch request size must be at least as large as the maximum message size the server allows or else it is possible for the producer to send messages larger than the consumer can fetch.
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

10
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

Backoff time between retries during rebalance.
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
</td> </tr> </table>

More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.
