---
title: Enabling the migration on the brokers
description: Enabling the migration on the brokers
weight: 14
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Enabling the migration on the brokers

Once the KRaft controller quorum has been started, the brokers will need to be reconfigured and restarted. Brokers may be restarted in a rolling fashion to avoid impacting cluster availability. Each broker requires the following configuration to communicate with the KRaft controllers and to enable the migration. 

  * controller.quorum.voters
  * controller.listener.names
  * The controller.listener.name should also be added to listener.security.property.map
  * zookeeper.metadata.migration.enable



Here is a sample config for a broker that is ready for migration:
    
    
    # Sample ZK broker server.properties listening on 9092
    broker.id=0
    listeners=PLAINTEXT://:9092
    advertised.listeners=PLAINTEXT://localhost:9092
    listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
    
    # Set the IBP
    inter.broker.protocol.version=3.5
    
    # Enable the migration
    zookeeper.metadata.migration.enable=true
    
    # ZooKeeper client configuration
    zookeeper.connect=localhost:2181
    
    # KRaft controller quorum configuration
    controller.quorum.voters=3000@localhost:9093
    controller.listener.names=CONTROLLER

_Note: Once the final ZK broker has been restarted with the necessary configuration, the migration will automatically begin._ When the migration is complete, an INFO level log can be observed on the active controller: 
    
    
    Completed migration of metadata from Zookeeper to KRaft
