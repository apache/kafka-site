---
title: Migrating brokers to KRaft
description: Migrating brokers to KRaft
weight: 17
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Migrating brokers to KRaft

Once the KRaft controller completes the metadata migration, the brokers will still be running in ZooKeeper mode. While the KRaft controller is in migration mode, it will continue sending controller RPCs to the ZooKeeper mode brokers. This includes RPCs like UpdateMetadata and LeaderAndIsr. 

To migrate the brokers to KRaft, they simply need to be reconfigured as KRaft brokers and restarted. Using the above broker configuration as an example, we would replace the `broker.id` with `node.id` and add `process.roles=broker`. It is important that the broker maintain the same Broker/Node ID when it is restarted. The zookeeper configurations should be removed at this point. Finally, if you have set `control.plane.listener.name`. please remove it before restarting in KRaft mode. 

If your broker has authorization configured via the `authorizer.class.name` property using `kafka.security.authorizer.AclAuthorizer`, this is also the time to change it to use `org.apache.kafka.metadata.authorizer.StandardAuthorizer` instead. 
    
    
    # Sample KRaft broker server.properties listening on 9092
    process.roles=broker
    node.id=0
    listeners=PLAINTEXT://:9092
    advertised.listeners=PLAINTEXT://localhost:9092
    listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
    
    # Don't set the IBP, KRaft uses "metadata.version" feature flag
    # inter.broker.protocol.version=3.8
    
    # Remove the migration enabled flag
    # zookeeper.metadata.migration.enable=true
    
    # Remove ZooKeeper client configuration
    # zookeeper.connect=localhost:2181
    
    # Keep the KRaft controller quorum configuration
    controller.quorum.voters=3000@localhost:9093
    controller.listener.names=CONTROLLER

Each broker is restarted with a KRaft configuration until the entire cluster is running in KRaft mode. 
