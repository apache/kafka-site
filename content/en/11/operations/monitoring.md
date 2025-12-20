---
title: Monitoring
description: Monitoring
weight: 6
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


Kafka uses Yammer Metrics for metrics reporting in the server and Scala clients. The Java clients use Kafka Metrics, a built-in metrics registry that minimizes transitive dependencies pulled into client applications. Both expose metrics via JMX and can be configured to report stats using pluggable stats reporters to hook up to your monitoring system. 

All Kafka rate metrics have a corresponding cumulative count metric with suffix `-total`. For example, `records-consumed-rate` has a corresponding metric named `records-consumed-total`. 

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

Byte in rate from clients
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Byte in rate from other brokers
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesInPerSec
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

Error rate
</td>  
<td>

kafka.network:type=RequestMetrics,name=ErrorsPerSec,request=([-.\w]+),error=([-.\w]+)
</td>  
<td>

Number of errors in responses counted per-request-type, per-error-code. If a response contains multiple errors, all are counted. error=NONE indicates successful responses.
</td> </tr>  
<tr>  
<td>

Request size in bytes
</td>  
<td>

kafka.network:type=RequestMetrics,name=RequestBytes,request=([-.\w]+)
</td>  
<td>

Size of requests for each request type.
</td> </tr>  
<tr>  
<td>

Temporary memory size in bytes
</td>  
<td>

kafka.network:type=RequestMetrics,name=TemporaryMemoryBytes,request={Produce|Fetch}
</td>  
<td>

Temporary memory used for message format conversions and decompression.
</td> </tr>  
<tr>  
<td>

Message conversion time
</td>  
<td>

kafka.network:type=RequestMetrics,name=MessageConversionsTimeMs,request={Produce|Fetch}
</td>  
<td>

Time in milliseconds spent on message format conversions.
</td> </tr>  
<tr>  
<td>

Message conversion rate
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name={Produce|Fetch}MessageConversionsPerSec,topic=([-.\w]+)
</td>  
<td>

Number of records which required message format conversion.
</td> </tr>  
<tr>  
<td>

Byte out rate to clients
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Byte out rate to other brokers
</td>  
<td>

kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesOutPerSec
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

\# of under minIsr partitions (|ISR| < min.insync.replicas)
</td>  
<td>

kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount
</td>  
<td>

0
</td> </tr>  
<tr>  
<td>

\# of offline log directories
</td>  
<td>

kafka.log:type=LogManager,name=OfflineLogDirectoryCount
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

kafka.server:type=FetcherLagMetrics,name=ConsumerLag,clientId=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)
</td>  
<td>

lag should be proportional to the maximum batch size of a produce request.
</td> </tr>  
<tr>  
<td>

Requests waiting in the producer purgatory
</td>  
<td>

kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Produce
</td>  
<td>

non-zero if ack=-1 is used
</td> </tr>  
<tr>  
<td>

Requests waiting in the fetch purgatory
</td>  
<td>

kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Fetch
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

Time the request waits in the request queue
</td>  
<td>

kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Time the request is processed at the leader
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

Time the request waits in the response queue
</td>  
<td>

kafka.network:type=RequestMetrics,name=ResponseQueueTimeMs,request={Produce|FetchConsumer|FetchFollower}
</td>  
<td>


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

Number of messages the consumer lags behind the producer by. Published by the consumer, not broker.
</td>  
<td>



_Old consumer:_ kafka.consumer:type=ConsumerFetcherManager,name=MaxLag,clientId=([-.\w]+)

_New consumer:_ kafka.consumer:type=consumer-fetch-manager-metrics,client-id={client-id} Attribute: records-lag-max


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

Bandwidth quota metrics per (user, client-id), user or client-id
</td>  
<td>

kafka.server:type={Produce|Fetch},user=([-.\w]+),client-id=([-.\w]+)
</td>  
<td>

Two attributes. throttle-time indicates the amount of time in ms the client was throttled. Ideally = 0. byte-rate indicates the data produce/consume rate of the client in bytes/sec. For (user, client-id) quotas, both user and client-id are specified. If per-client-id quota is applied to the client, user is not specified. If per-user quota is applied, client-id is not specified.
</td> </tr>  
<tr>  
<td>

Request quota metrics per (user, client-id), user or client-id
</td>  
<td>

kafka.server:type=Request,user=([-.\w]+),client-id=([-.\w]+)
</td>  
<td>

Two attributes. throttle-time indicates the amount of time in ms the client was throttled. Ideally = 0. request-time indicates the percentage of time spent in broker network and I/O threads to process requests from client group. For (user, client-id) quotas, both user and client-id are specified. If per-client-id quota is applied to the client, user is not specified. If per-user quota is applied, client-id is not specified.
</td> </tr>  
<tr>  
<td>

Requests exempt from throttling
</td>  
<td>

kafka.server:type=Request
</td>  
<td>

exempt-throttle-time indicates the percentage of time spent in broker network and I/O threads to process requests that are exempt from throttling.
</td> </tr>  
<tr>  
<td>

ZooKeeper client request latency
</td>  
<td>

kafka.server:type=ZooKeeperClientMetrics,name=ZooKeeperRequestLatencyMs
</td>  
<td>

Latency in millseconds for ZooKeeper requests from broker.
</td> </tr>  
<tr>  
<td>

ZooKeeper connection status
</td>  
<td>

kafka.server:type=SessionExpireListener,name=SessionState
</td>  
<td>

Connection status of broker's ZooKeeper session which may be one of Disconnected|SyncConnected|AuthFailed|ConnectedReadOnly|SaslAuthenticated|Expired.
</td> </tr> </table>

## Common monitoring metrics for producer/consumer/connect/streams

The following metrics are available on producer/consumer/connector/streams instances. For specific metrics, please see following sections.   
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

connection-close-rate
</td>  
<td>

Connections closed per second in the window.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

connection-creation-rate
</td>  
<td>

New connections established per second in the window.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

network-io-rate
</td>  
<td>

The average number of network operations (reads or writes) on all connections per second.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

outgoing-byte-rate
</td>  
<td>

The average number of outgoing bytes sent per second to all servers.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

request-rate
</td>  
<td>

The average number of requests sent per second.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

request-size-avg
</td>  
<td>

The average size of all requests in the window.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

request-size-max
</td>  
<td>

The maximum size of any request sent in the window.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

incoming-byte-rate
</td>  
<td>

Bytes/second read off all sockets.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

response-rate
</td>  
<td>

Responses received sent per second.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

select-rate
</td>  
<td>

Number of times the I/O layer checked for new I/O to perform per second.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

io-wait-time-ns-avg
</td>  
<td>

The average length of time the I/O thread spent waiting for a socket ready for reads or writes in nanoseconds.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

io-wait-ratio
</td>  
<td>

The fraction of time the I/O thread spent waiting.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

io-time-ns-avg
</td>  
<td>

The average length of time for I/O per select call in nanoseconds.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

io-ratio
</td>  
<td>

The fraction of time the I/O thread spent doing I/O.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

connection-count
</td>  
<td>

The current number of active connections.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

successful-authentication-rate
</td>  
<td>

Connections that were successfully authenticated using SASL or SSL.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

failed-authentication-rate
</td>  
<td>

Connections that failed authentication.
</td>  
<td>

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)
</td> </tr> </table>

## Common Per-broker metrics for producer/consumer/connect/streams

The following metrics are available on producer/consumer/connector/streams instances. For specific metrics, please see following sections.   
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

outgoing-byte-rate
</td>  
<td>

The average number of outgoing bytes sent per second for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-rate
</td>  
<td>

The average number of requests sent per second for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-size-avg
</td>  
<td>

The average size of all requests in the window for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-size-max
</td>  
<td>

The maximum size of any request sent in the window for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

incoming-byte-rate
</td>  
<td>

The average number of responses received per second for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-latency-avg
</td>  
<td>

The average request latency in ms for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

request-latency-max
</td>  
<td>

The maximum request latency in ms for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr>  
<tr>  
<td>

response-rate
</td>  
<td>

Responses received sent per second for a node.
</td>  
<td>

kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)
</td> </tr> </table>

## Producer monitoring

The following metrics are available on producer instances.   
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

kafka.producer:type=producer-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

buffer-total-bytes
</td>  
<td>

The maximum amount of buffer memory the client can use (whether or not it is currently used).
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

buffer-available-bytes
</td>  
<td>

The total amount of buffer memory that is not being used (either unallocated or in the free list).
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

bufferpool-wait-time
</td>  
<td>

The fraction of time an appender waits for space allocation.
</td>  
<td>

kafka.producer:type=producer-metrics,client-id=([-.\w]+)
</td> </tr> </table>

### Producer Sender Metrics

{{< include-html file="/static/11/generated/producer_metrics.html" >}} 

## New consumer monitoring

The following metrics are available on new consumer instances. 

### Consumer Group Metrics  
  
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

commit-latency-avg
</td>  
<td>

The average time taken for a commit request
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

commit-latency-max
</td>  
<td>

The max time taken for a commit request
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

commit-rate
</td>  
<td>

The number of commit calls per second
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

assigned-partitions
</td>  
<td>

The number of partitions currently assigned to this consumer
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

heartbeat-response-time-max
</td>  
<td>

The max time taken to receive a response to a heartbeat request
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

heartbeat-rate
</td>  
<td>

The average number of heartbeats per second
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

join-time-avg
</td>  
<td>

The average time taken for a group rejoin
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

join-time-max
</td>  
<td>

The max time taken for a group rejoin
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

join-rate
</td>  
<td>

The number of group joins per second
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

sync-time-avg
</td>  
<td>

The average time taken for a group sync
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

sync-time-max
</td>  
<td>

The max time taken for a group sync
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

sync-rate
</td>  
<td>

The number of group syncs per second
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

last-heartbeat-seconds-ago
</td>  
<td>

The number of seconds since the last controller heartbeat
</td>  
<td>

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)
</td> </tr> </table>

### Consumer Fetch Metrics

{{< include-html file="/static/11/generated/consumer_metrics.html" >}} 

## Connect Monitoring

A Connect worker process contains all the producer and consumer metrics as well as metrics specific to Connect. The worker process itself has a number of metrics, while each connector and task have additional metrics. {{< include-html file="/static/11/generated/connect_metrics.html" >}} 

## Streams Monitoring

A Kafka Streams instance contains all the producer and consumer metrics as well as additional metrics specific to streams. By default Kafka Streams has metrics with two recording levels: debug and info. The debug level records all metrics, while the info level records only the thread-level metrics. 

Note that the metrics have a 3-layer hierarchy. At the top level there are per-thread metrics. Each thread has tasks, with their own metrics. Each task has a number of processor nodes, with their own metrics. Each task also has a number of state stores and record caches, all with their own metrics. 

Use the following configuration option to specify which metrics you want collected: 
    
    
    metrics.recording.level="info"

### Thread Metrics

All the following metrics have a recording level of ``info``:   
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

commit-latency-avg
</td>  
<td>

The average execution time in ms for committing, across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

commit-latency-max
</td>  
<td>

The maximum execution time in ms for committing across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

poll-latency-avg
</td>  
<td>

The average execution time in ms for polling, across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

poll-latency-max
</td>  
<td>

The maximum execution time in ms for polling across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

process-latency-avg
</td>  
<td>

The average execution time in ms for processing, across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

process-latency-max
</td>  
<td>

The maximum execution time in ms for processing across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

punctuate-latency-avg
</td>  
<td>

The average execution time in ms for punctuating, across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

punctuate-latency-max
</td>  
<td>

The maximum execution time in ms for punctuating across all running tasks of this thread.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

commit-rate
</td>  
<td>

The average number of commits per second across all tasks.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

poll-rate
</td>  
<td>

The average number of polls per second across all tasks.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

process-rate
</td>  
<td>

The average number of process calls per second across all tasks.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

punctuate-rate
</td>  
<td>

The average number of punctuates per second across all tasks.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

task-created-rate
</td>  
<td>

The average number of newly created tasks per second.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

task-closed-rate
</td>  
<td>

The average number of tasks closed per second.
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

skipped-records-rate
</td>  
<td>

The average number of skipped records per second. 
</td>  
<td>

kafka.streams:type=stream-metrics,client-id=([-.\w]+)
</td> </tr> </table>

### Task Metrics

All the following metrics have a recording level of ``debug``:   
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

commit-latency-avg
</td>  
<td>

The average commit time in ns for this task. 
</td>  
<td>

kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

commit-latency-max
</td>  
<td>

The maximum commit time in ns for this task. 
</td>  
<td>

kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

commit-rate
</td>  
<td>

The average number of commit calls per second. 
</td>  
<td>

kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)
</td> </tr> </table>

### Processor Node Metrics

All the following metrics have a recording level of ``debug``:   
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

process-latency-avg
</td>  
<td>

The average process execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

process-latency-max
</td>  
<td>

The maximum process execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

punctuate-latency-avg
</td>  
<td>

The average punctuate execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

punctuate-latency-max
</td>  
<td>

The maximum punctuate execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

create-latency-avg
</td>  
<td>

The average create execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

create-latency-max
</td>  
<td>

The maximum create execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

destroy-latency-avg
</td>  
<td>

The average destroy execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

destroy-latency-max
</td>  
<td>

The maximum destroy execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

process-rate
</td>  
<td>

The average number of process operations per second. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

punctuate-rate
</td>  
<td>

The average number of punctuate operations per second. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

create-rate
</td>  
<td>

The average number of create operations per second. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

destroy-rate
</td>  
<td>

The average number of destroy operations per second. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

forward-rate
</td>  
<td>

The average rate of records being forwarded downstream, from source nodes only, per second. 
</td>  
<td>

kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)
</td> </tr> </table>

### State Store Metrics

All the following metrics have a recording level of ``debug``:   
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

put-latency-avg
</td>  
<td>

The average put execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-latency-max
</td>  
<td>

The maximum put execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-if-absent-latency-avg
</td>  
<td>

The average put-if-absent execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-if-absent-latency-max
</td>  
<td>

The maximum put-if-absent execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

get-latency-avg
</td>  
<td>

The average get execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

get-latency-max
</td>  
<td>

The maximum get execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

delete-latency-avg
</td>  
<td>

The average delete execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

delete-latency-max
</td>  
<td>

The maximum delete execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-all-latency-avg
</td>  
<td>

The average put-all execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-all-latency-max
</td>  
<td>

The maximum put-all execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

all-latency-avg
</td>  
<td>

The average all operation execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

all-latency-max
</td>  
<td>

The maximum all operation execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

range-latency-avg
</td>  
<td>

The average range execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

range-latency-max
</td>  
<td>

The maximum range execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

flush-latency-avg
</td>  
<td>

The average flush execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

flush-latency-max
</td>  
<td>

The maximum flush execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

restore-latency-avg
</td>  
<td>

The average restore execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

restore-latency-max
</td>  
<td>

The maximum restore execution time in ns. 
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-rate
</td>  
<td>

The average put rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-if-absent-rate
</td>  
<td>

The average put-if-absent rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

get-rate
</td>  
<td>

The average get rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

delete-rate
</td>  
<td>

The average delete rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

put-all-rate
</td>  
<td>

The average put-all rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

all-rate
</td>  
<td>

The average all operation rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

range-rate
</td>  
<td>

The average range rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

flush-rate
</td>  
<td>

The average flush rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

restore-rate
</td>  
<td>

The average restore rate for this store.
</td>  
<td>

kafka.streams:type=stream-[store-type]-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-type]-state-id=([-.\w]+)
</td> </tr> </table>

### Record Cache Metrics

All the following metrics have a recording level of ``debug``:   
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

hitRatio-avg
</td>  
<td>

The average cache hit ratio defined as the ratio of cache read hits over the total cache read requests. 
</td>  
<td>

kafka.streams:type=stream-record-cache-metrics,client-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

hitRatio-min
</td>  
<td>

The mininum cache hit ratio. 
</td>  
<td>

kafka.streams:type=stream-record-cache-metrics,client-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)
</td> </tr>  
<tr>  
<td>

hitRatio-max
</td>  
<td>

The maximum cache hit ratio. 
</td>  
<td>

kafka.streams:type=stream-record-cache-metrics,client-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)
</td> </tr> </table>

## Others

We recommend monitoring GC time and other stats and various server stats such as CPU utilization, I/O service time, etc. On the client side, we recommend monitoring the message/byte rate (global and per topic), request rate/size/time, and on the consumer side, max lag in messages among all partitions and min fetch request rate. For a consumer to keep up, max lag needs to be less than a threshold and min fetch rate needs to be larger than 0. 

## Audit

The final alerting we do is on the correctness of the data delivery. We audit that every message that is sent is consumed by all consumers and measure the lag for this to occur. For important topics we alert if a certain completeness is not achieved in a certain time period. The details of this are discussed in KAFKA-260. 
