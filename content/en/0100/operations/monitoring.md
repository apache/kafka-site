---
title: Monitoring
description: Monitoring
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

Kafka uses Yammer Metrics for metrics reporting in both the server and the client. This can be configured to report stats using pluggable stats reporters to hook up to your monitoring system. 

The easiest way to see the available metrics is to fire up jconsole and point it at a running kafka client or server; this will allow browsing all metrics with JMX. 

We do graphing and alerting on the following metrics:   
<table>  
<tr>  
<th>

Description
</th>  
<th>

Mbean name
</th>  
<th>

Normal value
</th> </tr>  
<tr>  
<td>

Message in rate
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Byte in rate
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Request rate
</td>  
<td>

kafka.network:type=RequestMetrics,name=RequestsPerSec,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Byte out rate
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Log flush rate and time
</td>  
<td>

kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs
</td>  
<td>


</td> </tr>  
<tr>  
<td>

\# of under replicated partitions (|ISR| < |all replicas|)
</td>  
<td>

kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
</td>  
<td>

0
</td> </tr>  
<tr>  
<td>

Is controller active on broker
</td>  
<td>

kafka.controller:type=KafkaController,name=ActiveControllerCount
</td>  
<td>

only one broker in the cluster should have 1
</td> </tr>  
<tr>  
<td>

Leader election rate
</td>  
<td>

kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs
</td>  
<td>

non-zero when there are broker failures
</td> </tr>  
<tr>  
<td>

Unclean leader election rate
</td>  
<td>

kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec
</td>  
<td>

0
</td> </tr>  
<tr>  
<td>

Partition counts
</td>  
<td>

kafka.server:type=ReplicaManager,name=PartitionCount
</td>  
<td>

mostly even across brokers
</td> </tr>  
<tr>  
<td>

Leader replica counts
</td>  
<td>

kafka.server:type=ReplicaManager,name=LeaderCount
</td>  
<td>

mostly even across brokers
</td> </tr>  
<tr>  
<td>

ISR shrink rate
</td>  
<td>

kafka.server:type=ReplicaManager,name=IsrShrinksPerSec
</td>  
<td>

If a broker goes down, ISR for some of the partitions will shrink. When that broker is up again, ISR will be expanded once the replicas are fully caught up. Other than that, the expected value for both ISR shrink rate and expansion rate is 0. 
</td> </tr>  
<tr>  
<td>

ISR expansion rate
</td>  
<td>

kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
</td>  
<td>

See above
</td> </tr>  
<tr>  
<td>

Max lag in messages btw follower and leader replicas
</td>  
<td>

kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica
</td>  
<td>

lag should be proportional to the maximum batch size of a produce request.
</td> </tr>  
<tr>  
<td>

Lag in messages per follower replica
</td>  
<td>

kafka.server:type=FetcherLagMetrics,name=ConsumerLag,clientId=([-.\\\w]+),topic=([-.\\\w]+),partition=([0-9]+)
</td>  
<td>

lag should be proportional to the maximum batch size of a produce request.
</td> </tr>  
<tr>  
<td>

Requests waiting in the producer purgatory
</td>  
<td>

kafka.server:type=ProducerRequestPurgatory,name=PurgatorySize
</td>  
<td>

non-zero if ack=-1 is used
</td> </tr>  
<tr>  
<td>

Requests waiting in the fetch purgatory
</td>  
<td>

kafka.server:type=FetchRequestPurgatory,name=PurgatorySize
</td>  
<td>

size depends on fetch.wait.max.ms in the consumer
</td> </tr>  
<tr>  
<td>

Request total time
</td>  
<td>

kafka.network:type=RequestMetrics,name=TotalTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>

broken into queue, local, remote and response send time
</td> </tr>  
<tr>  
<td>

Time the request waiting in the request queue
</td>  
<td>

kafka.network:type=RequestMetrics,name=QueueTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Time the request being processed at the leader
</td>  
<td>

kafka.network:type=RequestMetrics,name=LocalTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Time the request waits for the follower
</td>  
<td>

kafka.network:type=RequestMetrics,name=RemoteTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>

non-zero for produce requests when ack=-1
</td> </tr>  
<tr>  
<td>

Time to send the response
</td>  
<td>

kafka.network:type=RequestMetrics,name=ResponseSendTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Number of messages the consumer lags behind the producer by
</td>  
<td>

kafka.consumer:type=ConsumerFetcherManager,name=MaxLag,clientId=([-.\\\w]+)
</td>  
<td>


</td> </tr>  
<tr>  
<td>

The average fraction of time the network processors are idle
</td>  
<td>

kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent
</td>  
<td>

between 0 and 1, ideally > 0.3
</td> </tr>  
<tr>  
<td>

The average fraction of time the request handler threads are idle
</td>  
<td>

kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent
</td>  
<td>

between 0 and 1, ideally > 0.3
</td> </tr>  
<tr>  
<td>

Quota metrics per client-id
</td>  
<td>

kafka.server:type={Produce|Fetch},client-id==([-.\\\w]+)
</td>  
<td>

Two attributes. throttle-time indicates the amount of time in ms the client-id was throttled. Ideally = 0. byte-rate indicates the data produce/consume rate of the client in bytes/sec.
</td> </tr> </table>

## New producer monitoring

The following metrics are available on new producer instances.   
<table>  
<tr>  
<th>

Metric/Attribute name
</th>  
<th>

Description
</th>  
<th>

Mbean name
</th> </tr>  
<tr>  
<td>

waiting-threads
</td>  
<td>

The number of user threads blocked waiting for buffer memory to enqueue their records.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

buffer-total-bytes
</td>  
<td>

The maximum amount of buffer memory the client can use (whether or not it is currently used).
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

buffer-available-bytes
</td>  
<td>

The total amount of buffer memory that is not being used (either unallocated or in the free list).
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

bufferpool-wait-time
</td>  
<td>

The fraction of time an appender waits for space allocation.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

batch-size-avg
</td>  
<td>

The average number of bytes sent per partition per-request.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

batch-size-max
</td>  
<td>

The max number of bytes sent per partition per-request.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

compression-rate-avg
</td>  
<td>

The average compression rate of record batches.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-queue-time-avg
</td>  
<td>

The average time in ms record batches spent in the record accumulator.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-queue-time-max
</td>  
<td>

The maximum time in ms record batches spent in the record accumulator.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

request-latency-avg
</td>  
<td>

The average request latency in ms.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

request-latency-max
</td>  
<td>

The maximum request latency in ms.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-send-rate
</td>  
<td>

The average number of records sent per second.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

records-per-request-avg
</td>  
<td>

The average number of records per request.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-retry-rate
</td>  
<td>

The average per-second number of retried record sends.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-error-rate
</td>  
<td>

The average per-second number of record sends that resulted in errors.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-size-max
</td>  
<td>

The maximum record size.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-size-avg
</td>  
<td>

The average record size.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

requests-in-flight
</td>  
<td>

The current number of in-flight requests awaiting a response.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

metadata-age
</td>  
<td>

The age in seconds of the current producer metadata being used.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

connection-close-rate
</td>  
<td>

Connections closed per second in the window.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

connection-creation-rate
</td>  
<td>

New connections established per second in the window.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

network-io-rate
</td>  
<td>

The average number of network operations (reads or writes) on all connections per second.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

outgoing-byte-rate
</td>  
<td>

The average number of outgoing bytes sent per second to all servers.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

request-rate
</td>  
<td>

The average number of requests sent per second.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

request-size-avg
</td>  
<td>

The average size of all requests in the window.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

request-size-max
</td>  
<td>

The maximum size of any request sent in the window.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

incoming-byte-rate
</td>  
<td>

Bytes/second read off all sockets.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

response-rate
</td>  
<td>

Responses received sent per second.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

select-rate
</td>  
<td>

Number of times the I/O layer checked for new I/O to perform per second.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

io-wait-time-ns-avg
</td>  
<td>

The average length of time the I/O thread spent waiting for a socket ready for reads or writes in nanoseconds.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

io-wait-ratio
</td>  
<td>

The fraction of time the I/O thread spent waiting.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

io-time-ns-avg
</td>  
<td>

The average length of time for I/O per select call in nanoseconds.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

io-ratio
</td>  
<td>

The fraction of time the I/O thread spent doing I/O.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

connection-count
</td>  
<td>

The current number of active connections.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

outgoing-byte-rate
</td>  
<td>

The average number of outgoing bytes sent per second for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-rate
</td>  
<td>

The average number of requests sent per second for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-size-avg
</td>  
<td>

The average size of all requests in the window for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-size-max
</td>  
<td>

The maximum size of any request sent in the window for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

incoming-byte-rate
</td>  
<td>

The average number of responses received per second for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-latency-avg
</td>  
<td>

The average request latency in ms for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-latency-max
</td>  
<td>

The maximum request latency in ms for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

response-rate
</td>  
<td>

Responses received sent per second for a node.
</td>  
<td>

kafka.producer:type=producer-node-metrics,client-id=([-.\\\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

record-send-rate
</td>  
<td>

The average number of records sent per second for a topic.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+),topic=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

byte-rate
</td>  
<td>

The average number of bytes sent per second for a topic.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+),topic=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

compression-rate
</td>  
<td>

The average compression rate of record batches for a topic.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+),topic=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-retry-rate
</td>  
<td>

The average per-second number of retried record sends for a topic.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+),topic=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

record-error-rate
</td>  
<td>

The average per-second number of record sends that resulted in errors for a topic.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+),topic=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

produce-throttle-time-max
</td>  
<td>

The maximum time in ms a request was throttled by a broker.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+)
</td> </tr>  
<tr>  
<td>

produce-throttle-time-avg
</td>  
<td>

The average time in ms a request was throttled by a broker.
</td>  
<td>

kafka.producer:type=producer-topic-metrics,client-id=([-.\\\w]+)
</td> </tr> </table> We recommend monitoring GC time and other stats and various server stats such as CPU utilization, I/O service time, etc. On the client side, we recommend monitoring the message/byte rate (global and per topic), request rate/size/time, and on the consumer side, max lag in messages among all partitions and min fetch request rate. For a consumer to keep up, max lag needs to be less than a threshold and min fetch rate needs to be larger than 0. 

## Audit

The final alerting we do is on the correctness of the data delivery. We audit that every message that is sent is consumed by all consumers and measure the lag for this to occur. For important topics we alert if a certain completeness is not achieved in a certain time period. The details of this are discussed in KAFKA-260. 
