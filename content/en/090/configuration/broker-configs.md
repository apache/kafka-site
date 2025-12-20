---
title: Broker Configs
description: Broker Configs
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
Topic-level configurations and defaults are discussed in more detail below. {{< include-html file="/static/0110/generated/kafka_config.html" >}} 

More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.

Topic-level configuration Configurations pertinent to topics have both a global default as well an optional per-topic override. If no per-topic configuration is given the global default is used. The override can be set at topic creation time by giving one or more `--config` options. This example creates a topic named _my-topic_ with a custom max message size and flush rate: 
    
    
    ** > bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic my-topic --partitions 1
            --replication-factor 1 --config max.message.bytes=64000 --config flush.messages=1**
    

Overrides can also be changed or set later using the alter topic command. This example updates the max message size for _my-topic_ : 
    
    
    ** > bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic my-topic
        --config max.message.bytes=128000**
    

To remove an override you can do 
    
    
    ** > bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic my-topic
        --deleteConfig max.message.bytes**
    

The following are the topic-level configurations. The server's default configuration for this property is given under the Server Default Property heading, setting this default in the server config allows you to change the default given to topics that have no override specified.   
<table>  
<tr>  
<th>

Property
</th>  
<th>

Default
</th>  
<th>

Server Default Property
</th>  
<th>

Description
</th> </tr>  
<tr>  
<td>

cleanup.policy
</td>  
<td>

delete
</td>  
<td>

log.cleanup.policy
</td>  
<td>

A string that is either "delete" or "compact". This string designates the retention policy to use on old log segments. The default policy ("delete") will discard old segments when their retention time or size limit has been reached. The "compact" setting will enable log compaction on the topic.
</td> </tr>  
<tr>  
<td>

delete.retention.ms
</td>  
<td>

86400000 (24 hours)
</td>  
<td>

log.cleaner.delete.retention.ms
</td>  
<td>

The amount of time to retain delete tombstone markers for log compacted topics. This setting also gives a bound on the time in which a consumer must complete a read if they begin from offset 0 to ensure that they get a valid snapshot of the final stage (otherwise delete tombstones may be collected before they complete their scan).
</td> </tr>  
<tr>  
<td>

flush.messages
</td>  
<td>

None
</td>  
<td>

log.flush.interval.messages
</td>  
<td>

This setting allows specifying an interval at which we will force an fsync of data written to the log. For example if this was set to 1 we would fsync after every message; if it were 5 we would fsync after every five messages. In general we recommend you not set this and use replication for durability and allow the operating system's background flush capabilities as it is more efficient. This setting can be overridden on a per-topic basis (see the per-topic configuration section).
</td> </tr>  
<tr>  
<td>

flush.ms
</td>  
<td>

None
</td>  
<td>

log.flush.interval.ms
</td>  
<td>

This setting allows specifying a time interval at which we will force an fsync of data written to the log. For example if this was set to 1000 we would fsync after 1000 ms had passed. In general we recommend you not set this and use replication for durability and allow the operating system's background flush capabilities as it is more efficient.
</td> </tr>  
<tr>  
<td>

index.interval.bytes
</td>  
<td>

4096
</td>  
<td>

log.index.interval.bytes
</td>  
<td>

This setting controls how frequently Kafka adds an index entry to it's offset index. The default setting ensures that we index a message roughly every 4096 bytes. More indexing allows reads to jump closer to the exact position in the log but makes the index larger. You probably don't need to change this.
</td> </tr>  
<tr>  
<td>

max.message.bytes
</td>  
<td>

1,000,000
</td>  
<td>

message.max.bytes
</td>  
<td>

This is largest message size Kafka will allow to be appended to this topic. Note that if you increase this size you must also increase your consumer's fetch size so they can fetch messages this large.
</td> </tr>  
<tr>  
<td>

min.cleanable.dirty.ratio
</td>  
<td>

0.5
</td>  
<td>

log.cleaner.min.cleanable.ratio
</td>  
<td>

This configuration controls how frequently the log compactor will attempt to clean the log (assuming log compaction is enabled). By default we will avoid cleaning a log where more than 50% of the log has been compacted. This ratio bounds the maximum space wasted in the log by duplicates (at 50% at most 50% of the log could be duplicates). A higher ratio will mean fewer, more efficient cleanings but will mean more wasted space in the log.
</td> </tr>  
<tr>  
<td>

min.insync.replicas
</td>  
<td>

1
</td>  
<td>

min.insync.replicas
</td>  
<td>

When a producer sets request.required.acks to -1, min.insync.replicas specifies the minimum number of replicas that must acknowledge a write for the write to be considered successful. If this minimum cannot be met, then the producer will raise an exception (either NotEnoughReplicas or NotEnoughReplicasAfterAppend). When used together, min.insync.replicas and request.required.acks allow you to enforce greater durability guarantees. A typical scenario would be to create a topic with a replication factor of 3, set min.insync.replicas to 2, and produce with request.required.acks of -1. This will ensure that the producer raises an exception if a majority of replicas do not receive a write.
</td> </tr>  
<tr>  
<td>

retention.bytes
</td>  
<td>

None
</td>  
<td>

log.retention.bytes
</td>  
<td>

This configuration controls the maximum size a log can grow to before we will discard old log segments to free up space if we are using the "delete" retention policy. By default there is no size limit only a time limit.
</td> </tr>  
<tr>  
<td>

retention.ms
</td>  
<td>

7 days
</td>  
<td>

log.retention.minutes
</td>  
<td>

This configuration controls the maximum time we will retain a log before we will discard old log segments to free up space if we are using the "delete" retention policy. This represents an SLA on how soon consumers must read their data.
</td> </tr>  
<tr>  
<td>

segment.bytes
</td>  
<td>

1 GB
</td>  
<td>

log.segment.bytes
</td>  
<td>

This configuration controls the segment file size for the log. Retention and cleaning is always done a file at a time so a larger segment size means fewer files but less granular control over retention.
</td> </tr>  
<tr>  
<td>

segment.index.bytes
</td>  
<td>

10 MB
</td>  
<td>

log.index.size.max.bytes
</td>  
<td>

This configuration controls the size of the index that maps offsets to file positions. We preallocate this index file and shrink it only after log rolls. You generally should not need to change this setting.
</td> </tr>  
<tr>  
<td>

segment.ms
</td>  
<td>

7 days
</td>  
<td>

log.roll.hours
</td>  
<td>

This configuration controls the period of time after which Kafka will force the log to roll even if the segment file isn't full to ensure that retention can delete or compact old data.
</td> </tr>  
<tr>  
<td>

segment.jitter.ms
</td>  
<td>

0
</td>  
<td>

log.roll.jitter.{ms,hours}
</td>  
<td>

The maximum jitter to subtract from logRollTimeMillis.
</td> </tr> </table>
