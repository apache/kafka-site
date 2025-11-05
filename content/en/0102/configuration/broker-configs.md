---
title: Broker Configs
description: Broker Configs
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

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
