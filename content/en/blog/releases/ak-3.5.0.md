---
date: 2023-06-15
title: Apache Kafka 3.5.0 Release Announcement
linkTitle: AK 3.5.0
author: Mickael Maison (@MickaelMaison)
---



We are proud to announce the release of Apache Kafka 3.5.0. This release contains many new features and improvements. This blog post will highlight some of the more prominent features. For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/3.5.0/RELEASE_NOTES.html).

See the [Upgrading to 3.5.0 from any version 0.8.x through 3.4.x](https://kafka.apache.org/35/documentation.html#upgrade_3_5_0) section in the documentation for the list of notable changes and detailed upgrade steps.

The ability to migrate Kafka clusters from ZK to KRaft mode with no downtime is still an early access feature. It is currently only suitable for testing in non production environments. See [KIP-866](https://cwiki.apache.org/confluence/display/KAFKA/KIP-866+ZooKeeper+to+KRaft+Migration) for more details.

_Note: ZooKeeper is now marked deprecated in this release. ZooKeeper is planned to be removed in Apache Kafka 4.0. (Cf[ZooKeeper Deprecation](/documentation#zk_depr))_

## Kafka Broker, Controller, Producer, Consumer and Admin Client

  * **KIP-881: Rack-aware Partition Assignment for Kafka Consumers** : Kafka 3.4.0 only contained the protocol changes for [KIP-881](https://cwiki.apache.org/confluence/display/KAFKA/KIP-881%3A+Rack-aware+Partition+Assignment+for+Kafka+Consumers). The built-in assignors have now been updated to support rack-awareness.
  * **KIP-887: Add ConfigProvider to make use of environment variables** : [KIP-887](https://cwiki.apache.org/confluence/display/KAFKA/KIP-887%3A+Add+ConfigProvider+to+make+use+of+environment+variables) introduces a new `[ConfigProvider](https://kafka.apache.org/35/javadoc/org/apache/kafka/common/config/provider/ConfigProvider.html)` implementation, `EnvVarConfigProvider`, to retrieve configurations from environment variables.
  * **KIP-900: KRaft kafka-storage.sh API additions to support SCRAM for Kafka Brokers** : [KIP-900](https://cwiki.apache.org/confluence/display/KAFKA/KIP-900%3A+KRaft+kafka-storage.sh+API+additions+to+support+SCRAM+for+Kafka+Brokers) updates the `kafka-storage` tool and adds a mechanism to configure SCRAM for inter broker authentication with KRaft.
  * **KIP-903: Replicas with stale broker epoch should not be allowed to join the ISR:** [KIP-903](https://cwiki.apache.org/confluence/display/KAFKA/KIP-903%3A+Replicas+with+stale+broker+epoch+should+not+be+allowed+to+join+the+ISR) addresses a limitation of the inter broker replication protocol which could lead to data loss in case of a broker failing while another broker had an unclean shutdown.



## Kafka Streams

  * **KIP-399: Extend ProductionExceptionHandler to cover serialization exceptions** : [KIP-399](https://cwiki.apache.org/confluence/display/KAFKA/KIP-399%3A+Extend+ProductionExceptionHandler+to+cover+serialization+exceptions) adds a method, `handleSerializationException()`, to the `ProductionExceptionHandler` interface to handle any serialization errors encountered while producing records.
  * **KIP-889: Versioned State Stores** : [KIP-889](https://cwiki.apache.org/confluence/display/KAFKA/KIP-889%3A+Versioned+State+Stores) introduces versioned state stores to improve the accuracy of joins when out of order records are processed.
  * **KIP-907: Add Boolean Serde to public interface** : Kafka Streams includes built-in Serdes for most primitive types. [KIP-907](https://cwiki.apache.org/confluence/display/KAFKA/KIP-907%3A+Add+Boolean+Serde+to+public+interface) adds a new one for booleans.



## Kafka Connect

  * **KIP-710: Full support for distributed mode in dedicated MirrorMaker 2.0 clusters** : [KIP-710](https://cwiki.apache.org/confluence/display/KAFKA/KIP-710%3A+Full+support+for+distributed+mode+in+dedicated+MirrorMaker+2.0+clusters) improves the dedicated mode of MirrorMaker. It now supports running multiple instances and handling automatic reconfigurations.
  * **KIP-875: First-class offsets support in Kafka Connect** : [KIP-875](https://cwiki.apache.org/confluence/display/KAFKA/KIP-875%3A+First-class+offsets+support+in+Kafka+Connect) adds REST API endpoints for managing offset of Connectors. 3.5.0 only contains endpoints for listing offsets. Endpoints for updating and deleting offsets will come in a future release.
  * **KIP-894: Use incrementalAlterConfig for syncing topic configurations** : With [KIP-894](https://cwiki.apache.org/confluence/display/KAFKA/KIP-894%3A+Use+incrementalAlterConfigs+API+for+syncing+topic+configurations), MirrorMaker can use the `IncrementalAlterConfig` API when mirroring topic configuration between clusters.
  * **KAFKA-14021: MirrorMaker 2 should implement KIP-618 APIs** : [KAFKA-14021](https://issues.apache.org/jira/browse/KAFKA-14021) adds support for exactly-once semantics to MirrorSourceConnector.



## Summary

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 103 authors: A. Sophie Blee-Goldman, Akhilesh Chaganti, Alex Sorokoumov, Alexandre Dupriez, Alyssa Huang, Anastasia Vela, Andreas Maechler, andymg3, Artem Livshits, atu-sharm, bachmanity1, Bill Bejeck, Brendan Ribera, Calvin Liu, Chaitanya Mukka, Cheryl Simmons, Chia-Ping Tsai, Chris Egerton, Christo Lolov, Colin P. McCabe, csolidum, Daniel Scanteianu, David Arthur, David Jacot, David Karlsson, David Mao, Dejan Stojadinović, Divij Vaidya, dorwi, drgnchan, Dániel Urbán, Edoardo Comar, egyedt, emilnkrastev, Eric Haag, Farooq Qaiser, Federico Valeri, Gantigmaa Selenge, Greg Harris, Guozhang Wang, Hao Li, Hector Geraldino, Himani Arora, Hoki Min, hudeqi, iamazy, Iblis Lin, Ismael Juma, Ivan Yurchenko, Jakub Scholz, Jason Gustafson, Jeff Kim, Jim Galasyn, Jorge Esteban Quilcate Otoya, Josep Prat, José Armando García Sancio, Juan José Ramos, Junyang Liu, Justine Olshan, Kamal Chandraprakash, Kirk True, Kowshik Prakasam, littlehorse-eng, liuzc9, Lucas Brutschy, Lucia Cerchie, Luke Chen, Manikumar Reddy, Manyanda Chitimbo, Matthew Wong, Matthias J. Sax, Matthias Seiler, Michael Marshall, Mickael Maison, nicolasguyomar, Nikolay, Paolo Patierno, Philip Nee, Pierangelo Di Pilato, Proven Provenzano, Purshotam Chauhan, Qing, Rajini Sivaram, RivenSun, Robert Young, Rohan, Roman Schmitz, Ron Dagostino, Ruslan Krivoshein, Satish Duggana, Shay Elkin, Shekhar Rajak, Simon Woodman, Spacrocket, stejani-cflt, Terry, Tom Bentley, vamossagar12, Victoria Xia, Viktor Somogyi-Vass, Vladimir Korenev, Yash Mayya, Zheng-Xian Li 

