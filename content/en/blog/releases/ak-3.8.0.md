---
date: 2024-07-29
title: Apache Kafka 3.8.0 Release Announcement
linkTitle: AK 3.8.0
author: Josep Prat (@jlprat)
---



We are proud to announce the release of Apache Kafka 3.8.0. This release contains many new features and improvements. This blog post will highlight some of the more prominent features. For a full list of changes, be sure to check the [release notes](https://downloads.apache.org/kafka/3.8.0/RELEASE_NOTES.html).

See the [Upgrading to 3.8.0 from any version 0.8.x through 3.7.x](https://kafka.apache.org/documentation.html#upgrade_3_8_0) section in the documentation for the list of notable changes and detailed upgrade steps.

In a previous release, 3.6, [tiered storage](https://kafka.apache.org/38/documentation.html#tiered_storage) was released as early access feature. In this release, Tiered Storage now supports clusters configured with multiple log directories (i.e. JBOD feature). This feature still remains as early access. 

In the last release, 3.7, [KIP-858](https://cwiki.apache.org/confluence/display/KAFKA/KIP-858%3A+Handle+JBOD+broker+disk+failure+in+KRaft) was released in early access. Since this version, JBOD in KRaft is no longer considered an early access feature. 

Up until now, only the default compression level was used by Apache Kafka. From this version on, a configuration mechanism to specify compression level is included. See [KIP-390](https://cwiki.apache.org/confluence/display/KAFKA/KIP-390%3A+Support+Compression+Level) for more details. 

[KIP-848 The Next Generation of the Consumer Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-848%3A+The+Next+Generation+of+the+Consumer+Rebalance+Protocol) is available as preview in 3.8. This version includes numerous bug fixes and the community is encouraged to test and provide feedback. [See the preview release notes for more information.](https://cwiki.apache.org/confluence/display/KAFKA/The+Next+Generation+of+the+Consumer+Rebalance+Protocol+%28KIP-848%29+-+Preview+Release+Notes)

The configuration value `offsets.commit.required.acks` is deprecated in this version and it will be removed in Kafka 4.0. See [KIP-1041](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=303794933) for more details. 

_Note: ZooKeeper is marked as deprecated since the 3.5.0 release. ZooKeeper is planned to be removed in Apache Kafka 4.0. For more information, please see the documentation for[ZooKeeper Deprecation](https://kafka.apache.org/documentation/#zk_depr)_. 

## Kafka Broker, Controller, Producer, Consumer and Admin Client

  * **[KIP-390: Support Compression Level](https://cwiki.apache.org/confluence/display/KAFKA/KIP-390%3A+Support+Compression+Level): **  
Adds a mechanism to specify compression level instead of relying on the default one. 
  * **[KIP-719: Deprecate Log4J Appender](https://cwiki.apache.org/confluence/display/KAFKA/KIP-719%3A+Deprecate+Log4J+Appender): **  
Log4J Appender is now deprecated and it will be removed, most probably, in Kafka 4.0. 
  * **[(Preview) KIP-848 The Next Generation of the Consumer Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-848%3A+The+Next+Generation+of+the+Consumer+Rebalance+Protocol): **  
The new simplified Consumer Rebalance Protocol moves complexity away from the consumer and into the Group Coordinator within the broker and completely revamps the protocol to be incremental in nature. It provides the same guarantee as the current protocol––but better and more efficient, including no longer relying on a global synchronization barrier. [See the preview release notes for more information.](https://cwiki.apache.org/confluence/display/KAFKA/The+Next+Generation+of+the+Consumer+Rebalance+Protocol+%28KIP-848%29+-+Preview+Release+Notes)
  * **[KIP-899: Allow producer and consumer clients to rebootstrap](https://cwiki.apache.org/confluence/display/KAFKA/KIP-899%3A+Allow+producer+and+consumer+clients+to+rebootstrap): **  
This KIP allows Kafka clients to repeat the bootstrap process when updating metadata if none of the known brokers are available. 
  * **[KIP-993: Allow restricting files accessed by File and Directory ConfigProviders](https://cwiki.apache.org/confluence/display/KAFKA/KIP-993%3A+Allow+restricting+files+accessed+by+File+and+Directory+ConfigProviders): **  
This KIP adds the ability to limit the files accessible to the file and directory configuration providers so the caller doesn't have unrestricted access. 
  * **[KIP-974: Docker Image for GraalVM based Native Kafka Broker](https://cwiki.apache.org/confluence/display/KAFKA/KIP-974%3A+Docker+Image+for+GraalVM+based+Native+Kafka+Broker): **  
This update introduces the process to create Docker native image for Apache Kafka based onf GraalVM. The advantage of this Apache Kafka docker image that can launch brokers with sub-second startup time and minimal memory footprint by leveraging a GraalVM based native Kafka binary and runs in the Kraft mode. 
  * **[KIP-1018: Introduce max remote fetch timeout config for DelayedRemoteFetch requests](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1018%3A+Introduce+max+remote+fetch+timeout+config+for+DelayedRemoteFetch+requests): **  
Introduces a new timeout parameter, `remote.fetch.max.wait.ms`, to offer users the option to configure the timeout based on their workload. 
  * **[KIP-1019: Expose method to determine Metric Measurability](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1019%3A+Expose+method+to+determine+Metric+Measurability): **  
This KIP introduces a new method, `isMeasurable()`, to the `KafkaMetric` class, eliminating the need for accessing private fields or handling exceptions in case of non-measurable metrics. 
  * **[KIP-1028: Docker Official Image for Apache Kafka](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1028%3A+Docker+Official+Image+for+Apache+Kafka): **  
This update introduces the official Docker image for Apache Kafka. 
  * **[KIP-1036: Extend RecordDeserializationException exception](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1036%3A+Extend+RecordDeserializationException+exception): **  
[KIP-334](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=87297793) introduced into the Consumer the RecordDeserializationException with offsets information. That is useful to skip a poison pill but as you do not have access to the Record, it still prevents easy implementation of dead letter queue or simply logging the faulty data. 
  * **[KIP-1037: Allow WriteTxnMarkers API with Alter Cluster Permission](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1037%3A+Allow+WriteTxnMarkers+API+with+Alter+Cluster+Permission): **  
This KIP builds on [KIP-98](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging#KIP98ExactlyOnceDeliveryandTransactionalMessaging-5.2WriteTxnMarkerRequest) and [KIP-664](https://cwiki.apache.org/confluence/display/KAFKA/KIP-664%3A+Provide+tooling+to+detect+and+abort+hanging+transactions) allowing the `WriteTxnMarkers` API to be invoked with the Alter permission on the cluster to reflect that this API is an admin operation that can be called from the Kafka Admin Client. 
  * **[KIP-1041: Drop `offsets.commit.required.acks` config in 4.0 (deprecate in 3.8)](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=303794933): **  
The configuration `offsets.commit.required.acks` is deprecated and it will be removed in Kafka 4.0. 
  * **[KIP-1047 Introduce new org.apache.kafka.tools.api.Decoder to replace kafka.serializer.Decoder](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1047+Introduce+new+org.apache.kafka.tools.api.Decoder+to+replace+kafka.serializer.Decoder): **  
This KIP deprecates `kafka.serializer.Decoder` and introduces `org.apache.kafka.tools.api.Decoder` in oder to allow the migration of tool related code from core to the tools module. 



## Kafka Streams

  * **[KIP-989: Improved StateStore Iterator metrics for detecting leaks](https://cwiki.apache.org/confluence/display/KAFKA/KIP-989%3A+Improved+StateStore+Iterator+metrics+for+detecting+leaks): **  
This KIP introduces several new metrics to aid users in finding leaked Iterators, as well as identifying the cause of a high number of pinned blocks, or other kinds of memory leaks and performance problems. 
  * **[KIP-924: customizable task assignment for Streams](https://cwiki.apache.org/confluence/display/KAFKA/KIP-924%3A+customizable+task+assignment+for+Streams): **  
This KIP adds a new group of configurable interfaces for plugging custom behaviour into the Streams Partition Assignor. This configuration supplants the existing internal task assignor config. Additionally, it limits the scope of these configs to supplying a custom task assignor. This opens the door for future KIPs to add further configs in which a user can set to plug in custom behavior. 
  * **[KIP-813: Shareable State Stores](https://cwiki.apache.org/confluence/display/KAFKA/KIP-813%3A+Shareable+State+Stores): **  
This KIP adds Shareable State Stores, introducing the ability to use data within a state store across multiple applications without duplicating it on topic level. 



## Kafka Connect

  * **[KIP-477: Add PATCH method for connector config in Connect REST API](https://cwiki.apache.org/confluence/display/KAFKA/KIP-477%3A+Add+PATCH+method+for+connector+config+in+Connect+REST+API): **  
This KIP adds the ability in Kafka Connect to understand `PATCH` methods in the Connect REST API, allowing partial configuration updates. 
  * **[KIP-1004: Enforce tasks.max property in Kafka Connect](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1004%3A+Enforce+tasks.max+property+in+Kafka+Connect): **  
This KIP changes Kafka Connect so it respects the value for the `tasks.max` property. Check the KIP description page for compatibility and migration plan. 



## Summary

Ready to get started with Apache Kafka 3.8.0? Check out all the details in the [release notes](https://downloads.apache.org/kafka/3.8.0/RELEASE_NOTES.html) and [download](https://kafka.apache.org/downloads) Apache Kafka 3.8.0.

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 196 contributors:  
Aadithya Chandra, Abhijeet Kumar, Abhinav Dixit, Adrian Preston, Afshin Moazami, Ahmed Najiub, Ahmed Sobeh, Akhilesh Chaganti, Almog Gavra, Alok Thatikunta, Alyssa Huang, Anatoly Popov, Andras Katona, Andrew Schofield, Anna Sophie Blee-Goldman, Antoine Pourchet, Anton Agestam, Anton Liauchuk, Anuj Sharma, Apoorv Mittal, Arnout Engelen, Arpit Goyal, Artem Livshits, Ashwin Pankaj, Ayoub Omari, Bruno Cadonna, Calvin Liu, Cameron Redpath, charliecheng630, Cheng-Kai, Zhang, Cheryl Simmons, Chia Chuan Yu, Chia-Ping Tsai, ChickenchickenLove, Chris Egerton, Chris Holland, Christo Lolov, Christopher Webb, Colin P. McCabe, Colt McNealy, cooper.tseng@suse.com, Vedarth Sharma, Crispin Bernier, Daan Gerits, David Arthur, David Jacot, David Mao, dengziming, Divij Vaidya, DL1231, Dmitry Werner, Dongnuo Lyu, Drawxy, Dung Ha, Edoardo Comar, Eduwer Camacaro, Emanuele Sabellico, Erik van Oosten, Eugene Mitskevich, Fan Yang, Federico Valeri, Fiore Mario Vitale, flashmouse, Florin Akermann, Frederik Rouleau, Gantigmaa Selenge, Gaurav Narula, ghostspiders, gongxuanzhang, Greg Harris, Gyeongwon Do, Hailey Ni, Hao Li, Hector Geraldino, highluck, hudeqi, Hy (하이), IBeyondy, Iblis Lin, Igor Soarez, ilyazr, Ismael Juma, Ivan Vaskevych, Ivan Yurchenko, James Faulkner, Jamie Holmes, Jason Gustafson, Jeff Kim, jiangyuan, Jim Galasyn, Jinyong Choi, Joel Hamill, John Doe zh2725284321@gmail.com, John Roesler, John Yu, Johnny Hsu, Jorge Esteban Quilcate Otoya, Josep Prat, José Armando García Sancio, Jun Rao, Justine Olshan, Kalpesh Patel, Kamal Chandraprakash, Ken Huang, Kirk True, Kohei Nozaki, Krishna Agarwal, KrishVora01, Kuan-Po (Cooper) Tseng, Kvicii, Lee Dongjin, Leonardo Silva, Lianet Magrans, LiangliangSui, Linu Shibu, lixinyang, Lokesh Kumar, Loïc GREFFIER, Lucas Brutschy, Lucia Cerchie, Luke Chen, Manikumar Reddy, mannoopj, Manyanda Chitimbo, Mario Pareja, Matthew de Detrich, Matthias Berndt, Matthias J. Sax, Matthias Sax, Max Riedel, Mayank Shekhar Narula, Michael Edgar, Michael Westerby, Mickael Maison, Mike Lloyd, Minha, Jeong, Murali Basani, n.izhikov, Nick Telford, Nikhil Ramakrishnan, Nikolay, Octavian Ciubotaru, Okada Haruki, Omnia G.H Ibrahim, Ori Hoch, Owen Leung, Paolo Patierno, Philip Nee, Phuc-Hong-Tran, PoAn Yang, Proven Provenzano, Qichao Chu, Ramin Gharib, Ritika Reddy, Rittika Adhikari, Rohan, Ron Dagostino, runom, rykovsi, Sagar Rao, Said Boudjelda, sanepal, Sanskar Jhajharia, Satish Duggana, Sean Quah, Sebastian Marsching, Sebastien Viale, Sergio Troiano, Sid Yagnik, Stanislav Kozlovski, Stig Døssing, Sudesh Wasnik, TaiJuWu, TapDang, testn, TingIāu "Ting" Kì, vamossagar12, Vedarth Sharma, Victor van den Hoven, Vikas Balani, Viktor Somogyi-Vass, Vincent Rose, Walker Carlson, wernerdv, Yang Yu, Yash Mayya, yicheny, Yu-Chen Lai, yuz10, Zhifeng Chen, Zihao Lin, Ziming Deng, 谭九鼎 


