---
date: 2023-10-10
title: Apache Kafka 3.6.0 Release Announcement
linkTitle: AK 3.6.0
author: Satish Duggana (@SatishDuggana)
---



We are proud to announce the release of Apache Kafka 3.6.0. This release contains many new features and improvements. This blog post will highlight some of the more prominent features. For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/3.6.0/RELEASE_NOTES.html).

See the [Upgrading to 3.6.0 from any version 0.8.x through 3.5.x](https://kafka.apache.org/36/documentation.html#upgrade_3_6_0) section in the documentation for the list of notable changes and detailed upgrade steps.

The 3.6.0 release marked the first production ready release for the migration of Kafka clusters from a ZooKeeper metadata system to a KRaft metadata system. Users wanting to perform this migration are advised to first upgrade to 3.6.2 or 3.7.1 to receive important bug fixes. 

See the ZooKeeper to KRaft migration [operations documentation](https://kafka.apache.org/documentation/#kraft_zk_migration) for details. Note that support for JBOD is still not available for KRaft clusters, therefore clusters utilizing JBOD can not be migrated. See [KIP-858](https://cwiki.apache.org/confluence/display/KAFKA/KIP-858%3A+Handle+JBOD+broker+disk+failure+in+KRaft) for details regarding KRaft and JBOD. 

Support for Delegation Tokens in KRaft ([KAFKA-15219](https://issues.apache.org/jira/browse/KAFKA-15219)) was completed in 3.6, further reducing the gap of features between ZooKeeper-based Kafka clusters and KRaft. Migration of delegation tokens from ZooKeeper to KRaft is also included in 3.6.

[Tiered Storage](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage) is an early access feature. It is currently only suitable for testing in non production environments. See the [Early Access Release Notes](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Tiered+Storage+Early+Access+Release+Notes) for more details.

_Note: ZooKeeper is marked as deprecated since 3.5.0 release. ZooKeeper is planned to be removed in Apache Kafka 4.0. For more information, please see the documentation for[ZooKeeper Deprecation](/documentation#zk_depr)_

## Kafka Broker, Controller, Producer, Consumer and Admin Client

  * **[KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage): Kafka Tiered Storage (Early Access): **  
Introduces Tiered Storage to Kafka. Note that this is an early access feature only advised for use in non-production environments (see the [early access notes](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Tiered+Storage+Early+Access+Release+Notes) for more information). This feature provides a separation of computation and storage in the broker for pluggable storage tiering natively in Kafka Tiered Storage brings a seamless extension of storage to remote objects with minimal operational changes. 
  * **[KIP-890](https://cwiki.apache.org/confluence/display/KAFKA/KIP-890%3A+Transactions+Server-Side+Defense): Transactions Server Side Defense (Part 1): **  
Hanging transactions can negatively impact your read committed consumers and prevent compacted logs from being compacted. KIP-890 helps address hanging transactions by verifying partition additions. Part 2 of KIP-890 will optimize verification, which currently adds an extra hop.  
In 3.6.0, transaction verification will prevent hanging transactions on data partitions. In the next release, transactional offset commits will also be covered. 
  * **[KIP-797](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=195726330): Accept duplicate listener on port for IPv4/IPv6: **  
Until now, Kafka has not supported duplicate listeners on the same port. This works when using only a single IP stack, but presents an issue if you are working with both IPv4 and IPv6. With KIP-797, brokers can be configured with listeners that have the same port on different IP stacks. This update does not affect advertised listeners, which already have this feature. 
  * **[KIP-863](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=225152035): Reduce CompletedFetch#parseRecord() memory copy: **  
Reduces memory allocation and improves memory performance during record deserialization by using a ByteBuffer instead of byte[] for deserialization, which improves efficiency. Updated public interfaces include the Deserializer class, ByteBufferDeserializer class, and StringDeserializer class. 
  * **[KIP-868](https://cwiki.apache.org/confluence/display/KAFKA/KIP-868+Metadata+Transactions): Metadata Transactions: **  
Improves the overall durability of the KRaft layer by adding metadata transactions that consist of: 
    * BeginTransaction
    * Number of records
    * EndTransaction or AbortTransaction
KRaft uses record batches as a mechanism for atomicity. Typically, there was a limit to the fetch size on the Raft consensus layer, and the controller could generate a set of atomic records that exceeded this limit. This update introduces marker records that allow larger sets of atomic records to be sent to the Raft consensus layer in multiple batches. This bypasses the fetch limit. 
  * **[KIP-902](https://cwiki.apache.org/confluence/display/KAFKA/KIP-902%3A+Upgrade+Zookeeper+to+3.8.2): Upgrade Zookeeper to 3.8.2:**  
This upgrades the ZooKeeper version that is bundled with Kafka to version 3.8.2. The new version includes several updates and security improvements. 
  * **[KIP-917](https://cwiki.apache.org/confluence/display/KAFKA/KIP-917%3A+Additional+custom+metadata+for+remote+log+segment): Additional custom metadata for remote log segment:**  
It introduces having an optional custom metadata as part of remote log segment metadata. RemoteStorageManager returns the optional custom metadata when copyLogSegmentData() is invoked. It will be passed along with remote log segment metadata. 
  * **[KIP-937](https://cwiki.apache.org/confluence/display/KAFKA/KIP-937%3A+Improve+Message+Timestamp+Validation): Improve Message Timestamp Validation: **  
It improves data integrity and prevents potential pitfalls caused by inaccurate timestamp handling by adding more validation logic for message timestamps. While past timestamps are a normal occurrence in Kafka, future timestamps might represent an incorrectly formatted integer. KIP-937 rejects messages with future timestamps and provides a descriptive exemption. 
  * **[KIP-938](https://cwiki.apache.org/confluence/display/KAFKA/KIP-938%3A+Add+more+metrics+for+measuring+KRaft+performance): Add more metrics for measuring KRaft performance: **  
Adds new controller, loader, and snapshot emitter KRaft performance metrics. 



## Kafka Streams

  * **[KIP-923](https://cwiki.apache.org/confluence/display/KAFKA/KIP-923%3A+Add+A+Grace+Period+to+Stream+Table+Join): Add A Grace Period to Stream Table Join: **  
Adds a grace period to stream-table joins to improve table-side out-of-order data handling. The joined object has a new method called "withGracePeriod" that will cause the table side lookup to only happen after the grace period has passed.
  * **[KIP-941](https://cwiki.apache.org/confluence/display/KAFKA/KIP-941%3A+Range+queries+to+accept+null+lower+and+upper+bounds): Range queries to accept null lower and upper bounds:**  
Previously, RangeQuery did not support null to specify “no upper/lower bound”. KIP-941 allows users to pass null into withRange(...) for lower/upper bounds to specify a full or half-open range: 
    * `withRange(null, null)` == `withNoBounds()`
    * `withRange(lower, null)` == `withLowerBound(lower)`
    * `withRange(null, upper)` == `withUpperBound(upper)`



## Kafka Connect

  * **[KIP-793](https://cwiki.apache.org/confluence/display/KAFKA/KIP-793%3A+Allow+sink+connectors+to+be+used+with+topic-mutating+SMTs): Allow sink connectors to be used with topic-mutating SMTs: **  
Adds support for topic-mutating SMTs for async sink connectors. This is to address an incompatibility between sink connectors overriding the SinkTask::preCommit method and SMTs that mutate the topic field of a SinkRecord .
  * **[KIP-875](https://cwiki.apache.org/confluence/display/KAFKA/KIP-875%3A+First-class+offsets+support+in+Kafka+Connect): First-class offsets support in Kafka Connect: **  
Provides first-class admin support for offsets in Kafka Connect. KIP-875 Part 1 added endpoints to get offsets and a new STOPPED state for connectors. The alter offsets and reset offsets endpoints have now been added.  Action | Description  
---|---  
GET /connectors/{connector}/offsets | Retrieve the offsets for a connector; the connector must exist  
PATCH /connectors/{connector}/offsets | Alter the offsets for a connector; the connector must exist, and must be in the STOPPED state   
DELETE /connectors/{connector}/offsets | Reset the offsets for a connector; the connector must exist, and must be in the STOPPED state   
PUT /connectors/{connector}/pause | Pause the connector; the connector must exist  
  * **[KIP-898](https://cwiki.apache.org/confluence/display/KAFKA/KIP-898%3A+Modernize+Connect+plugin+discovery): Modernize Connect plugin discovery: **  
With KIP-898, Connect workers can now read from ServiceLoader manifests and module info directly during startup for more efficient plugin class discovery. Note that this update allows connector developers to add service declarations to their plugins.



## Summary

Ready to get started with Apache Kafka 3.6.0? Check out all the details in the [release notes](https://archive.apache.org/dist/kafka/3.6.0/RELEASE_NOTES.html) and [download](https://kafka.apache.org/downloads) Apache Kafka 3.6.0.

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 139 contributors:   
A. Sophie Blee-Goldman, Aaron Ai, Abhijeet Kumar, aindriu-aiven, Akhilesh Chaganti, Alexandre Dupriez, Alexandre Garnier, Alok Thatikunta, Alyssa Huang, Aman Singh, Andras Katona, Andrew Schofield, Andrew Grant, Aneel Kumar, Anton Agestam, Artem Livshits, atu-sharm, bachmanity1, Bill Bejeck, Bo Gao, Bruno Cadonna, Calvin Liu, Chaitanya Mukka, Chase Thomas, Cheryl Simmons, Chia-Ping Tsai, Chris Egerton, Christo Lolov, Clay Johnson, Colin P. McCabe, Colt McNealy, d00791190, Damon Xie, Danica Fine, Daniel Scanteianu, Daniel Urban, David Arthur, David Jacot, David Mao, dengziming, Deqi Hu, Dimitar Dimitrov, Divij Vaidya, DL1231, Dániel Urbán, Erik van Oosten, ezio, Farooq Qaiser, Federico Valeri, flashmouse, Florin Akermann, Gabriel Oliveira, Gantigmaa Selenge, Gaurav Narula, GeunJae Jeon, Greg Harris, Guozhang Wang, Hailey Ni, Hao Li, Hector Geraldino, hudeqi, hzh0425, Iblis Lin, iit2009060, Ismael Juma, Ivan Yurchenko, James Shaw, Jason Gustafson, Jeff Kim, Jim Galasyn, John Roesler, Joobi S B, Jorge Esteban Quilcate Otoya, Josep Prat, Joseph (Ting-Chou) Lin, José Armando García Sancio, Jun Rao, Justine Olshan, Kamal Chandraprakash, Keith Wall, Kirk True, Lianet Magrans, LinShunKang, Liu Zeyu, lixy, Lucas Bradstreet, Lucas Brutschy, Lucent-Wong, Lucia Cerchie, Luke Chen, Manikumar Reddy, Manyanda Chitimbo, Maros Orsak, Matthew de Detrich, Matthias J. Sax, maulin-vasavada, Max Riedel, Mehari Beyene, Michal Cabak (@miccab), Mickael Maison, Milind Mantri, minjian.cai, mojh7, Nikolay, Okada Haruki, Omnia G H Ibrahim, Owen Leung, Philip Nee, prasanthV, Proven Provenzano, Purshotam Chauhan, Qichao Chu, Rajini Sivaram, Randall Hauch, Renaldo Baur Filho, Ritika Reddy, Rittika Adhikari, Rohan, Ron Dagostino, Sagar Rao, Said Boudjelda, Sambhav Jain, Satish Duggana, sciclon2, Shekhar Rajak, Sungyun Hur, Sushant Mahajan, Tanay Karmarkar, tison, Tom Bentley, vamossagar12, Victoria Xia, Vincent Jiang, vveicc, Walker Carlson, Yash Mayya, Yi-Sheng Lien, Ziming Deng, 蓝士钦 


