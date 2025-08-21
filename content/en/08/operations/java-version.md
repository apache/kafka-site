---
title: Java Version
description: Java Version
weight: 3
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Java Version

Any version of Java 1.6 or later should work fine, we are using 1.6.0_21. Here are our command line options: 
    
    
    java -server -Xms3072m -Xmx3072m -XX:NewSize=256m -XX:MaxNewSize=256m -XX:+UseParNewGC -XX:+UseConcMarkSweepGC 
         -XX:+UseCMSInitiatingOccupancyOnly -XX:+CMSConcurrentMTEnabled -XX:+CMSScavengeBeforeRemark 
         -XX:CMSInitiatingOccupancyFraction=30 
         -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintTenuringDistribution 
         -Xloggc:logs/gc.log -Djava.awt.headless=true
         -Dcom.sun.management.jmxremote -classpath <long list of jars> the.actual.Class
    	
