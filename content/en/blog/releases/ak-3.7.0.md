---
date: 2024-02-27
title: Apache Kafka 3.7.0 Release Announcement
linkTitle: AK 3.7.0
author: Stanislav Kozlovski (@BdKozlovski)
---



We are proud to announce the release of Apache Kafka 3.7.0. This release contains many new features and improvements. This blog post will highlight some of the more prominent features. For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/3.7.0/RELEASE_NOTES.html).

See the [Upgrading to 3.7.0 from any version 0.8.x through 3.6.x](https://kafka.apache.org/documentation.html#upgrade_3_7_0) section in the documentation for the list of notable changes and detailed upgrade steps.

In the last release, 3.6, [the ability to migrate Kafka clusters from a ZooKeeper metadata system](https://kafka.apache.org/documentation/#kraft_zk_migration) to a KRaft metadata system was ready for usage in production environments with one caveat -- JBOD was not yet available for KRaft clusters. In this release, we are shipping an early access release of JBOD in KRaft. (See [KIP-858](https://cwiki.apache.org/confluence/display/KAFKA/KIP-858%3A+Handle+JBOD+broker+disk+failure+in+KRaft) and the [release notes](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+JBOD+in+KRaft+Early+Access+Release+Notes) for details). 

Additionally, client APIs released prior to Apache Kafka 2.1 are now marked deprecated in 3.7 and will be removed in Apache Kafka 4.0. See [KIP-896](https://cwiki.apache.org/confluence/display/KAFKA/KIP-896%3A+Remove+old+client+protocol+API+versions+in+Kafka+4.0) for details and RPC versions that are now deprecated. 

Java 11 support for the Kafka broker is also marked deprecated in 3.7, and is planned to be removed in Kafka 4.0. See [KIP-1013](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=284789510) for more details. Note that clients can continue to use JDK >= 11 to connect to Kafka brokers. 

_Note: ZooKeeper is marked as deprecated since the 3.5.0 release. ZooKeeper is planned to be removed in Apache Kafka 4.0. For more information, please see the documentation for[ZooKeeper Deprecation](https://kafka.apache.org/documentation/#zk_depr)_. 

## Kafka Broker, Controller, Producer, Consumer and Admin Client

  * **[(Early Access) KIP-858 Handle JBOD broker disk failure in KRaft](https://cwiki.apache.org/confluence/display/KAFKA/KIP-858%3A+Handle+JBOD+broker+disk+failure+in+KRaft): **  
This update closes the gap on one of the last major missing features in KRaft by adding JBOD support in KRaft-based clusters. Note that it is not yet recommended for use in production environments. Please refer to the [release notes](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+JBOD+in+KRaft+Early+Access+Release+Notes) to help us test it and provide feedback at [KAFKA-16061](https://issues.apache.org/jira/browse/KAFKA-16061). 
  * **[KIP-714 Client metrics and observability](https://cwiki.apache.org/confluence/display/KAFKA/KIP-714%3A+Client+metrics+and+observability): **  
With KIP-714, operators get better visibility into the clients connecting to their cluster with broker-side support of client-level metrics via a standardized telemetry interface. 
  * **[KIP-1000 List Client Metrics Configuration Resources](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1000%3A+List+Client+Metrics+Configuration+Resources): **  
KIP-1000 supports KIP-714 by introducing a way to create, read, update, and delete the client metrics configuration resources using the existing RPCs and the kafka-configs.sh tool. 
  * **[(Early Access) KIP-848 The Next Generation of the Consumer Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-848%3A+The+Next+Generation+of+the+Consumer+Rebalance+Protocol): **  
The new simplified Consumer Rebalance Protocol moves complexity away from the consumer and into the Group Coordinator within the broker and completely revamps the protocol to be incremental in nature. It provides the same guarantee as the current protocol––but better and more efficient, including no longer relying on a global synchronization barrier. [See the early access release notes for more information.](https://cwiki.apache.org/confluence/display/KAFKA/The+Next+Generation+of+the+Consumer+Rebalance+Protocol+%28KIP-848%29+-+Early+Access+Release+Notes)
  * **[KIP-951 Leader discovery optimisations for the client](https://cwiki.apache.org/confluence/display/KAFKA/KIP-951%3A+Leader+discovery+optimisations+for+the+client): **  
KIP-951 optimizes the time it takes for a client to discover the new leader of a partition, leading to reduced end-to-end latency of produce/fetch requests in the presence of leadership changes (broker restarts, partition reassignments, etc.). 
  * **[KIP-975 Docker Image for Apache Kafka](https://cwiki.apache.org/confluence/display/KAFKA/KIP-975%3A+Docker+Image+for+Apache+Kafka): **  
Introduces an official Apache Kafka Docker image, enabling quicker testing and deployment, as well as onboarding of developers. 
  * **[KIP-580 Exponential Backoff for Kafka Clients](https://cwiki.apache.org/confluence/display/KAFKA/KIP-580%3A+Exponential+Backoff+for+Kafka+Clients): **  
Changes the client’s retry backoff time used for retrying failed requests from a static one to an exponentially-increasing one. This should help reduce slow metadata convergence after broker failure due to overload. 
  * **[KIP-963 Additional metrics in Tiered Storage](https://cwiki.apache.org/confluence/display/KAFKA/KIP-963%3A+Additional+metrics+in+Tiered+Storage): **  
KIP-405 brought the early access of Tiered Storage, and with this update we’re introducing new metrics for the feature, allowing you to better monitor performance, troubleshoot, and prevent issues. 
  * **[KIP-979 Allow independently stop KRaft processes](https://cwiki.apache.org/confluence/display/KAFKA/KIP-979%3A+Allow+independently+stop+KRaft+processes): **  
Adds a way to independently stop KRaft processes in cases where operators are running in combined mode (a controller and broker in the same node). Previously, you could only stop both. The command line for stopping Kafka nodes now includes a pair of optional and mutually exclusive parameters "[--process-role]" OR "[--node-id]" to use with ./bin/kafka-server-stop.sh. 
  * **[KIP-890 Transactions Server-Side Defense](https://cwiki.apache.org/confluence/display/KAFKA/KIP-890%3A+Transactions+Server-Side+Defense): **  
Another part of this KIP shipped, this time adding transaction verification preventing hanging transactions for consumer offset partitions. 
  * **[KIP-896 Remove old client protocol API versions in Kafka 4.0](https://cwiki.apache.org/confluence/display/KAFKA/KIP-896%3A+Remove+old+client+protocol+API+versions+in+Kafka+4.0): **  
KIP-896 marks all client request versions older than Apache Kafka 2.1 as deprecated, and introduces new metrics to monitor the presence of such requests. Support for these requests will be dropped in Apache Kafka 4.0. 
  * **[KIP-919 Allow AdminClient to Talk Directly with the KRaft Controller Quorum and add Controller Registration](https://cwiki.apache.org/confluence/display/KAFKA/KIP-919%3A+Allow+AdminClient+to+Talk+Directly+with+the+KRaft+Controller+Quorum+and+add+Controller+Registration): **  
Allows the AdminClient to talk directly with the KRaft Controller Quorum, which allows us to support operations like DESCRIBE_QUORUM and INCREMENTAL_ALTER_CONFIGS to dynamically change the log4j levels on a KRaft controller. This helps with debugging scenarios where other parts of the system are down. 
  * **[KIP-978 Allow dynamic reloading of certificates with different DN / SANs](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=263429128): **  
Allows configurability to prevent checks that ensure DN (Distinguished Name) and SAN (Subject Alternative Names) are the same between old and new keystores when they’re being reload. This ultimately allows dynamic reloading of certificates that have different DN/SANs. 
  * **[KIP-1001 Add CurrentControllerId Metric](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1001%3A+Add+CurrentControllerId+Metric): **  
Adds a CurrentControllerId metric, allowing users to find the current controller by looking at the metrics of any Kafka broker/controller. 
  * **[KIP-938 Add more metrics for measuring KRaft performance](https://cwiki.apache.org/confluence/display/KAFKA/KIP-938%3A+Add+more+metrics+for+measuring+KRaft+performance): **  
We’ve added 11 new metrics for measuring KRaft-mode performance, including ActiveControllersCount, CurrentMetadataVersion and TimedOutBrokerHeartbeatCount. 
  * **[KIP-1013 Drop broker and tools support for Java 11 in Kafka 4.0 (deprecate in 3.7)](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=284789510): **  
Java 11 is now deprecated for all the server and tools modules - kafka-server-common, kafka-server, kafka_2.13, kafka-storage, kafka-metadata, kafka-group-coordinator, kafka-raft, kafka-shell, kafka-tools. It will not be supported after Kafka 4.0. All other modules (including clients, streams and connect) will continue to require Java 11 (as specified by [KIP-750](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=181308223)). 



## Kafka Streams

  * **[KIP-925 Rack aware task assignment in Kafka Streams](https://cwiki.apache.org/confluence/display/KAFKA/KIP-925%3A+Rack+aware+task+assignment+in+Kafka+Streams): **  
In part one of KIP-925, the min_traffic assignment strategy for Kafka Streams was added. Part two finishes the KIP by introducing the second rack-aware assignment strategy: balanced_subtopology. 
  * **[KIP-954 Expand default DSL store configuration to custom types](https://cwiki.apache.org/confluence/display/KAFKA/KIP-954%3A+expand+default+DSL+store+configuration+to+custom+types): **  
KIP-954 builds on KIP-591 and allows users to provide a default state store provider for their custom stores. As part of this change, a new interface has been provided along with default support for RocksDB and in-memory state stores. 
  * **[KIP-962 Relax non-null key requirement in Kafka Streams](https://cwiki.apache.org/confluence/display/KAFKA/KIP-962%3A+Relax+non-null+key+requirement+in+Kafka+Streams): **  
Kafka Streams treated records with null-keys as invalid input for joins and dropped them on the floor. KIP-962 relaxes this behavior for various left-joins and thus allows null-key records to be processed successfully. 
  * **[KIP-988 Streams Standby Update Listener](https://cwiki.apache.org/confluence/display/KAFKA/KIP-988%3A+Streams+Standby+Update+Listener): **  
Adds a new interface for handling cases where standby tasks have their a) state stores registered, b) load a batch of records and c) stop updates. 
  * **[KIP-960](https://cwiki.apache.org/confluence/display/KAFKA/KIP-960%3A+Support+single-key_single-timestamp+interactive+queries+%28IQv2%29+for+versioned+state+stores) / [KIP-968](https://cwiki.apache.org/confluence/display/KAFKA/KIP-968%3A+Support+single-key_multi-timestamp+interactive+queries+%28IQv2%29+for+versioned+state+stores) IQ support for Versioned State Stores: **  
Version state stores were added in Apache Kafka 3.5 release (KIP-889), but it was not possible so far to query the new stores. KIP-960 and KIP-968 close this gap by adding new query types for IQv2 namely VersionedKeyQuery and MultiVersionedKeyQuery, respectively. Both queries allow you to do lookups for a single key, to ask for the most recent value, a historic value, or a range of historic values for the provided key. 
  * **[KIP-985 Add reverseRange and reverseAll query over kv-store in IQv2](https://cwiki.apache.org/confluence/display/KAFKA/KIP-985%3A+Add+reverseRange+and+reverseAll+query+over+kv-store+in+IQv2): **  
IQv2 supports RangeQueries which allow you to query for a range of keys. However, the API did not provide any guarantee about the ordering of the returned result. With KIP-985 it’s now possible to request the result to be ordered (per partition) in either ascending or descending order, or leave the order unspecified. 
  * **[KIP-992 Introduce IQv2 Query Types: TimestampedKeyQuery and TimestampedRangeQuery](https://cwiki.apache.org/confluence/display/KAFKA/KIP-992%3A+Proposal+to+introduce+IQv2+Query+Types%3A+TimestampedKeyQuery+and+TimestampedRangeQuery): **  
Finally, KIP-992 adds new timestamped-key and timestamped-range interactive queries for timestamped key-value state stores. This change improves the type safety of the IQv2 API. The existing RangeQuery now always returns only the value if issued against a timestamped key-value store. 



## Kafka Connect

  * **[KIP-976 Cluster-wide dynamic log adjustment for Kafka Connect](https://cwiki.apache.org/confluence/display/KAFKA/KIP-976%3A+Cluster-wide+dynamic+log+adjustment+for+Kafka+Connect): **  
KIP-495 introduced the ability for users to dynamically change the log level of individual workers in their connect cluster. To address situations when it is not possible to target an individual worker, KIP-976 allows for dynamic log-level changes to be broadcast to all workers across the cluster in a single update. 
  * **[KIP-980 Allow creating connectors in a stopped state](https://cwiki.apache.org/confluence/display/KAFKA/KIP-980%3A+Allow+creating+connectors+in+a+stopped+state): **  
This update allows users to create new Connectors in a STOPPED or PAUSED state, enabling use cases like migrating connectors. There is now a new optional "initial_state" field during connector creation. 
  * **[KIP-959 Add BooleanConverter to Kafka Connect](https://cwiki.apache.org/confluence/display/KAFKA/KIP-959%3A+Add+BooleanConverter+to+Kafka+Connect): **  
KIP-959 adds a BooleanConverter to Connect, supporting serializing and deserializing the boolean primitive in a Kafka Connect schema. This implements both org.apache.kafka.connect.storage.Converter and org.apache.kafka.connect.storage.HeaderConverter. 
  * **[KIP-970 Deprecate and remove Connect's redundant task configurations endpoint](https://cwiki.apache.org/confluence/display/KAFKA/KIP-970%3A+Deprecate+and+remove+Connect%27s+redundant+task+configurations+endpoint): **  
Deprecates a redundant endpoint for fetching task configurations, eventually to be removed in Apache Kafka 4.0. 



## Summary

Ready to get started with Apache Kafka 3.7.0? Check out all the details in the [release notes](https://archive.apache.org/dist/kafka/3.7.0/RELEASE_NOTES.html) and [download](https://kafka.apache.org/downloads) Apache Kafka 3.7.0.

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 146 contributors:   
Abhijeet Kumar, Akhilesh Chaganti, Alieh, Alieh Saeedi, Almog Gavra, Alok Thatikunta, Alyssa Huang, Aman Singh, Andras Katona, Andrew Schofield, Anna Sophie Blee-Goldman, Anton Agestam, Apoorv Mittal, Arnout Engelen, Arpit Goyal, Artem Livshits, Ashwin Pankaj, ashwinpankaj, atu-sharm, bachmanity1, Bob Barrett, Bruno Cadonna, Calvin Liu, Cerchie, chern, Chris Egerton, Christo Lolov, Colin Patrick McCabe, Colt McNealy, Crispin Bernier, David Arthur, David Jacot, David Mao, Deqi Hu, Dimitar Dimitrov, Divij Vaidya, Dongnuo Lyu, Eaugene Thomas, Eduwer Camacaro, Eike Thaden, Federico Valeri, Florin Akermann, Gantigmaa Selenge, Gaurav Narula, gongzhongqiang, Greg Harris, Guozhang Wang, Gyeongwon, Do, Hailey Ni, Hanyu Zheng, Hao Li, Hector Geraldino, hudeqi, Ian McDonald, Iblis Lin, Igor Soarez, iit2009060, Ismael Juma, Jakub Scholz, James Cheng, Jason Gustafson, Jay Wang, Jeff Kim, Jim Galasyn, John Roesler, Jorge Esteban Quilcate Otoya, Josep Prat, José Armando García Sancio, Jotaniya Jeel, Jouni Tenhunen, Jun Rao, Justine Olshan, Kamal Chandraprakash, Kirk True, kpatelatwork, kumarpritam863, Laglangyue, Levani Kokhreidze, Lianet Magrans, Liu Zeyu, Lucas Brutschy, Lucia Cerchie, Luke Chen, maniekes, Manikumar Reddy, mannoopj, Maros Orsak, Matthew de Detrich, Matthias J. Sax, Max Riedel, Mayank Shekhar Narula, Mehari Beyene, Michael Westerby, Mickael Maison, Nick Telford, Nikhil Ramakrishnan, Nikolay, Okada Haruki, olalamichelle, Omnia G.H Ibrahim, Owen Leung, Paolo Patierno, Philip Nee, Phuc-Hong-Tran, Proven Provenzano, Purshotam Chauhan, Qichao Chu, Matthias J. Sax, Rajini Sivaram, Renaldo Baur Filho, Ritika Reddy, Robert Wagner, Rohan, Ron Dagostino, Roon, runom, Ruslan Krivoshein, rykovsi, Sagar Rao, Said Boudjelda, Satish Duggana, shuoer86, Stanislav Kozlovski, Taher Ghaleb, Tang Yunzi, TapDang, Taras Ledkov, tkuramoto33, Tyler Bertrand, vamossagar12, Vedarth Sharma, Viktor Somogyi-Vass, Vincent Jiang, Walker Carlson, Wuzhengyu97, Xavier Léauté, Xiaobing Fang, yangy0000, Ritika Reddy, Yanming Zhou, Yash Mayya, yuyli, zhaohaidao, Zihao Lin, Ziming Deng 


