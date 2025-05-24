---
title: Monitoring
description: Monitoring
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Monitoring

Kafka uses Yammer Metrics for metrics reporting in the server and Scala clients. The Java clients use Kafka Metrics, a built-in metrics registry that minimizes transitive dependencies pulled into client applications. Both expose metrics via JMX and can be configured to report stats using pluggable stats reporters to hook up to your monitoring system. 

All Kafka rate metrics have a corresponding cumulative count metric with suffix `-total`. For example, `records-consumed-rate` has a corresponding metric named `records-consumed-total`. 

The easiest way to see the available metrics is to fire up jconsole and point it at a running kafka client or server; this will allow browsing all metrics with JMX. 

We do graphing and alerting on the following metrics:  Description | Mbean name | Normal value  
---|---|---  
Message in rate | kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec |   
Byte in rate from clients | kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec |   
Byte in rate from other brokers | kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesInPerSec |   
Request rate | kafka.network:type=RequestMetrics,name=RequestsPerSec,request={Produce|FetchConsumer|FetchFollower} |   
Error rate | kafka.network:type=RequestMetrics,name=ErrorsPerSec,request=([-.\w]+),error=([-.\w]+) | Number of errors in responses counted per-request-type, per-error-code. If a response contains multiple errors, all are counted. error=NONE indicates successful responses.  
Request size in bytes | kafka.network:type=RequestMetrics,name=RequestBytes,request=([-.\w]+) | Size of requests for each request type.  
Temporary memory size in bytes | kafka.network:type=RequestMetrics,name=TemporaryMemoryBytes,request={Produce|Fetch} | Temporary memory used for message format conversions and decompression.  
Message conversion time | kafka.network:type=RequestMetrics,name=MessageConversionsTimeMs,request={Produce|Fetch} | Time in milliseconds spent on message format conversions.  
Message conversion rate | kafka.server:type=BrokerTopicMetrics,name={Produce|Fetch}MessageConversionsPerSec,topic=([-.\w]+) | Number of records which required message format conversion.  
Byte out rate to clients | kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec |   
Byte out rate to other brokers | kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesOutPerSec |   
Log flush rate and time | kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs |   
# of under replicated partitions (|ISR| < |all replicas|) | kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions | 0  
# of under minIsr partitions (|ISR| < min.insync.replicas) | kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount | 0  
# of offline log directories | kafka.log:type=LogManager,name=OfflineLogDirectoryCount | 0  
Is controller active on broker | kafka.controller:type=KafkaController,name=ActiveControllerCount | only one broker in the cluster should have 1  
Leader election rate | kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs | non-zero when there are broker failures  
Unclean leader election rate | kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec | 0  
Partition counts | kafka.server:type=ReplicaManager,name=PartitionCount | mostly even across brokers  
Leader replica counts | kafka.server:type=ReplicaManager,name=LeaderCount | mostly even across brokers  
ISR shrink rate | kafka.server:type=ReplicaManager,name=IsrShrinksPerSec | If a broker goes down, ISR for some of the partitions will shrink. When that broker is up again, ISR will be expanded once the replicas are fully caught up. Other than that, the expected value for both ISR shrink rate and expansion rate is 0.   
ISR expansion rate | kafka.server:type=ReplicaManager,name=IsrExpandsPerSec | See above  
Max lag in messages btw follower and leader replicas | kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica | lag should be proportional to the maximum batch size of a produce request.  
Lag in messages per follower replica | kafka.server:type=FetcherLagMetrics,name=ConsumerLag,clientId=([-.\w]+),topic=([-.\w]+),partition=([0-9]+) | lag should be proportional to the maximum batch size of a produce request.  
Requests waiting in the producer purgatory | kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Produce | non-zero if ack=-1 is used  
Requests waiting in the fetch purgatory | kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Fetch | size depends on fetch.wait.max.ms in the consumer  
Request total time | kafka.network:type=RequestMetrics,name=TotalTimeMs,request={Produce|FetchConsumer|FetchFollower} | broken into queue, local, remote and response send time  
Time the request waits in the request queue | kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request={Produce|FetchConsumer|FetchFollower} |   
Time the request is processed at the leader | kafka.network:type=RequestMetrics,name=LocalTimeMs,request={Produce|FetchConsumer|FetchFollower} |   
Time the request waits for the follower | kafka.network:type=RequestMetrics,name=RemoteTimeMs,request={Produce|FetchConsumer|FetchFollower} | non-zero for produce requests when ack=-1  
Time the request waits in the response queue | kafka.network:type=RequestMetrics,name=ResponseQueueTimeMs,request={Produce|FetchConsumer|FetchFollower} |   
Time to send the response | kafka.network:type=RequestMetrics,name=ResponseSendTimeMs,request={Produce|FetchConsumer|FetchFollower} |   
Number of messages the consumer lags behind the producer by. Published by the consumer, not broker. |  _Old consumer:_ kafka.consumer:type=ConsumerFetcherManager,name=MaxLag,clientId=([-.\w]+) _New consumer:_ kafka.consumer:type=consumer-fetch-manager-metrics,client-id={client-id} Attribute: records-lag-max |   
The average fraction of time the network processors are idle | kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent | between 0 and 1, ideally > 0.3  
The average fraction of time the request handler threads are idle | kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent | between 0 and 1, ideally > 0.3  
Bandwidth quota metrics per (user, client-id), user or client-id | kafka.server:type={Produce|Fetch},user=([-.\w]+),client-id=([-.\w]+) | Two attributes. throttle-time indicates the amount of time in ms the client was throttled. Ideally = 0. byte-rate indicates the data produce/consume rate of the client in bytes/sec. For (user, client-id) quotas, both user and client-id are specified. If per-client-id quota is applied to the client, user is not specified. If per-user quota is applied, client-id is not specified.  
Request quota metrics per (user, client-id), user or client-id | kafka.server:type=Request,user=([-.\w]+),client-id=([-.\w]+) | Two attributes. throttle-time indicates the amount of time in ms the client was throttled. Ideally = 0. request-time indicates the percentage of time spent in broker network and I/O threads to process requests from client group. For (user, client-id) quotas, both user and client-id are specified. If per-client-id quota is applied to the client, user is not specified. If per-user quota is applied, client-id is not specified.  
Requests exempt from throttling | kafka.server:type=Request | exempt-throttle-time indicates the percentage of time spent in broker network and I/O threads to process requests that are exempt from throttling.  
ZooKeeper client request latency | kafka.server:type=ZooKeeperClientMetrics,name=ZooKeeperRequestLatencyMs | Latency in millseconds for ZooKeeper requests from broker.  
ZooKeeper connection status | kafka.server:type=SessionExpireListener,name=SessionState | Connection status of broker's ZooKeeper session which may be one of Disconnected|SyncConnected|AuthFailed|ConnectedReadOnly|SaslAuthenticated|Expired.  
  
## Common monitoring metrics for producer/consumer/connect/streams

The following metrics are available on producer/consumer/connector/streams instances. For specific metrics, please see following sections.  Metric/Attribute name | Description | Mbean name  
---|---|---  
connection-close-rate | Connections closed per second in the window. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
connection-creation-rate | New connections established per second in the window. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
network-io-rate | The average number of network operations (reads or writes) on all connections per second. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
outgoing-byte-rate | The average number of outgoing bytes sent per second to all servers. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
request-rate | The average number of requests sent per second. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
request-size-avg | The average size of all requests in the window. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
request-size-max | The maximum size of any request sent in the window. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
incoming-byte-rate | Bytes/second read off all sockets. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
response-rate | Responses received sent per second. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
select-rate | Number of times the I/O layer checked for new I/O to perform per second. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
io-wait-time-ns-avg | The average length of time the I/O thread spent waiting for a socket ready for reads or writes in nanoseconds. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
io-wait-ratio | The fraction of time the I/O thread spent waiting. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
io-time-ns-avg | The average length of time for I/O per select call in nanoseconds. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
io-ratio | The fraction of time the I/O thread spent doing I/O. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
connection-count | The current number of active connections. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
successful-authentication-rate | Connections that were successfully authenticated using SASL or SSL. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
failed-authentication-rate | Connections that failed authentication. | kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)  
  
## Common Per-broker metrics for producer/consumer/connect/streams

The following metrics are available on producer/consumer/connector/streams instances. For specific metrics, please see following sections.  Metric/Attribute name | Description | Mbean name  
---|---|---  
outgoing-byte-rate | The average number of outgoing bytes sent per second for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
request-rate | The average number of requests sent per second for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
request-size-avg | The average size of all requests in the window for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
request-size-max | The maximum size of any request sent in the window for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
incoming-byte-rate | The average number of responses received per second for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
request-latency-avg | The average request latency in ms for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
request-latency-max | The maximum request latency in ms for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
response-rate | Responses received sent per second for a node. | kafka.producer:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)  
  
## Producer monitoring

The following metrics are available on producer instances.  Metric/Attribute name | Description | Mbean name  
---|---|---  
waiting-threads | The number of user threads blocked waiting for buffer memory to enqueue their records. | kafka.producer:type=producer-metrics,client-id=([-.\w]+)  
buffer-total-bytes | The maximum amount of buffer memory the client can use (whether or not it is currently used). | kafka.producer:type=producer-metrics,client-id=([-.\w]+)  
buffer-available-bytes | The total amount of buffer memory that is not being used (either unallocated or in the free list). | kafka.producer:type=producer-metrics,client-id=([-.\w]+)  
bufferpool-wait-time | The fraction of time an appender waits for space allocation. | kafka.producer:type=producer-metrics,client-id=([-.\w]+)  
  
### Producer Sender Metrics

{{< include-html file="/static/20/generated/producer_metrics.html" >}} 

## New consumer monitoring

The following metrics are available on new consumer instances. 

### Consumer Group Metrics

Metric/Attribute name | Description | Mbean name  
---|---|---  
commit-latency-avg | The average time taken for a commit request | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
commit-latency-max | The max time taken for a commit request | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
commit-rate | The number of commit calls per second | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
assigned-partitions | The number of partitions currently assigned to this consumer | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
heartbeat-response-time-max | The max time taken to receive a response to a heartbeat request | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
heartbeat-rate | The average number of heartbeats per second | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
join-time-avg | The average time taken for a group rejoin | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
join-time-max | The max time taken for a group rejoin | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
join-rate | The number of group joins per second | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
sync-time-avg | The average time taken for a group sync | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
sync-time-max | The max time taken for a group sync | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
sync-rate | The number of group syncs per second | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
last-heartbeat-seconds-ago | The number of seconds since the last controller heartbeat | kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)  
  
### Consumer Fetch Metrics

{{< include-html file="/static/20/generated/consumer_metrics.html" >}} 

## Connect Monitoring

A Connect worker process contains all the producer and consumer metrics as well as metrics specific to Connect. The worker process itself has a number of metrics, while each connector and task have additional metrics. {{< include-html file="/static/20/generated/connect_metrics.html" >}} 

## Streams Monitoring

A Kafka Streams instance contains all the producer and consumer metrics as well as additional metrics specific to streams. By default Kafka Streams has metrics with two recording levels: debug and info. The debug level records all metrics, while the info level records only the thread-level metrics. 

Note that the metrics have a 3-layer hierarchy. At the top level there are per-thread metrics. Each thread has tasks, with their own metrics. Each task has a number of processor nodes, with their own metrics. Each task also has a number of state stores and record caches, all with their own metrics. 

Use the following configuration option to specify which metrics you want collected: 
    
    
    metrics.recording.level="info"

### Thread Metrics

All the following metrics have a recording level of ``info``:  Metric/Attribute name | Description | Mbean name  
---|---|---  
commit-latency-avg | The average execution time in ms for committing, across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
commit-latency-max | The maximum execution time in ms for committing across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
poll-latency-avg | The average execution time in ms for polling, across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
poll-latency-max | The maximum execution time in ms for polling across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
process-latency-avg | The average execution time in ms for processing, across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
process-latency-max | The maximum execution time in ms for processing across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
punctuate-latency-avg | The average execution time in ms for punctuating, across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
punctuate-latency-max | The maximum execution time in ms for punctuating across all running tasks of this thread. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
commit-rate | The average number of commits per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
commit-total | The total number of commit calls across all tasks. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
poll-rate | The average number of polls per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
poll-total | The total number of poll calls across all tasks. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
process-rate | The average number of process calls per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
process-total | The total number of process calls across all tasks. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
punctuate-rate | The average number of punctuates per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
punctuate-total | The total number of punctuate calls across all tasks. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
task-created-rate | The average number of newly created tasks per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
task-created-total | The total number of tasks created. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
task-closed-rate | The average number of tasks closed per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
task-closed-total | The total number of tasks closed. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
skipped-records-rate | The average number of skipped records per second. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
skipped-records-total | The total number of skipped records. | kafka.streams:type=stream-metrics,client-id=([-.\w]+)  
  
### Task Metrics

All the following metrics have a recording level of ``debug``:  Metric/Attribute name | Description | Mbean name  
---|---|---  
commit-latency-avg | The average commit time in ns for this task.  | kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)  
commit-latency-max | The maximum commit time in ns for this task.  | kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)  
commit-rate | The average number of commit calls per second.  | kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)  
commit-total | The total number of commit calls.  | kafka.streams:type=stream-task-metrics,client-id=([-.\w]+),task-id=([-.\w]+)  
  
### Processor Node Metrics

All the following metrics have a recording level of ``debug``:  Metric/Attribute name | Description | Mbean name  
---|---|---  
process-latency-avg | The average process execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
process-latency-max | The maximum process execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
punctuate-latency-avg | The average punctuate execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
punctuate-latency-max | The maximum punctuate execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
create-latency-avg | The average create execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
create-latency-max | The maximum create execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
destroy-latency-avg | The average destroy execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
destroy-latency-max | The maximum destroy execution time in ns.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
process-rate | The average number of process operations per second.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
process-total | The total number of process operations called.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
punctuate-rate | The average number of punctuate operations per second.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
punctuate-total | The total number of punctuate operations called.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
create-rate | The average number of create operations per second.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
create-total | The total number of create operations called.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
destroy-rate | The average number of destroy operations per second.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
destroy-total | The total number of destroy operations called.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
forward-rate | The average rate of records being forwarded downstream, from source nodes only, per second.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
forward-total | The total number of of records being forwarded downstream, from source nodes only.  | kafka.streams:type=stream-processor-node-metrics,client-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)  
  
### State Store Metrics

All the following metrics have a recording level of ``debug``. Note that the ``store-scope`` value is specified in `StoreSupplier#metricsScope()` for user's customized state stores; for built-in state stores, currently we have `in-memory-state`, `in-memory-lru-state`, `rocksdb-state` (for RocksDB backed key-value store), `rocksdb-window-state` (for RocksDB backed window store) and `rocksdb-session-state` (for RocksDB backed session store).  Metric/Attribute name | Description | Mbean name  
---|---|---  
put-latency-avg | The average put execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-latency-max | The maximum put execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-if-absent-latency-avg | The average put-if-absent execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-if-absent-latency-max | The maximum put-if-absent execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
get-latency-avg | The average get execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
get-latency-max | The maximum get execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
delete-latency-avg | The average delete execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
delete-latency-max | The maximum delete execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-all-latency-avg | The average put-all execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-all-latency-max | The maximum put-all execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
all-latency-avg | The average all operation execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
all-latency-max | The maximum all operation execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
range-latency-avg | The average range execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
range-latency-max | The maximum range execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
flush-latency-avg | The average flush execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
flush-latency-max | The maximum flush execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
restore-latency-avg | The average restore execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
restore-latency-max | The maximum restore execution time in ns.  | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-rate | The average put rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-total | The total number of put calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-if-absent-rate | The average put-if-absent rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-if-absent-total | The total number of put-if-absent calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
get-rate | The average get rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
get-total | The total number of get calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
delete-rate | The average delete rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
delete-total | The total number of delete calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-all-rate | The average put-all rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
put-all-total | The total number of put-all calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
all-rate | The average all operation rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
all-total | The total number of all operation calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
range-rate | The average range rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
range-total | The total number of range calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
flush-rate | The average flush rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
flush-total | The total number of flush calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
restore-rate | The average restore rate for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
restore-total | The total number of restore calls for this store. | kafka.streams:type=stream-[store-scope]-metrics,client-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)  
  
### Record Cache Metrics

All the following metrics have a recording level of ``debug``:  Metric/Attribute name | Description | Mbean name  
---|---|---  
hitRatio-avg | The average cache hit ratio defined as the ratio of cache read hits over the total cache read requests.  | kafka.streams:type=stream-record-cache-metrics,client-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)  
hitRatio-min | The mininum cache hit ratio.  | kafka.streams:type=stream-record-cache-metrics,client-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)  
hitRatio-max | The maximum cache hit ratio.  | kafka.streams:type=stream-record-cache-metrics,client-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)  
  
## Others

We recommend monitoring GC time and other stats and various server stats such as CPU utilization, I/O service time, etc. On the client side, we recommend monitoring the message/byte rate (global and per topic), request rate/size/time, and on the consumer side, max lag in messages among all partitions and min fetch request rate. For a consumer to keep up, max lag needs to be less than a threshold and min fetch rate needs to be larger than 0. 

## Audit

The final alerting we do is on the correctness of the data delivery. We audit that every message that is sent is consumed by all consumers and measure the lag for this to occur. For important topics we alert if a certain completeness is not achieved in a certain time period. The details of this are discussed in KAFKA-260. 
