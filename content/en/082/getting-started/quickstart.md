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

This tutorial assumes you are starting fresh and have no existing Kafka or ZooKeeper data. 

## Step 1: Download the code 

[Download](https://www.apache.org/dyn/closer.cgi?path=/kafka/0.8.2.0/kafka_2.10-0.8.2.0.tgz "Kafka downloads") the 0.8.2.0 release and un-tar it. 
    
    
    > **tar -xzf kafka_2.10-0.8.2.0.tgz**
    > **cd kafka_2.10-0.8.2.0**
    

## Step 2: Start the server

Kafka uses ZooKeeper so you need to first start a ZooKeeper server if you don't already have one. You can use the convenience script packaged with kafka to get a quick-and-dirty single-node ZooKeeper instance. 
    
    
    > **bin/zookeeper-server-start.sh config/zookeeper.properties**
    [2013-04-22 15:01:37,495] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
    ...
    

Now start the Kafka server: 
    
    
    > **bin/kafka-server-start.sh config/server.properties**
    [2013-04-22 15:01:47,028] INFO Verifying properties (kafka.utils.VerifiableProperties)
    [2013-04-22 15:01:47,051] INFO Property socket.send.buffer.bytes is overridden to 1048576 (kafka.utils.VerifiableProperties)
    ...
    

## Step 3: Create a topic

Let's create a topic named "test" with a single partition and only one replica: 
    
    
    > **bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test**
    

We can now see that topic if we run the list topic command: 
    
    
    > **bin/kafka-topics.sh --list --zookeeper localhost:2181**
    test
    

Alternatively, instead of manually creating topics you can also configure your brokers to auto-create topics when a non-existent topic is published to. 

## Step 4: Send some messages

Kafka comes with a command line client that will take input from a file or from standard input and send it out as messages to the Kafka cluster. By default each line will be sent as a separate message. 

Run the producer and then type a few messages into the console to send to the server. 
    
    
    > **bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test** 
    **This is a message**
    **This is another message**
    

## Step 5: Start a consumer

Kafka also has a command line consumer that will dump out messages to standard output. 
    
    
    > **bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning**
    This is a message
    This is another message
    

If you have each of the above commands running in a different terminal then you should now be able to type messages into the producer terminal and see them appear in the consumer terminal. 

All of the command line tools have additional options; running the command with no arguments will display usage information documenting them in more detail. 

## Step 6: Setting up a multi-broker cluster

So far we have been running against a single broker, but that's no fun. For Kafka, a single broker is just a cluster of size one, so nothing much changes other than starting a few more broker instances. But just to get feel for it, let's expand our cluster to three nodes (still all on our local machine). 

First we make a config file for each of the brokers: 
    
    
    > **cp config/server.properties config/server-1.properties** 
    > **cp config/server.properties config/server-2.properties**
    

Now edit these new files and set the following properties: 
    
    
     
    config/server-1.properties:
        broker.id=1
        port=9093
        log.dir=/tmp/kafka-logs-1
     
    config/server-2.properties:
        broker.id=2
        port=9094
        log.dir=/tmp/kafka-logs-2
    

The `broker.id` property is the unique and permanent name of each node in the cluster. We have to override the port and log directory only because we are running these all on the same machine and we want to keep the brokers from all trying to register on the same port or overwrite each others data. 

We already have Zookeeper and our single node started, so we just need to start the two new nodes: 
    
    
    > **bin/kafka-server-start.sh config/server-1.properties &**
    ...
    > **bin/kafka-server-start.sh config/server-2.properties &**
    ...
    

Now create a new topic with a replication factor of three: 
    
    
    > **bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic**
    

Okay but now that we have a cluster how can we know which broker is doing what? To see that run the "describe topics" command: 
    
    
    > **bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic**
    Topic:my-replicated-topic	PartitionCount:1	ReplicationFactor:3	Configs:
    	Topic: my-replicated-topic	Partition: 0	Leader: 1	Replicas: 1,2,0	Isr: 1,2,0
    

Here is an explanation of output. The first line gives a summary of all the partitions, each additional line gives information about one partition. Since we have only one partition for this topic there is only one line. 

  * "leader" is the node responsible for all reads and writes for the given partition. Each node will be the leader for a randomly selected portion of the partitions. 
  * "replicas" is the list of nodes that replicate the log for this partition regardless of whether they are the leader or even if they are currently alive. 
  * "isr" is the set of "in-sync" replicas. This is the subset of the replicas list that is currently alive and caught-up to the leader. 
Note that in my example node 1 is the leader for the only partition of the topic. 

We can run the same command on the original topic we created to see where it is: 
    
    
    > **bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test**
    Topic:test	PartitionCount:1	ReplicationFactor:1	Configs:
    	Topic: test	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
    

So there is no surprise there--the original topic has no replicas and is on server 0, the only server in our cluster when we created it. 

Let's publish a few messages to our new topic: 
    
    
    > **bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic**
    ...
    **my test message 1**
    **my test message 2**
    **^C** 
    

Now let's consume these messages: 
    
    
    > **bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic**
    ...
    my test message 1
    my test message 2
    **^C**
    

Now let's test out fault-tolerance. Broker 1 was acting as the leader so let's kill it: 
    
    
    > **ps | grep server-1.properties**
    _7564_ ttys002    0:15.91 /System/Library/Frameworks/JavaVM.framework/Versions/1.6/Home/bin/java...
    > **kill -9 7564**
    

Leadership has switched to one of the slaves and node 1 is no longer in the in-sync replica set: 
    
    
    > **bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic**
    Topic:my-replicated-topic	PartitionCount:1	ReplicationFactor:3	Configs:
    	Topic: my-replicated-topic	Partition: 0	Leader: 2	Replicas: 1,2,0	Isr: 2,0
    

But the messages are still be available for consumption even though the leader that took the writes originally is down: 
    
    
    > **bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic**
    ...
    my test message 1
    my test message 2
    **^C**
    
