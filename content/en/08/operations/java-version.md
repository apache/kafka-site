---
title: Java Version
description: Java Version
weight: 3
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->


Any version of Java 1.6 or later should work fine, we are using 1.6.0_21. Here are our command line options: 
    
    
    java -server -Xms3072m -Xmx3072m -XX:NewSize=256m -XX:MaxNewSize=256m -XX:+UseParNewGC -XX:+UseConcMarkSweepGC 
         -XX:+UseCMSInitiatingOccupancyOnly -XX:+CMSConcurrentMTEnabled -XX:+CMSScavengeBeforeRemark 
         -XX:CMSInitiatingOccupancyFraction=30 
         -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintTenuringDistribution 
         -Xloggc:logs/gc.log -Djava.awt.headless=true
         -Dcom.sun.management.jmxremote -classpath <long list of jars> the.actual.Class
    	
