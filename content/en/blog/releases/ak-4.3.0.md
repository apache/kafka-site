---
date: 2026-05-22
title: Apache Kafka 4.3.0 Release Announcement
linkTitle: AK 4.3.0
author: Mickael Maison
aliases:
  - /blog/2026/05/22/apache-kafka-4.3.0-release-announcement/
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

We are proud to announce the release of Apache Kafka® 4.3. This release contains many new features and improvements. This blog post will highlight some of the more prominent ones. For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/4.3.0/RELEASE_NOTES.html).

With 25 KIPs and over 600 commits since 4.2.0, this release introduces many new features, improvements and bug fixes to all the components.


See the [Upgrading to 4.3](https://kafka.apache.org/documentation.html#upgrade_4_3_0) section in the documentation for the list of notable changes and detailed upgrade steps.

## Deprecation Notices
* [KIP-1244 Drop support for streams-scala in Kafka 5.0 (deprecate in 4.3)](https://cwiki.apache.org/confluence/x/r4LMFw)     
  Deprecates the streams-scala module. Marked for removal in Apache Kafka 5.0.

* [KIP-1237: Deprecate group.coordinator.rebalance.protocols config](https://cwiki.apache.org/confluence/x/jIqmFw)    
  Deprecates the `group.coordinator.rebalance.protocols` broker configuration. Marked for removal in Apache Kafka 5.0.

* [KIP-1280: Update MirrorMaker to use KIP-877 to emit metrics](https://cwiki.apache.org/confluence/x/a4s8G)    
  Deprecates the existing MirrorMaker metrics. They are marked for removal in Apache Kafka 5.0. Users should transition to the new metric names.

## Kafka Broker, Controller, Producer, Consumer and Admin Client

* [KIP-1023: Follower fetch from tiered offset](https://cwiki.apache.org/confluence/x/8op3EQ)    
  Adds a new broker configuration, `follower.fetch.last.tiered.offset.enable` (default: `false`). When enabled the last tiered offset is used as the start offset when bootstrapping a new follower.

* [KIP-1066: Mechanism to cordon brokers and log directories](https://cwiki.apache.org/confluence/x/Lg_TEg)    
  Introduces a new configuration, `cordoned.log.dirs` to cordon log directories. New partitions cannot be placed on a cordoned log directory. This can be used when scaling or [decommissioning brokers or log directories](https://kafka.apache.org/43/operations/basic-kafka-operations/#decommissioning-brokers-and-log-directories).

* [KIP-1196: Introduce group.coordinator.append.max.buffer.size config](https://cwiki.apache.org/confluence/x/hA5JFg)    
  Introduces the `group.coordinator.append.max.buffer.size` and `share.coordinator.append.max.buffer.size` configurations to set the maximum buffer size the coordinators can use. There are also metrics to track the buffer usage.

* [KIP-1208: Add prefix to TopicBasedRemoteLogMetadataManagerConfig to enable setting admin configs](https://cwiki.apache.org/confluence/x/vYqhFg)    
  Introduces a new prefix `remote.log.metadata.admin.` for setting configurations for the admin client used by the tiered storage's `RemoteLogMetadataManager`.

* [KIP-1211: Align the behavior of num.partitions and default.replication.factor for topic creation](https://cwiki.apache.org/confluence/x/WIrHFg)    
  Fixes inconsistencies how `num.partitions` and `default.replication.factor` were applied when creating topics.

* [KIP-1219: Configurations for KRaft Fetch and FetchSnapshot Byte Size](https://cwiki.apache.org/confluence/x/yQkGFw)    
  Adds new broker configurations, `controller.quorum.fetch.snapshot.max.bytes` and `controller.quorum.fetch.max.bytes`, to control the maximum amount of data Fetch and FetchSnapshot requests can retrieve.

* [KIP-1235: Correct the default min.insync.replicas to 2 for the __remote_log_metadata topic](https://cwiki.apache.org/confluence/x/yommFw)
  Adds a new broker configuration, `remote.log.metadata.topic.min.isr`, to set the minimum in-sync replicas for the internal topic used by tiered storage.

* [KIP-1240: Additional group configurations for share groups](https://cwiki.apache.org/confluence/x/tIHMFw)    
  Adds a number of new broker and group configurations to control the behavior of share groups.

* [KIP-1251: Assignment epochs for consumer groups](https://cwiki.apache.org/confluence/x/8ITMFw)    
  Improves the member epoch validation logic to avoid unnecessary fencing of group members.

* [KIP-1257: Partition Size Percentage Metrics for Storage Monitoring](https://cwiki.apache.org/confluence/x/MAEXG)    
  Introduces new metrics to track how much of the maximum retention each topic-partition currently uses.

* [KIP-1258: Add Support for OAuth Client Assertion to client_credentials Grant Type](https://cwiki.apache.org/confluence/x/dwEXG)    
  Adds support for client assertion authentication to client_credentials grant type with OAuth to enhance security and compatibility with OAuth providers.

* [KIP-1263: Group Coordinator Assignment Batching and Offload](https://cwiki.apache.org/confluence/x/DIE8G)    
  Improves the group coordinator assignment logic to avoid recomputing assignments when unnecessary.

* [KIP-1274: Deprecate and remove support for Classic rebalance protocol in KafkaConsumer (Phase 1)](https://cwiki.apache.org/confluence/x/PoY8G)    
  Logs a message when starting a consumer with the `classic` rebalance protocol recommending to use the new consumer rebalance protocol instead as the `classic` protocol will be deprecated in a future release.

## Kafka Streams

* [KIP-1035: StateStore managed changelog offsets](https://cwiki.apache.org/confluence/x/aQviEQ)    
  Adds methods to the `StateStore` API to manage changelog offsets. This is an internal runtime change, and only relevant for custom `StateStore` implementations.

* [KIP-1247: Make Bytes utils class part of the public API](https://cwiki.apache.org/confluence/x/DYTMFw)    
  Exposes the `Bytes` class as part of the public API so it appears in the javadoc.

* [KIP-1250: Add metric to track size of in-memory state stores](https://cwiki.apache.org/confluence/x/noTMFw)    
  Adds new metrics tracking the number of keys in the in-memory state stores.

* [KIP-1259: Add configuration to wipe Kafka Streams local state on startup](https://cwiki.apache.org/confluence/x/XgIXG)    
  Adds a new configuration, `state.cleanup.dir.max.age.ms`, to automatically delete state directories that have not been modified for that duration on startup.

* [KIP-1270: Extend ProcessingExceptionHandler for GlobalThread](https://cwiki.apache.org/confluence/x/qIE8G)    
  Adds a new configuration, `processing.exception.handler.global.enabled`, to enable `ProcessingExceptionHandler` to handle `GlobalKTable` exceptions.

* [KIP-1271: Allow to Store Headers in State Stores](https://cwiki.apache.org/confluence/x/QIM8G)    
  Extends the Processor API to support record headers in state stores.

* [KIP-1285: DSL Opt-in Support for Headers-Aware State Stores](https://cwiki.apache.org/confluence/x/4ow8G)    
  Exposes Headers-Aware State Stores (KIP-1271) to the DSL API.

## Kafka Connect

* [KIP-1239: Batch offset translation in RemoteClusterUtils](https://cwiki.apache.org/confluence/x/h4HMFw)    
  Adds a new method `RemoteClusterUtils.translateOffsets()` to translate the committed offsets of several consumer groups at the same time.

* [KIP-1273: Improve Connect configurable components discoverability](https://cwiki.apache.org/confluence/x/J4U8G)    
  Introduces a new interface, `ConnectPlugin`, that all Kafka Connect plugins implement to ensure common methods across all plugin types. 

* [KIP-1280: Update MirrorMaker to use KIP-877 to emit metrics](https://cwiki.apache.org/confluence/x/a4s8G)    
  Adds a new configuration, `metric.names.formats`, for `MirrorSourceConnector` and `MirrorCheckpointConnector` to opt-in to the new metric names.


## Summary

Ready to get started with Apache Kafka 4.3.0? Check out all the details in the [upgrade notes](https://kafka.apache.org/documentation.html#upgrade_4_3_0) and the [release notes](https://archive.apache.org/dist/kafka/4.3.0/RELEASE_NOTES.html), and [download](https://kafka.apache.org/downloads) Apache Kafka 4.3.0.

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 147 contributors (and 3 AIs):  
高春晖, 조형준, Abhijeet Kumar, Abhinav Dixit, Alieh Saeedi, Alyssa Huang, Andrew Schofield, Aneesh Garg, Angelo R., Anton Vasanth, ANUSHREE BONDIA, Apoorv Mittal, Arpit Goyal, Artem Livshits, averemee-si, Bill Bejeck, Bolin Lin, Calvin Liu, Chang-Chi Hsu, Chang-Yu Huang, Chia-Ping Tsai, Chia-Yi Chiu, ChickenchickenLove, Chih-Yuan Chien, Chirag Wadhwa, Chris Egerton, Christo Lolov, Claude, Claude Sonnet 4.6, Copilot, cui, Dale Lane, David Arthur, David Jacot, Deepak Goyal, Dejan Stojadinović, dengziming, Ding, Dmitry Werner, Dongnuo Lyu, Donny Nadolny, Edoardo Comar, Eduwer Camacaro, Emanuele Rabino, Emmanuel Oppong, Eric Chang, Erik Anderson, Evan Zhou, Federico Valeri, Fiore Mario Vitale, gabriellefu, Gaurav Narula, Gianmarco, Giuseppe Lillo, gomudayya, Gyeongwon, Do, Harish Vishwanath, Hector Geraldino, high.lee, Himanshu Verma, Hong-Yi Chen, Hy (하이), hy-rice, Ibuki Kaji, Ilyas Toumlilt, Ismael Juma, Izzy Harker, J.V.S Aarathi, Jacob Montemayor, JeevanYewale, Jhen-Yung Hsu, Jian, Jiayao Sun, jimmy, Jinhe Zhang, Joanna-D, Jonah Hooper, José Armando García Sancio, Josep Prat, Jun Rao, Justine Olshan, k-apol, Kamal Chandraprakash, Ken Huang, Kevin Wu, khilesh Chaganti, Kirk True, Kuan-Po Tseng, Lan Ding, Levani Kokhreidze, Lianet Magrans, Lucas Brutschy, Lucy Liu, Luke Chen, Ma Jialong, Mahsa Seifikar, manan.gupta, Manikumar Reddy, mannoopj, Maros Orsak, Matthias J. Sax, Mickael Maison, Ming-Yen Chung, Moshe Blumberg, Murali Basani, Nandini Singhal, Nick Guo, Nick Telford, Nikita Shupletsov, Nilesh Kumar, Lan Ding, Paolo Patierno, Park Jiwon, Parker Chang, Philippus Baalman, PoAn Yang, Prabhash Kumar, Raghu Baddam, Rajarshi Misra, Rion Williams, Rion Williams,, Ritika Reddy, Robin Marechal, runom, S.Y. Wang, Saket Ranjan, Sanskar Jhajharia, Santhan3159, Sean Quah, Shashank, Shivsundar R, Siddhartha Devineni, sstremler, Steven Schlansker, Stig Døssing, Sushant Mahajan, TaiJuWu, TengYao Chi, Tirth, tison, Uladzislau Blok, Viktor Somogyi-Vass, Vincent Jiang, Vincent Potuček, Xuan-Zhang Gong, Zheguang Zhao, Zhiyan Tang, zoo-code
