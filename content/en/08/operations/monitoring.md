---
title: Monitoring
description: Monitoring
weight: 5
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Monitoring

Kafka uses Yammer Metrics for metrics reporting in both the server and the client. This can be configured to report stats using pluggable stats reporters to hook up to your monitoring system. 

The easiest way to see the available metrics to fire up jconsole and point it at a running kafka client or server; this will all browsing all metrics with JMX. 

We pay particular we do graphing and alerting on the following metrics:  Description | Mbean name | Normal value  
---|---|---  
Message in rate | "kafka.server":name="AllTopicsMessagesInPerSec", type="BrokerTopicMetrics" |   
Byte in rate | "kafka.server":name="AllTopicsBytesInPerSec",type="BrokerTopicMetrics" |   
Request rate | "kafka.network":name="{Produce|Fetch-consumer|Fetch-follower}-RequestsPerSec",type="RequestMetrics" |   
Byte out rate | "kafka.server":name="AllTopicsBytesOutPerSec", type="BrokerTopicMetrics" |   
Log flush rate and time | "kafka.log":name="LogFlushRateAndTimeMs",type="LogFlushStats" |   
# of under replicated partitions (|ISR| < |all replicas|) | "kafka.server":name="UnderReplicatedPartitions",type="ReplicaManager" | 0  
Is controller active on broker | "kafka.controller":name="ActiveControllerCount",type="KafkaController" | only one broker in the cluster should have 1  
Leader election rate | "kafka.controller":name="LeaderElectionRateAndTimeMs", type="ControllerStats" | non-zero when there are broker failures  
Unclean leader election rate | "kafka.controller":name="UncleanLeaderElectionsPerSec", type="ControllerStats" | 0  
Partition counts | "kafka.server":name="PartitionCount",type="ReplicaManager" | mostly even across brokers  
Leader replica counts | "kafka.server":name="LeaderCount",type="ReplicaManager" | mostly even across brokers  
ISR shrink rate | "kafka.server":name="ISRShrinksPerSec",type="ReplicaManager" | If a broker goes down, ISR for some of the partitions will shrink. When that broker is up again, ISR will be expanded once the replicas are fully caught up. Other than that, the expected value for both ISR shrink rate and expansion rate is 0.   
ISR expansion rate | "kafka.server":name="ISRExpandsPerSec",type="ReplicaManager" | See above  
Max lag in messages btw follower and leader replicas | "kafka.server":name="([-.\\\w]+)-MaxLag",type="ReplicaFetcherManager" | < replica.lag.max.messages  
Lag in messages per follower replica | "kafka.server":name="([-.\\\w]+)-ConsumerLag",type="FetcherLagMetrics" | < replica.lag.max.messages  
Requests waiting in the producer purgatory | "kafka.server":name="PurgatorySize",type="ProducerRequestPurgatory" | non-zero if ack=-1 is used  
Requests waiting in the fetch purgatory | "kafka.server":name="PurgatorySize",type="FetchRequestPurgatory" | size depends on fetch.wait.max.ms in the consumer  
Request total time | "kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-TotalTimeMs",type="RequestMetrics" | broken into queue, local, remote and response send time  
Time the request waiting in the request queue | "kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-QueueTimeMs",type="RequestMetrics" |   
Time the request being processed at the leader | "kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-LocalTimeMs",type="RequestMetrics" |   
Time the request waits for the follower | "kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-RemoteTimeMs",type="RequestMetrics" | non-zero for produce requests when ack=-1  
Time to send the response | "kafka.network":name="{Produce|Fetch-Consumer|Fetch-Follower}-ResponseSendTimeMs",type="RequestMetrics" |   
Number of messages the consumer lags behind the broker among all partitions consumed | "kafka.consumer":name="([-.\\\w]+)-MaxLag",type="ConsumerFetcherManager" | small and not growing  
The min fetch rate among all fetchers to brokers in a consumer | "kafka.consumer":name="([-.\\\w]+)-MinFetch",type="ConsumerFetcherManager" | >= 1000/fetch.wait.max.ms  
We recommend monitor GC time and other stats and various server stats such as CPU utilization, I/O service time, etc. On the client side, we recommend monitor the message/byte rate (global and per topic), request rate/size/time, and on the consumer side, max lag in messages among all partitions and min fetch request rate. For a consumer to keep up, max lag needs to be less than a threshold and min fetch rate needs to be larger than 0. 

## Audit

The final alerting we do is on the correctness of the data delivery. We audit that every message that is sent is consumed by all consumers and measure the lag for this to occur. For important topics we alert if a certain completeness is not achieved in a certain time period. The details of this are discussed in KAFKA-260. 
