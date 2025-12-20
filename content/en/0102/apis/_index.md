---
title: API
description: 
weight: 2
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


Kafka includes four core apis: 

  1. The Producer API allows applications to send streams of data to topics in the Kafka cluster. 
  2. The Consumer API allows applications to read streams of data from topics in the Kafka cluster. 
  3. The Streams API allows transforming streams of data from input topics to output topics. 
  4. The Connect API allows implementing connectors that continually pull from some source system or application into Kafka or push from Kafka into some sink system or application. 
Kafka exposes all its functionality over a language independent protocol which has clients available in many programming languages. However only the Java clients are maintained as part of the main Kafka project, the others are available as independent open source projects. A list of non-Java clients is available [here](https://cwiki.apache.org/confluence/display/KAFKA/Clients). 

# Producer API

The Producer API allows applications to send streams of data to topics in the Kafka cluster. 

Examples showing how to use the producer are given in the [javadocs](/0102/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html "Kafka 0.10.2 Javadoc"). 

To use the producer, you can use the following maven dependency: 
    
    
    		<dependency>
    			<groupId>org.apache.kafka</groupId>
    			<artifactId>kafka-clients</artifactId>
    			<version>0.10.2.0</version>
    		</dependency>
    	

# Consumer API

The Consumer API allows applications to read streams of data from topics in the Kafka cluster. 

Examples showing how to use the consumer are given in the [javadocs](/0102/javadoc/index.html?org/apache/kafka/clients/consumer/KafkaConsumer.html "Kafka 0.10.2 Javadoc"). 

To use the consumer, you can use the following maven dependency: 
    
    
    		<dependency>
    			<groupId>org.apache.kafka</groupId>
    			<artifactId>kafka-clients</artifactId>
    			<version>0.10.2.0</version>
    		</dependency>
    	

# Streams API

The Streams API allows transforming streams of data from input topics to output topics. 

Examples showing how to use this library are given in the [javadocs](/0102/javadoc/index.html?org/apache/kafka/streams/KafkaStreams.html "Kafka 0.10.2 Javadoc")

Additional documentation on using the Streams API is available [here](/0102/documentation/streams). 

To use Kafka Streams you can use the following maven dependency: 
    
    
    		<dependency>
    			<groupId>org.apache.kafka</groupId>
    			<artifactId>kafka-streams</artifactId>
    			<version>0.10.2.0</version>
    		</dependency>
    	

# Connect API

The Connect API allows implementing connectors that continually pull from some source data system into Kafka or push from Kafka into some sink data system. 

Many users of Connect won't need to use this API directly, though, they can use pre-built connectors without needing to write any code. Additional information on using Connect is available [here](/documentation.html#connect). 

Those who want to implement custom connectors can see the [javadoc](/0102/javadoc/index.html?org/apache/kafka/connect "Kafka 0.10.2 Javadoc"). 

# Legacy APIs

A more limited legacy producer and consumer api is also included in Kafka. These old Scala APIs are deprecated and only still available for compatibility purposes. Information on them can be found here [ here](/081/documentation.html#producerapi "Kafka 0.8.1 Docs"). 
