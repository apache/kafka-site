---
title: Quick Start
description: 
weight: 3
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Quick Start

## Step 1: Download the code 

[Download](../downloads.html "Kafka downloads") the 0.8 release. 
    
    
    **> tar xzf kafka-<VERSION>.tgz**
    **> cd kafka-<VERSION>**
    **> ./sbt update**
    **> ./sbt package**
    **> ./sbt assembly-package-dependency**
    

This tutorial assumes you are starting on a fresh zookeeper instance with no pre-existing data. If you want to migrate from an existing 0.7 installation you will need to follow the migration instructions. 

## Step 2: Start the server

Kafka uses zookeeper so you need to first start a zookeeper server if you don't already have one. You can use the convenience script packaged with kafka to get a quick-and-dirty single-node zookeeper instance. 
    
    
    **> bin/zookeeper-server-start.sh config/zookeeper.properties**
    [2013-04-22 15:01:37,495] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
    ...
    

Now start the Kafka server: 
    
    
    **> bin/kafka-server-start.sh config/server.properties**
    [2013-04-22 15:01:47,028] INFO Verifying properties (kafka.utils.VerifiableProperties)
    [2013-04-22 15:01:47,051] INFO Property socket.send.buffer.bytes is overridden to 1048576 (kafka.utils.VerifiableProperties)
    ...
    

## Step 3: Create a topic

Let's create a topic named "test" with a single partition and only one replica: 
    
    
    > **bin/kafka-create-topic.sh --zookeeper localhost:2181 --replica 1 --partition 1 --topic test**
    

We can now see that topic if we run the list topic command: 
    
    
    > **bin/kafka-list-topic.sh --zookeeper localhost:2181**
    

Alternatively, you can also configure your brokers to auto-create topics when a non-existent topic is published to. 

## Step 4: Send some messages

Kafka comes with a command line client that will take input from a file or standard in and send it out as messages to the Kafka cluster. By default each line will be sent as a separate message. 

Run the producer and then type a few messages to send to the server. 
    
    
    > **bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test** 
    This is a message
    This is another message
    

## Step 5: Start a consumer

Kafka also has a command line consumer that will dump out messages to standard out. 
    
    
    **> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning**
    This is a message
    This is another message
    

If you have each of the above commands running in a different terminal then you should now be able to type messages into the producer terminal and see them appear in the consumer terminal. 

All the command line tools have additional options; running the command with no arguments will display usage information documenting them in more detail. 

## Step 6: Setting up a multi-broker cluster

So far we have been running against a single broker, but that's no fun. For Kafka, a single broker is just a cluster of size one, so nothing much changes other than starting a few more broker instances. But just to get feel for it, let's expand our cluster to three nodes (still all on our local machine). 

First we make a config file for each of the brokers: 
    
    
    **> cp config/server.properties config/server-1.properties 
    > cp config/server.properties config/server-2.properties**
    

Now edit these new files and set the following properties: 
    
    
     
    config/server-1.properties:
        broker.id=1
        port=9093
        log.dir=/tmp/kafka-logs-1
     
    config/server-2.properties:
        broker.id=2
        port=9094
        log.dir=/tmp/kafka-logs-2
    

The `broker.id` property is the unique and permanent name of each node in the cluster. We have to override the port and log directory only because we are running these all on the same machine and we want to keep the brokers from trying to all register on the same port or overwrite each others data. 

We already have Zookeeper and our single node started, so we just need to start the two new nodes. However, this time we have to override the JMX port used by java too to avoid clashes with the running node: 
    
    
    **> JMX_PORT=9997 bin/kafka-server-start.sh config/server-1.properties &**
    ...
    **> JMX_PORT=9998 bin/kafka-server-start.sh config/server-2.properties &**
    ...
    

Now create a new topic with a replication factor of three: 
    
    
    > **bin/kafka-create-topic.sh --zookeeper localhost:2181 --replica 3 --partition 1 --topic my-replicated-topic**
    

Okay but now that we have a cluster how can we know which broker is doing what? To see that run the "list topics" command: 
    
    
    > **bin/kafka-list-topic.sh --zookeeper localhost:2181**
    topic: my-replicated-topic  partition: 0  leader: 1  replicas: 1,2,0  isr: 1,2,0
    topic: test	                partition: 0  leader: 0  replicas: 0      isr: 0
    

Here is an explanation of output: 

  * "leader" is the node responsible for all reads and writes for the given partition. Each node would be the leader for a randomly selected portion of the partitions. 
  * "replicas" is the list of nodes that are supposed to server the log for this partition regardless of whether they are currently alive. 
  * "isr" is the set of "in-sync" replicas. This is the subset of the replicas list that is currently alive and caught-up to the leader. 
Note that both topics we created have only a single partition (partition 0). The original topic has no replicas and so it is only present on the leader (node 0), the replicated topic is present on all three nodes with node 1 currently acting as leader and all replicas in sync. 

As before let's publish a few messages message: 
    
    
    > **bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic**
    ...
    **my test message 1**
    **my test message 2**
    **^C** 
    

Now consume this message: 
    
    
    **> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic**
    ...
    my test message 1
    my test message 2
    **^C**
    

Now let's test out fault-tolerance. Kill the broker acting as leader for this topic's only partition: 
    
    
    > **pkill -9 -f server-1.properties**
    

Leadership should switch to one of the slaves: 
    
    
    > **bin/kafka-list-topic.sh --zookeeper localhost:2181**
    ...
    topic: my-replicated-topic	partition: 0	leader: 2	replicas: 1,2,0	isr: 2
    topic: test	partition: 0	leader: 0	replicas: 0	isr: 0
    

And the messages should still be available for consumption even though the leader that took the writes originally is down: 
    
    
    **> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic**
    ...
    my test message 1
    my test message 2
    **^C**
    
