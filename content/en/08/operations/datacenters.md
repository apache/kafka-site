---
title: Datacenters
description: Datacenters
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Datacenters

Some deployments will need to manage a data pipeline that spans multiple datacenters. Our approach to this is to deploy a local Kafka cluster in each datacenter and machines in each location interact only with their local cluster. 

For applications that need a global view of all data we use the [mirror maker tool](/08/tools.html) to provide clusters which have aggregate data mirrored from all datacenters. These aggregator clusters are used for reads by applications that require this. 

Likewise in order to support data load into Hadoop which resides in separate facilities we provide local read-only clusters that mirror the production data centers in the facilities where this data load occurs. 

This allows each facility to stand alone and operate even if the inter-datacenter links are unavailable: when this occurs the mirroring falls behind until the link is restored at which time it catches up. 

This deployment pattern allows datacenters to act as independent entities and allows us to manage and tune inter-datacenter replication centrally. 

This is not the only possible deployment pattern. It is possible to read from or write to a remote Kafka cluster over the WAN though TCP tuning will be necessary for high-latency links. 

It is generally not advisable to run a single Kafka cluster that spans multiple datacenters as this will incur very high replication latency both for Kafka writes and Zookeeper writes and neither Kafka nor Zookeeper will remain available if the network partitions. 
