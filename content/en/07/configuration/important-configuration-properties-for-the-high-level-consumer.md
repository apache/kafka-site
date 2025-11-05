---
title: Important configuration properties for the high-level consumer
description: Important configuration properties for the high-level consumer
weight: 2
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Important configuration properties for the high-level consumer: 

More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.

property | default | description  
---|---|---  
`groupid` | groupid | is a string that uniquely identifies a set of consumers within the same consumer group.   
`socket.timeout.ms` | 30000 | controls the socket timeout for network requests   
`socket.buffersize` | 64*1024 | controls the socket receive buffer for network requests  
`fetch.size` | 300 * 1024 | controls the number of bytes of messages to attempt to fetch in one request to the Kafka server  
`backoff.increment.ms` | 1000 | This parameter avoids repeatedly polling a broker node which has no new data. We will backoff every time we get an empty set from the broker for this time period  
`queuedchunks.max` | 100 | the high level consumer buffers the messages fetched from the server internally in blocking queues. This parameter controls the size of those queues  
`autocommit.enable` | true | if set to true, the consumer periodically commits to zookeeper the latest consumed offset of each partition.   
`autocommit.interval.ms` | 10000 | is the frequency that the consumed offsets are committed to zookeeper.   
`autooffset.reset` | smallest | 

  * `smallest`: automatically reset the offset to the smallest offset available on the broker.
  * `largest` : automatically reset the offset to the largest offset available on the broker.
  * `anything else`: throw an exception to the consumer.

  
`consumer.timeout.ms` | -1 | By default, this value is -1 and a consumer blocks indefinitely if no new message is available for consumption. By setting the value to a positive integer, a timeout exception is thrown to the consumer if no message is available for consumption after the specified timeout value.  
`rebalance.retries.max` | 4 | max number of retries during rebalance  
`mirror.topics.whitelist` | "" | Whitelist of topics for this mirror's embedded consumer to consume. At most one of whitelist/blacklist may be specified.  
`mirror.topics.blacklist` | "" | Topics to skip mirroring. At most one of whitelist/blacklist may be specified  
`mirror.consumer.numthreads` | 4 | The number of threads to be used per topic for the mirroring consumer, by default  
  