---
title: Preparing for migration
description: Preparing for migration
weight: 14
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Preparing for migration

Before beginning the migration, the Kafka brokers must be upgraded to software version 3.8.1 and have the "inter.broker.protocol.version" configuration set to "3.8". 

It is recommended to enable TRACE level logging for the migration components while the migration is active. This can be done by adding the following log4j configuration to each KRaft controller's "log4j.properties" file. 
    
    
    log4j.logger.org.apache.kafka.metadata.migration=TRACE

It is generally useful to enable DEBUG logging on the KRaft controllers and the ZK brokers during the migration. 
