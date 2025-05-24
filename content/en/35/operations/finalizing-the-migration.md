---
title: Finalizing the migration
description: Finalizing the migration
weight: 16
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Finalizing the migration

Once all brokers have been restarted in KRaft mode, the last step to finalize the migration is to take the KRaft controllers out of migration mode. This is done by removing the "zookeeper.metadata.migration.enable" property from each of their configs and restarting them one at a time. 
    
    
    # Sample KRaft cluster controller.properties listening on 9093
    process.roles=controller
    node.id=3000
    controller.quorum.voters=3000@localhost:9093
    controller.listener.names=CONTROLLER
    listeners=CONTROLLER://:9093
    
    # Disable the migration
    # zookeeper.metadata.migration.enable=true
    
    # Remove ZooKeeper client configuration
    # zookeeper.connect=localhost:2181
    
    # Other configs ...