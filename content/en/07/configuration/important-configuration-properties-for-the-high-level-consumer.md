---
title: Important configuration properties for the high-level consumer
description: 
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


# Important configuration properties for the high-level consumer: 

More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.  
  
<table>  
<tr>  
<th>

property
</th>  
<th>

default
</th>  
<th>

description
</th> </tr>  
<tr>  
<td>

`groupid`
</td>  
<td>

groupid
</td>  
<td>

is a string that uniquely identifies a set of consumers within the same consumer group. 
</td> </tr>  
<tr>  
<td>

`socket.timeout.ms`
</td>  
<td>

30000
</td>  
<td>

controls the socket timeout for network requests 
</td> </tr>  
<tr>  
<td>

`socket.buffersize`
</td>  
<td>

64*1024
</td>  
<td>

controls the socket receive buffer for network requests
</td> </tr>  
<tr>  
<td>

`fetch.size`
</td>  
<td>

300 * 1024
</td>  
<td>

controls the number of bytes of messages to attempt to fetch in one request to the Kafka server
</td> </tr>  
<tr>  
<td>

`backoff.increment.ms`
</td>  
<td>

1000
</td>  
<td>

This parameter avoids repeatedly polling a broker node which has no new data. We will backoff every time we get an empty set from the broker for this time period
</td> </tr>  
<tr>  
<td>

`queuedchunks.max`
</td>  
<td>

100
</td>  
<td>

the high level consumer buffers the messages fetched from the server internally in blocking queues. This parameter controls the size of those queues
</td> </tr>  
<tr>  
<td>

`autocommit.enable`
</td>  
<td>

true
</td>  
<td>

if set to true, the consumer periodically commits to zookeeper the latest consumed offset of each partition. 
</td> </tr>  
<tr>  
<td>

`autocommit.interval.ms` 
</td>  
<td>

10000
</td>  
<td>

is the frequency that the consumed offsets are committed to zookeeper. 
</td> </tr>  
<tr>  
<td>

`autooffset.reset`
</td>  
<td>

smallest
</td>  
<td>



  * `smallest`: automatically reset the offset to the smallest offset available on the broker.
  * `largest` : automatically reset the offset to the largest offset available on the broker.
  * `anything else`: throw an exception to the consumer.


</td> </tr>  
<tr>  
<td>

`consumer.timeout.ms`
</td>  
<td>

-1
</td>  
<td>

By default, this value is -1 and a consumer blocks indefinitely if no new message is available for consumption. By setting the value to a positive integer, a timeout exception is thrown to the consumer if no message is available for consumption after the specified timeout value.
</td> </tr>  
<tr>  
<td>

`rebalance.retries.max` 
</td>  
<td>

4
</td>  
<td>

max number of retries during rebalance
</td> </tr>  
<tr>  
<td>

`mirror.topics.whitelist`
</td>  
<td>

""
</td>  
<td>

Whitelist of topics for this mirror's embedded consumer to consume. At most one of whitelist/blacklist may be specified.
</td> </tr>  
<tr>  
<td>

`mirror.topics.blacklist`
</td>  
<td>

""
</td>  
<td>

Topics to skip mirroring. At most one of whitelist/blacklist may be specified
</td> </tr>  
<tr>  
<td>

`mirror.consumer.numthreads`
</td>  
<td>

4
</td>  
<td>

The number of threads to be used per topic for the mirroring consumer, by default
</td> </tr> </table>
