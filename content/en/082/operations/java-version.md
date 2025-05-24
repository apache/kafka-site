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

We're currently running JDK 1.7 u51, and we've switched over to the G1 collector. If you do this (and we highly recommend it), make sure you're on u51. We tried out u21 in testing, but we had a number of problems with the GC implementation in that version. Our tuning looks like this: 
    
    
    -Xms4g -Xmx4g -XX:PermSize=48m -XX:MaxPermSize=48m -XX:+UseG1GC
    -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35
    

For reference, here are the stats on one of LinkedIn's busiest clusters (at peak): \- 15 brokers \- 15.5k partitions (replication factor 2) \- 400k messages/sec in \- 70 MB/sec inbound, 400 MB/sec+ outbound The tuning looks fairly aggressive, but all of the brokers in that cluster have a 90% GC pause time of about 21ms, and they're doing less than 1 young GC per second. 
