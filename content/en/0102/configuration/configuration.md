---
title: Configuration
description: 
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

Kafka uses key-value pairs in the [property file format](http://en.wikipedia.org/wiki/.properties) for configuration. These values can be supplied either from a file or programmatically. 

# Broker Configs

The essential configurations are the following: 

  * `broker.id`
  * `log.dirs`
  * `zookeeper.connect` 
Topic-level configurations and defaults are discussed in more detail below. {{< include-html file="/static/0102/generated/kafka_config.html" >}} 

More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.

Topic-level configuration Configurations pertinent to topics have both a server default as well an optional per-topic override. If no per-topic configuration is given the server default is used. The override can be set at topic creation time by giving one or more `--config` options. This example creates a topic named _my-topic_ with a custom max message size and flush rate: 
    
    
      ** > bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic my-topic --partitions 1
              --replication-factor 1 --config max.message.bytes=64000 --config flush.messages=1**
      

Overrides can also be changed or set later using the alter configs command. This example updates the max message size for _my-topic_ : 
    
    
      ** > bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name my-topic --alter --add-config max.message.bytes=128000**
      

To check overrides set on the topic you can do 
    
    
      ** > bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name my-topic --describe**
      

To remove an override you can do 
    
    
      ** > bin/kafka-configs.sh --zookeeper localhost:2181  --entity-type topics --entity-name my-topic --alter --delete-config max.message.bytes**
      

The following are the topic-level configurations. The server's default configuration for this property is given under the Server Default Property heading. A given server default config value only applies to a topic if it does not have an explicit topic config override. {{< include-html file="/static/0102/generated/topic_config.html" >}} 

# Producer Configs

Below is the configuration of the Java producer: {{< include-html file="/static/0102/generated/producer_config.html" >}} 

For those interested in the legacy Scala producer configs, information can be found [ here](http://kafka.apache.org/082/documentation.html#producerconfigs). 

# Consumer Configs

In 0.9.0.0 we introduced the new Java consumer as a replacement for the older Scala-based simple and high-level consumers. The configs for both new and old consumers are described below. 

## New Consumer Configs

Below is the configuration for the new consumer: {{< include-html file="/static/0102/generated/consumer_config.html" >}} 

## Old Consumer Configs

The essential old consumer configurations are the following: 

  * `group.id`
  * `zookeeper.connect` 
Property | Default | Description  
---|---|---  
group.id |  | A string that uniquely identifies the group of consumer processes to which this consumer belongs. By setting the same group id multiple processes indicate that they are all part of the same consumer group.  
zookeeper.connect |  | Specifies the ZooKeeper connection string in the form `hostname:port` where host and port are the host and port of a ZooKeeper server. To allow connecting through other ZooKeeper nodes when that ZooKeeper machine is down you can also specify multiple hosts in the form `hostname1:port1,hostname2:port2,hostname3:port3`.  The server may also have a ZooKeeper chroot path as part of its ZooKeeper connection string which puts its data under some path in the global ZooKeeper namespace. If so the consumer should use the same chroot path in its connection string. For example to give a chroot path of `/chroot/path` you would give the connection string as `hostname1:port1,hostname2:port2,hostname3:port3/chroot/path`.  
consumer.id | null |  Generated automatically if not set.  
socket.timeout.ms | 30 * 1000 | The socket timeout for network requests. The actual timeout set will be max.fetch.wait + socket.timeout.ms.  
socket.receive.buffer.bytes | 64 * 1024 | The socket receive buffer for network requests  
fetch.message.max.bytes | 1024 * 1024 | The number of bytes of messages to attempt to fetch for each topic-partition in each fetch request. These bytes will be read into memory for each partition, so this helps control the memory used by the consumer. The fetch request size must be at least as large as the maximum message size the server allows or else it is possible for the producer to send messages larger than the consumer can fetch.  
num.consumer.fetchers | 1 | The number fetcher threads used to fetch data.  
auto.commit.enable | true | If true, periodically commit to ZooKeeper the offset of messages already fetched by the consumer. This committed offset will be used when the process fails as the position from which the new consumer will begin.  
auto.commit.interval.ms | 60 * 1000 | The frequency in ms that the consumer offsets are committed to zookeeper.  
queued.max.message.chunks | 2 | Max number of message chunks buffered for consumption. Each chunk can be up to fetch.message.max.bytes.  
rebalance.max.retries | 4 | When a new consumer joins a consumer group the set of consumers attempt to "rebalance" the load to assign partitions to each consumer. If the set of consumers changes while this assignment is taking place the rebalance will fail and retry. This setting controls the maximum number of attempts before giving up.  
fetch.min.bytes | 1 | The minimum amount of data the server should return for a fetch request. If insufficient data is available the request will wait for that much data to accumulate before answering the request.  
fetch.wait.max.ms | 100 | The maximum amount of time the server will block before answering the fetch request if there isn't sufficient data to immediately satisfy fetch.min.bytes  
rebalance.backoff.ms | 2000 | Backoff time between retries during rebalance. If not set explicitly, the value in zookeeper.sync.time.ms is used.   
refresh.leader.backoff.ms | 200 | Backoff time to wait before trying to determine the leader of a partition that has just lost its leader.  
auto.offset.reset | largest |  What to do when there is no initial offset in ZooKeeper or if an offset is out of range:  
* smallest : automatically reset the offset to the smallest offset  
* largest : automatically reset the offset to the largest offset  
* anything else: throw exception to the consumer  
consumer.timeout.ms | -1 | Throw a timeout exception to the consumer if no message is available for consumption after the specified interval  
exclude.internal.topics | true | Whether messages from internal topics (such as offsets) should be exposed to the consumer.  
client.id | group id value | The client id is a user-specified string sent in each request to help trace calls. It should logically identify the application making the request.  
zookeeper.session.timeout.ms  | 6000 | ZooKeeper session timeout. If the consumer fails to heartbeat to ZooKeeper for this period of time it is considered dead and a rebalance will occur.  
zookeeper.connection.timeout.ms | 6000 | The max time that the client waits while establishing a connection to zookeeper.  
zookeeper.sync.time.ms  | 2000 | How far a ZK follower can be behind a ZK leader  
offsets.storage | zookeeper | Select where offsets should be stored (zookeeper or kafka).  
offsets.channel.backoff.ms | 1000 | The backoff period when reconnecting the offsets channel or retrying failed offset fetch/commit requests.  
offsets.channel.socket.timeout.ms | 10000 | Socket timeout when reading responses for offset fetch/commit requests. This timeout is also used for ConsumerMetadata requests that are used to query for the offset manager.  
offsets.commit.max.retries | 5 | Retry the offset commit up to this many times on failure. This retry count only applies to offset commits during shut-down. It does not apply to commits originating from the auto-commit thread. It also does not apply to attempts to query for the offset coordinator before committing offsets. i.e., if a consumer metadata request fails for any reason, it will be retried and that retry does not count toward this limit.  
dual.commit.enabled | true | If you are using "kafka" as offsets.storage, you can dual commit offsets to ZooKeeper (in addition to Kafka). This is required during migration from zookeeper-based offset storage to kafka-based offset storage. With respect to any given consumer group, it is safe to turn this off after all instances within that group have been migrated to the new version that commits offsets to the broker (instead of directly to ZooKeeper).  
partition.assignment.strategy | range | Select between the "range" or "roundrobin" strategy for assigning partitions to consumer streams.The round-robin partition assignor lays out all the available partitions and all the available consumer threads. It then proceeds to do a round-robin assignment from partition to consumer thread. If the subscriptions of all consumer instances are identical, then the partitions will be uniformly distributed. (i.e., the partition ownership counts will be within a delta of exactly one across all consumer threads.) Round-robin assignment is permitted only if: (a) Every topic has the same number of streams within a consumer instance (b) The set of subscribed topics is identical for every consumer instance within the group. Range partitioning works on a per-topic basis. For each topic, we lay out the available partitions in numeric order and the consumer threads in lexicographic order. We then divide the number of partitions by the total number of consumer streams (threads) to determine the number of partitions to assign to each consumer. If it does not evenly divide, then the first few consumers will have one extra partition.  
  
More details about consumer configuration can be found in the scala class `kafka.consumer.ConsumerConfig`.

# Kafka Connect Configs

Below is the configuration of the Kafka Connect framework. {{< include-html file="/static/0102/generated/connect_config.html" >}} 

# Kafka Streams Configs

Below is the configuration of the Kafka Streams client library. {{< include-html file="/static/0102/generated/streams_config.html" >}} 
