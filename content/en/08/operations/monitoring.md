---
title: Monitoring
description: Monitoring
weight: 5
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

Kafka uses Yammer Metrics for metrics reporting in both the server and the client. This can be configured to report stats using pluggable stats reporters to hook up to your monitoring system. 

The easiest way to see the available metrics to fire up jconsole and point it at a running kafka client or server; this will all browsing all metrics with JMX. 

We pay particular we do graphing and alerting on the following metrics:   
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

"kafka.server":name="AllTopicsMessagesInPerSec", type="BrokerTopicMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Byte in rate
</td>  
<td>

"kafka.server":name="AllTopicsBytesInPerSec",type="BrokerTopicMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Request rate
</td>  
<td>

"kafka.network":name="{Produce|Fetch-consumer|Fetch-follower}-RequestsPerSec",type="RequestMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Byte out rate
</td>  
<td>

"kafka.server":name="AllTopicsBytesOutPerSec", type="BrokerTopicMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Log flush rate and time
</td>  
<td>

"kafka.log":name="LogFlushRateAndTimeMs",type="LogFlushStats"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

\# of under replicated partitions (|ISR| < |all replicas|)
</td>  
<td>

"kafka.server":name="UnderReplicatedPartitions",type="ReplicaManager"
</td>  
<td>

0
</td> </tr>  
<tr>  
<td>

Is controller active on broker
</td>  
<td>

"kafka.controller":name="ActiveControllerCount",type="KafkaController"
</td>  
<td>

only one broker in the cluster should have 1
</td> </tr>  
<tr>  
<td>

Leader election rate
</td>  
<td>

"kafka.controller":name="LeaderElectionRateAndTimeMs", type="ControllerStats"
</td>  
<td>

non-zero when there are broker failures
</td> </tr>  
<tr>  
<td>

Unclean leader election rate
</td>  
<td>

"kafka.controller":name="UncleanLeaderElectionsPerSec", type="ControllerStats"
</td>  
<td>

0
</td> </tr>  
<tr>  
<td>

Partition counts
</td>  
<td>

"kafka.server":name="PartitionCount",type="ReplicaManager"
</td>  
<td>

mostly even across brokers
</td> </tr>  
<tr>  
<td>

Leader replica counts
</td>  
<td>

"kafka.server":name="LeaderCount",type="ReplicaManager"
</td>  
<td>

mostly even across brokers
</td> </tr>  
<tr>  
<td>

ISR shrink rate
</td>  
<td>

"kafka.server":name="ISRShrinksPerSec",type="ReplicaManager"
</td>  
<td>

If a broker goes down, ISR for some of the partitions will shrink. When that broker is up again, ISR will be expanded once the replicas are fully caught up. Other than that, the expected value for both ISR shrink rate and expansion rate is 0. 
</td> </tr>  
<tr>  
<td>

ISR expansion rate
</td>  
<td>

"kafka.server":name="ISRExpandsPerSec",type="ReplicaManager"
</td>  
<td>

See above
</td> </tr>  
<tr>  
<td>

Max lag in messages btw follower and leader replicas
</td>  
<td>

"kafka.server":name="([-.\\\w]+)-MaxLag",type="ReplicaFetcherManager"
</td>  
<td>

< replica.lag.max.messages
</td> </tr>  
<tr>  
<td>

Lag in messages per follower replica
</td>  
<td>

"kafka.server":name="([-.\\\w]+)-ConsumerLag",type="FetcherLagMetrics"
</td>  
<td>

< replica.lag.max.messages
</td> </tr>  
<tr>  
<td>

Requests waiting in the producer purgatory
</td>  
<td>

"kafka.server":name="PurgatorySize",type="ProducerRequestPurgatory"
</td>  
<td>

non-zero if ack=-1 is used
</td> </tr>  
<tr>  
<td>

Requests waiting in the fetch purgatory
</td>  
<td>

"kafka.server":name="PurgatorySize",type="FetchRequestPurgatory"
</td>  
<td>

size depends on fetch.wait.max.ms in the consumer
</td> </tr>  
<tr>  
<td>

Request total time
</td>  
<td>

"kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-TotalTimeMs",type="RequestMetrics"
</td>  
<td>

broken into queue, local, remote and response send time
</td> </tr>  
<tr>  
<td>

Time the request waiting in the request queue
</td>  
<td>

"kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-QueueTimeMs",type="RequestMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Time the request being processed at the leader
</td>  
<td>

"kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-LocalTimeMs",type="RequestMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Time the request waits for the follower
</td>  
<td>

"kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-RemoteTimeMs",type="RequestMetrics"
</td>  
<td>

non-zero for produce requests when ack=-1
</td> </tr>  
<tr>  
<td>

Time to send the response
</td>  
<td>

"kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-ResponseSendTimeMs",type="RequestMetrics"
</td>  
<td>


</td> </tr>  
<tr>  
<td>

Number of messages the consumer lags behind the broker among all partitions consumed
</td>  
<td>

"kafka.consumer":name="([-.\\\w]+)-MaxLag",type="ConsumerFetcherManager"
</td>  
<td>

small and not growing
</td> </tr>  
<tr>  
<td>

The min fetch rate among all fetchers to brokers in a consumer
</td>  
<td>

"kafka.consumer":name="([-.\\\w]+)-MinFetch",type="ConsumerFetcherManager"
</td>  
<td>

>= 1000/fetch.wait.max.ms
</td> </tr> </table> We recommend monitor GC time and other stats and various server stats such as CPU utilization, I/O service time, etc. On the client side, we recommend monitor the message/byte rate (global and per topic), request rate/size/time, and on the consumer side, max lag in messages among all partitions and min fetch request rate. For a consumer to keep up, max lag needs to be less than a threshold and min fetch rate needs to be larger than 0. 

## Audit

The final alerting we do is on the correctness of the data delivery. We audit that every message that is sent is consumed by all consumers and measure the lag for this to occur. For important topics we alert if a certain completeness is not achieved in a certain time period. The details of this are discussed in KAFKA-260. 
