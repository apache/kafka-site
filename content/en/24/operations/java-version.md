---
title: Java Version
description: Java Version
weight: 4
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Java Version

From a security perspective, we recommend you use the latest released version of JDK 1.8 as older freely available versions have disclosed security vulnerabilities. LinkedIn is currently running JDK 1.8 u5 (looking to upgrade to a newer version) with the G1 collector. LinkedIn's tuning looks like this: 
    
    
      -Xmx6g -Xms6g -XX:MetaspaceSize=96m -XX:+UseG1GC
      -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:G1HeapRegionSize=16M
      -XX:MinMetaspaceFreeRatio=50 -XX:MaxMetaspaceFreeRatio=80
      

For reference, here are the stats on one of LinkedIn's busiest clusters (at peak): 

  * 60 brokers
  * 50k partitions (replication factor 2)
  * 800k messages/sec in
  * 300 MB/sec inbound, 1 GB/sec+ outbound

The tuning looks fairly aggressive, but all of the brokers in that cluster have a 90% GC pause time of about 21ms, and they're doing less than 1 young GC per second. 
