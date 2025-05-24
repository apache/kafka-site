---
title: Provisioning the KRaft controller quorum
description: Provisioning the KRaft controller quorum
weight: 15
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Provisioning the KRaft controller quorum

Two things are needed before the migration can begin. First, the brokers must be configured to support the migration and second, a KRaft controller quorum must be deployed. The KRaft controllers should be provisioned with the same cluster ID as the existing Kafka cluster. This can be found by examining one of the "meta.properties" files in the data directories of the brokers, or by running the following command. 
    
    
    $ bin/zookeeper-shell.sh localhost:2181 get /cluster/id

The KRaft controller quorum should also be provisioned with the latest `metadata.version`. This is done automatically when you format the node with the `kafka-storage.sh` tool. For further instructions on KRaft deployment, please refer to the above documentation. 

In addition to the standard KRaft configuration, the KRaft controllers will need to enable support for the migration as well as provide ZooKeeper connection configuration. 

Here is a sample config for a KRaft controller that is ready for migration: 
    
    
    # Sample KRaft cluster controller.properties listening on 9093
    process.roles=controller
    node.id=3000
    controller.quorum.bootstrap.servers=localhost:9093
    controller.listener.names=CONTROLLER
    listeners=CONTROLLER://:9093
    
    # Enable the migration
    zookeeper.metadata.migration.enable=true
    
    # ZooKeeper client configuration
    zookeeper.connect=localhost:2181
    
    # The inter broker listener in brokers to allow KRaft controller send RPCs to brokers
    inter.broker.listener.name=PLAINTEXT
    
    # Other configs ...

The new standalone controller in the example configuration above should be formatted using the `kafka-storage format --standalone`command.

_Note: The KRaft cluster`node.id` values must be different from any existing ZK broker `broker.id`. In KRaft-mode, the brokers and controllers share the same Node ID namespace._
