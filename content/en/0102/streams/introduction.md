---
title: Introduction
description: 
weight: 1
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


# Streams

  1. [Core Concepts](/0102/documentation/streams/core-concepts)
  2. [Architecture](/0102/documentation/streams/architecture)
  3. [Developer Guide](/0102/documentation/streams/developer-guide)
     * [Low-level Processor API](/0102/documentation/streams/developer-guide#streams_processor)
     * [High-level Streams DSL](/0102/documentation/streams/developer-guide#streams_dsl)
     * [Application Configuration and Execution](/0102/documentation/streams/developer-guide#streams_execute)
  4. [Upgrade Guide and API Changes](/0102/documentation/streams/upgrade-guide)



# Overview

Kafka Streams is a client library for processing and analyzing data stored in Kafka and either write the resulting data back to Kafka or send the final output to an external system. It builds upon important stream processing concepts such as properly distinguishing between event time and processing time, windowing support, and simple yet efficient management of application state. 

Kafka Streams has a **low barrier to entry** : You can quickly write and run a small-scale proof-of-concept on a single machine; and you only need to run additional instances of your application on multiple machines to scale up to high-volume production workloads. Kafka Streams transparently handles the load balancing of multiple instances of the same application by leveraging Kafka's parallelism model. 

Some highlights of Kafka Streams: 

  * Designed as a **simple and lightweight client library** , which can be easily embedded in any Java application and integrated with any existing packaging, deployment and operational tools that users have for their streaming applications.
  * Has **no external dependencies on systems other than Apache Kafka itself** as the internal messaging layer; notably, it uses Kafka's partitioning model to horizontally scale processing while maintaining strong ordering guarantees.
  * Supports **fault-tolerant local state** , which enables very fast and efficient stateful operations like windowed joins and aggregations.
  * Employs **one-record-at-a-time processing** to achieve millisecond processing latency, and supports **event-time based windowing operations** with late arrival of records.
  * Offers necessary stream processing primitives, along with a **high-level Streams DSL** and a **low-level Processor API**.



Previous [Next](/0102/documentation/streams/core-concepts)

  * [Documentation](/documentation)


