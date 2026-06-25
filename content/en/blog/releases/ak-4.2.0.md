---
date: 2026-02-17
title: Apache Kafka 4.2.0 Release Announcement
linkTitle: AK 4.2.0
author: Christo Lolov
aliases:
  - /blog/2026/01/14/apache-kafka-4.2.0-release-announcement/
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




We are proud to announce the release of Apache Kafka® 4.2. This release contains many new features and improvements. This blog post will highlight some of the more prominent ones. For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/4.2.0/RELEASE_NOTES.html).

Kafka Queues (Share Groups) is now production-ready with new features like the RENEW acknowledgement type for extended processing times, adaptive batching for share coordinators, soft and strict enforcements of quantity of fetched records, and comprehensive lag metrics.

Kafka Streams brings the server-side rebalance protocol to GA with a limited feature set, adds dead letter queue support in exception handlers, introduces anchored wall-clock punctuation for deterministic scheduling, and gives users full control over whether to send a leave group request on closing.

This release also delivers significant improvements to consistency and observability: CLI tools now feature standardized arguments like --bootstrap-server across all tools, metric naming has been corrected to follow the kafka.COMPONENT convention, and new idle ratio metrics provide better visibility into controller and MetadataLoader performance.

Security is enhanced with a new allowlist connector client configuration override policy, while thread-safety improvements to RecordHeader eliminate concurrency risks.

Additional highlights include support for Java 25, external schema support in JsonConverter for reduced message sizes, dynamic configuration for remote log manager thread pools, adaptive batching in group coordinators, and rack ID exposure in the Admin API for consumer and share group members.

See the [Upgrading to 4.2](https://kafka.apache.org/documentation.html#upgrade_4_2_0) section in the documentation for the list of notable changes and detailed upgrade steps.

## Deprecation Notices
* [KIP-1136: Make ConsumerGroupMetadata an interface](https://cwiki.apache.org/confluence/x/r45EF)    
  Deprecates the constructors of ConsumerGroupMetadata. Marked for removal in Apache Kafka 5.0.

* [KIP-1193: Deprecate MX4j support](https://cwiki.apache.org/confluence/x/dAxJFg)    
  Adds various deprecation warnings for MX4j. Marked for removal in Apache Kafka 5.0.

* [KIP-1195: deprecate and remove org.apache.kafka.streams.errors.BrokerNotFoundException](https://cwiki.apache.org/confluence/x/8AxJFg)    
  Deprecates BrokerNotFoundException. Marked for removal in Apache Kafka 5.0.

## Kafka Broker, Controller, Producer, Consumer and Admin Client

* [KIP-932: Queues for Kafka](https://cwiki.apache.org/confluence/x/4hA0Dw)    
  Introduces share groups, a new cooperative consumption model where multiple consumers can concurrently process records from the same partitions with individual acknowledgment and delivery counting - enabling queue-like use cases without strict partition-to-consumer assignment.

* [KIP-1052: Enable warmup in producer performance test](https://cwiki.apache.org/confluence/x/iIxyEg)    
  Adds an optional `--warmup-records` argument to the producer performance test, separating startup measurements from steady-state statistics for cleaner performance analysis.

* [KIP-1100: Rename org.apache.kafka.server:type=AssignmentsManager and org.apache.kafka.storage.internals.log.RemoteStorageThreadPool metrics](https://cwiki.apache.org/confluence/x/6oqMEw)    
  Fixes inconsistent metric naming by deprecating metrics accidentally changed to `org.apache.kafka.COMPONENT` format and introducing new metrics using the correct `kafka.COMPONENT` convention.

* [KIP-1147: Improve consistency of command-line arguments](https://cwiki.apache.org/confluence/x/DguWF)    
  Standardizes command-line tool arguments by introducing consistent options like `--bootstrap-server` and `--command-config` across all tools, deprecating inconsistent legacy options.

* [KIP-1157: Enforce KafkaPrincipalSerde Implementation for KafkaPrincipalBuilder](https://cwiki.apache.org/confluence/x/1gq9F)    
  Makes `KafkaPrincipalBuilder` extend `KafkaPrincipalSerde` to enforce serialization/deserialization support at compile-time rather than failing at runtime during KRaft broker-controller communication.

* [KIP-1160: Enable returning supported features from a specific broker](https://cwiki.apache.org/confluence/x/5gnXF)    
  Adds an optional `--node-id` argument to `describeFeatures`, allowing users to query supported features from a specific node to address version inconsistencies across nodes.

* [KIP-1161: Unifying LIST-Type Configuration Validation and Default Values](https://cwiki.apache.org/confluence/x/HArXF)    
  Standardizes validation for comma-separated list configurations by rejecting null/empty values, ignoring duplicates, converting string configs to proper LIST types, and throwing ConfigExceptions during parsing rather than at runtime.

* [KIP-1172: Improve EndToEndLatency Tool with argument parser and message key/header support](https://cwiki.apache.org/confluence/x/Awu9F)    
  Improves the `EndToEndLatency` tool with robust named-argument parsing, new optional parameters for message keys and headers, and renamed arguments aligned with Kafka conventions.

* [KIP-1175: Fix the typo `PARTITIONER_ADPATIVE_PARTITIONING_ENABLE` in ProducerConfig](https://cwiki.apache.org/confluence/x/KYogFQ)    
  Fixes a misspelling by introducing the correctly spelled `PARTITIONER_ADAPTIVE_PARTITIONING_ENABLE_CONFIG` constant while deprecating the misspelled version.

* [KIP-1179: Introduce remote.log.manager.follower.thread.pool.size config](https://cwiki.apache.org/confluence/x/xAlWFQ)    
  Introduces a new dynamic configuration `remote.log.manager.follower.thread.pool.size` with proper naming conventions and dynamic configuration support for the follower partition thread pool.

* [KIP-1180: Add generic feature level metrics](https://cwiki.apache.org/confluence/x/Cwo-FQ)    
  Adds new metrics displaying finalized, minimum supported, and maximum supported feature levels for each production feature, improving visibility into upgrade/downgrade scenarios.

* [KIP-1186: Update AddRaftVoterRequest RPC to support auto-join](https://cwiki.apache.org/confluence/x/1QkBFg)    
  Adds a boolean `AckWhenCommitted` flag to `AddRaftVoterRequest` that allows immediate response after locally writing the new voter set, preventing availability issues during auto-joining controller operations.

* [KIP-1190: Add a metric for controller thread idleness](https://cwiki.apache.org/confluence/x/TApJFg)    
  Adds a new `AvgIdleRatio` metric measuring the proportion of time the controller thread spends idle versus actively processing events, improving performance visibility.

* [KIP-1192: Add include argument to ConsumerPerformance tool](https://cwiki.apache.org/confluence/x/PAxJFg)    
  Adds an `--include` argument to ConsumerPerformance for regex-based topic filtering, enabling multi-topic performance testing.

* [KIP-1197: Introduce new method to improve the TopicBasedRemoteLogMetadataManager's initialization](https://cwiki.apache.org/confluence/x/Hg9JFg)    
  Fixes TopicBasedRemoteLogMetadataManager initialization failures by introducing a `BrokerReadyCallback` interface that delays initialization until the broker is fully ready.

* [KIP-1205: Improve RecordHeader to be Thread-Safe](https://cwiki.apache.org/confluence/x/nYmhFg)    
  Addresses thread-safety issues in `RecordHeader` by implementing double-checked locking with volatile fields, eliminating `NullPointerException` risks during concurrent access with negligible overhead.

* [KIP-1206: Strict max fetch records in share fetch](https://cwiki.apache.org/confluence/x/p4mhFg)    
  Introduces a new `ShareAcquireMode` configuration for shared fetch operations, offering "batch_optimized" (soft limit) and "record_limit" (strict enforcement) modes for different processing scenarios.

* [KIP-1207: Fix anomaly of JMX metrics RequestHandlerAvgIdlePercent in kraft combined mode](https://cwiki.apache.org/confluence/x/E4qhFg)    
  Fixes the `RequestHandlerAvgIdlePercent` metric in KRaft combined mode by normalizing by combined thread count and introducing separate broker and controller metrics for per-pool visibility.

* [KIP-1217: Include push interval in ClientTelemetryReceiver context](https://cwiki.apache.org/confluence/x/6QnxFg)    
  Addresses stale client telemetry metrics by introducing new interfaces that include push interval information, enabling proper metric lifecycle management.

* [KIP-1222: Acquisition lock timeout renewal in share consumer explicit mode](https://cwiki.apache.org/confluence/x/pwkuFw)    
  Adds a new `RENEW` acknowledgement type for share consumers, allowing applications to extend acquisition lock timeouts on records requiring longer processing times.

* [KIP-1224: Adaptive append.linger.ms for the group coordinator and share coordinator](https://cwiki.apache.org/confluence/x/NopKFw)    
  Introduces adaptive batching mode for group and share coordinators that automatically adjusts batch linger times based on workload, eliminating the 5ms latency floor without manual tuning.

* [KIP-1226: Introducing Share Partition Lag Persistence and Retrieval](https://cwiki.apache.org/confluence/x/DItKFw)    
  Adds share partition lag metrics for share groups, enabling operators to monitor consumption progress, detect imbalances, and support future autoscaling capabilities.

* [KIP-1227: Expose Rack ID in MemberDescription and ShareMemberDescription](https://cwiki.apache.org/confluence/x/nwpeFw)    
  Exposes rack ID information for consumer and share group members in the Admin API by adding a `rackId` field to member description classes.

* [KIP-1228: Add Transaction Version to WriteTxnMarkersRequest](https://cwiki.apache.org/confluence/x/3gpeFw)    
  Adds a TransactionVersion field to WriteTxnMarkersRequest, enabling stricter epoch validation for Transaction Version 2 markers and strengthening exactly-once semantics guarantees.

* [KIP-1229: Add Idle Thread Ratio Metric to MetadataLoader](https://cwiki.apache.org/confluence/x/ZQteFw)    
  Adds an `AvgIdleRatio` metric to the MetadataLoader component in KRaft clusters, improving visibility into event queue processing efficiency.

## Kafka Streams

* [KIP-1034: Dead letter queue in Kafka Streams](https://cwiki.apache.org/confluence/x/HwviEQ)    
  Adds dead letter queue (DLQ) support to Kafka Streams exception handlers by introducing a new `Response` class with DLQ records, new `handleError()` methods, and raw source record bytes in error contexts.

* [KIP-1071: Streams Rebalance Protocol](https://cwiki.apache.org/confluence/x/2BCTEg)    
  Introduces a new server-side group management protocol for Kafka Streams, enabling broker-side task assignment, centralized topology metadata storage, and improved observability through dedicated RPCs and admin tools.

* [KIP-1146: Anchored punctuation](https://cwiki.apache.org/confluence/x/9QqWF)    
  Introduces anchored wall-clock punctuation for Kafka Streams by adding an optional `startTime` parameter to `schedule()`, enabling callbacks at fixed, deterministic times (e.g., exactly at the start of every hour).

* [KIP-1153: Refactor Kafka Streams CloseOptions to Fluent API Style](https://cwiki.apache.org/confluence/x/QAq9F)    
  Gives users explicit control over whether KafkaStreams sends a leave-group request on shutdown via a new `GroupMembershipOperation` enum, wrapped in a fluent-style `CloseOptions` class that replaces the deprecated boolean-based API.

* [KIP-1216: Add rebalance listener metrics for Kafka Streams](https://cwiki.apache.org/confluence/x/ywnxFg)    
  Adds thread-level latency metrics for tasks-revoked, tasks-assigned, and tasks-lost rebalance callbacks in Kafka Streams, restoring observability after the move to the dedicated streams rebalance protocol.

* [KIP-1221: Add application-id tag to Kafka Streams state metric](https://cwiki.apache.org/confluence/x/jQobFw)    
  Adds an `application-id` tag to the Kafka Streams `client-state` JMX metric, enabling operators to group multiple instances belonging to the same logical application.

* [KIP-1230: Add config for file system permissions](https://cwiki.apache.org/confluence/x/jgl3Fw)    
  Adds an opt-in `allow.os.group.write.access` configuration for Kafka Streams, allowing users to grant write access to their OS user-group for the local state directory.

## Kafka Connect

* [KIP-1054: Support external schemas in JSONConverter](https://cwiki.apache.org/confluence/x/q4tyEg)    
  Adds an optional `schema.content` configuration to JsonConverter, allowing schemas to be specified externally rather than embedded in every JSON message - reducing message size and simplifying plain JSON integration.

* [KIP-1120: AppInfo metrics don't contain the client-id](https://cwiki.apache.org/confluence/x/3gn0Ew)    
  Adds a `client-id` tag to AppInfo metrics for Kafka Worker and MirrorMaker 2 clients, improving monitoring and debugging consistency with other Kafka clients.

* [KIP-1188: New ConnectorClientConfigOverridePolicy with allowlist of configurations](https://cwiki.apache.org/confluence/x/2IkvFg)    
  Introduces a new "Allowlist" connector client configuration override policy to address security vulnerabilities, allowing administrators to explicitly specify which client configurations connectors can override.

## Summary

Ready to get started with Apache Kafka 4.2.0? Check out all the details in the [upgrade notes](https://kafka.apache.org/documentation.html#upgrade_4_2_0) and the [release notes](https://archive.apache.org/dist/kafka/4.2.0/RELEASE_NOTES.html), and [download](https://kafka.apache.org/downloads) Apache Kafka 4.2.0.

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 155 contributors:  
Abhi Tiwari, Abhijeet Kumar, Abhinav Dixit, Abhiram98, Alex, Alieh Saeedi, ally heev, Alyssa Huang, Andrew J Schofield, Anton Vasanth, Apoorv Mittal, Arpit Goyal, Artem Livshits, Bill Bejeck, Bolin Lin, Bruno Cadonna, Calvin Liu, Chang-Chi Hsu, Chang-Yu Huang, Chia-Ping Tsai, Chih-Yuan Chien, Chirag Wadhwa, Chris Egerton, Christo Lolov, Chuckame, Clemens Hutter, Colin Patrick McCabe, d00791190, Dave Troiano, David Arthur, David Jacot, Deep Golani, Dejan Stojadinović, devtrace404, Dmitry Werner, Dongnuo Lyu, Donny Nadolny, Eduwer Camacaro, Elizabeth Bennett, EME, Eric Chang, Erik Anderson, Evan Zhou, Evgeniy Kuvardin, farzan ghalami, Fatih, Federico Valeri, Gantigmaa Selenge, Gasparina Damien, Gaurav Narula, Genseric Ghiro, George Wu, Greg Harris, Harish Vishwanath, Herman Kolstad Jakobsen, Hong-Yi Chen, Ismael Juma, Izzy Harker, Jared Harley, Jhen-Yung Hsu, Jian, Jim Galasyn, Jimmy Wang, Jing-Jia Hung, Jinhe Zhang, Joel Hamill, Jonah Hooper, Josep Prat, José Armando García Sancio, Juha Mynttinen, Jun Rao, Justine Olshan, k-apol, Kamal Chandraprakash, Kaushik Raina, keemsisi, Ken Huang, Kevin Wu, Kirk True, knoxy5467, KTKTK-HZ, Kuan-Po Tseng, Lan Ding, Levani Kokhreidze, Liam Clarke-Hutchinson, Lianet Magrans, Linsiyuan9, Logan Zhu, lorcan, Lord of Abyss, Lucas Brutschy, Lucy Liu, Luke Chen, Mahsa Seifikar, majialong, Manikumar Reddy, Maros Orsak, Masahiro Mori, Mason Chen, Matt Welch, Matthias J. Sax, Michael Knox, Michael Morris, Mickael Maison, Ming-Yen Chung, NeatGuyCoding, Nick Guo, NICOLAS GUYOMAR, Nikita Shupletsov, Now, Okada Haruki, Omnia Ibrahim, Otmar Ertl, OuO, Paolo Patierno, Patrik Nagy, Pawel Szymczyk, PoAn Yang, Ken Huang, Priyanka K U, Rajani K, Rajini Sivaram, Ram, Ritika Reddy, Robert Young, Ryan Dielhenn, S.Y. Wang, samarth-ksolves, Sanskar Jhajharia, Satish Duggana, Sean Quah, Sebastien Viale, Shang-Hao Yang, Shashank, Shivsundar R, Siyang He, Sophie Blee-Goldman, Stig Døssing, stroller, Sushant Mahajan, TaiJuWu, TengYao Chi, Tsung-Han Ho (Miles Ho), Ubuntu, Uladzislau Blok, Vincent PÉRICART, Xiao Yang, xijiu, Xuan-Zhang Gong, yangxuze, Yeikel Santana, Yu-Syuan Jheng, YuChia Ma, Yunchi Pang, Yung
