---
date: 2024-11-06
title: Apache Kafka 3.9.0 Release Announcement
linkTitle: AK 3.9.0
author: Colin P. McCabe
---



We are proud to announce the release of Apache Kafka 3.9.0. This is a major release, the final one in the 3.x line. This will also be the final major release to feature the deprecated Apache ZooKeeper mode. Starting in 4.0 and later, Kafka will always run without ZooKeeper.

## Dynamic KRaft Quorums

When in KRaft mode, Kafka relies on a Raft quorum of controller processes to store its metadata log. Previously, controller quorums were specified by a static configuration that needed to be set on all brokers and controllers. This made changing the hostnames of controllers, or adding or removing them, very difficult to do without downtime.

[KIP-853: KRaft Controller Membership Changes](https://cwiki.apache.org/confluence/display/KAFKA/KIP-853%3A+KRaft+Controller+Membership+Changes) makes quorum membership dynamic. Administrators can now add and remove controller nodes by running the **kafka-metadata-quorum.sh** tool or using the associated AdminClient API. 

This feature has been eagerly awaited by the community, and we are excited to deliver it in 3.9. The main limitation in 3.9 is that we do not support converting over static metadata quorums to dynamic ones. However, this ability is coming soon.

For more information about using the new dynamic quorums feature, see [the KIP-853 documentation.](https://kafka.apache.org/39/documentation.html#kraft_reconfig)

## Improved ZooKeeper Migration

Users that are using ZooKeeper mode today need to go through a process called ZooKeeper migration before they will be able to use KRaft mode. The migration process involves running a series of commands to copy the metadata stored in ZooKeeper into a KRaft quorum.

ZK migration is not a new feature; indeed, it has been under development since Kafka 3.4. However, I wanted to highlight that Kafka 3.9 is the final and best iteration of our ZK migration feature. As we migrated thousands of clusters (big and small), we found and fixed many bugs. We also closed all of the remaining feature gaps that kept some users tied to ZooKeeper.

Kafka 4.0 will be fully saying goodbye to ZooKeeper. There will be no support for running in ZK mode, or migrating from ZK mode. This means that administrators that are still using the deprecated ZK mode who need to upgrade to 4.0 and beyond will need to make a stop at a "bridge release." For example, if you wanted to upgrade from Kafka 3.0 to Kafka 4.0, you might do the following:

  * Upgrade to Kafka 3.9.
  * Perform ZK migration.
  * Upgrade to Kafka 4.0.



In this example, Kafka 3.9 serves as the "bridge" to 4.0

As you migrate your older Kafka clusters, also keep in mind that Kafka 3.5 and later use a version of ZooKeeper that is not wire-compatible with Kafka versions older than 2.4. Therefore, if you want to migrate a cluster older than that, you will have to make an additional stop at a release with a ZK version supported by both Kafkas. See [KIP-902](https://cwiki.apache.org/confluence/display/KAFKA/KIP-902%3A+Upgrade+Zookeeper+to+3.8.2) for details.

As an example, if you wanted to migrate from Kafka 1.0 to Kafka 4.0, you might do the following:

  * Upgrade to Kafka 3.4 (a newer version will not work due to ZK incompatibilites)
  * Upgrade to ZooKeeper 3.8
  * Upgrade to Kafka 3.9.
  * Perform ZK migration.
  * Upgrade to Kafka 4.0.



These multi-step migrations should be quite rare. Running such an old Kafka version raises security concerns, after all. However, I wanted to mention it for completeness.

## Tiered Storage

Tiered storage is a feature that has been under development since Kafka 3.6. It allows Kafka to seamlessly offload data to pluggable external storage systems, such as cloud object stores. (See [KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage) for more details.)

Tiered storage is now production-ready in Kafka 3.9. In addition, we added the following improvements:

  * **[KIP-950: Tiered Storage Disablement](https://cwiki.apache.org/confluence/display/KAFKA/KIP-950%3A++Tiered+Storage+Disablement): **  
There is now a mechanism for dynamically disabling tiered storage on a per-topic basis. 
  * **[KIP-956 Tiered Storage Quotas](https://cwiki.apache.org/confluence/display/KAFKA/KIP-956+Tiered+Storage+Quotas): **  
Administrators can now put upper bounds on tiered storage upload and download rates. 
  * **[KIP-1005: Expose EarliestLocalOffset and TieredOffset](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1005%3A+Expose+EarliestLocalOffset+and+TieredOffset): **  
Kafka now exposes the highest offset at which partition data is stored in remote storage. 
  * **[KIP-1057: Add remote log metadata flag to the dump log tool](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1057%3A+Add+remote+log+metadata+flag+to+the+dump+log+tool): **  
The kafka-dump-log.sh tool gained the ability to examine tiered storage records. 



## Kafka Streams

There are several Kafka Streams improvements in Apache Kafka 3.9.

  * **[KIP-1049: Add config log.summary.interval.ms to Kafka Streams](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1049%3A+Add+config+log.summary.interval.ms+to+Kafka+Streams): **  
Introduce the log.summary.interval.ms to control the frequency of summary logs. 
  * **[KIP-1033: Add Kafka Streams exception handler for exceptions occurring during processing](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1033%3A+Add+Kafka+Streams+exception+handler+for+exceptions+occurring+during+processing): **  
Improve exception handling in Kafka streams. 



## Kafka Connect

Kafka Connect received several improvements in 3.9 as well.

  * **[KIP-1040: Improve handling of nullable values in InsertField, ExtractField, and other transformations](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1040%3A+Improve+handling+of+nullable+values+in+InsertField%2C+ExtractField%2C+and+other+transformations): **  
Add more configuration knobs for handling nulls. 
  * **[KIP-1031: Control offset translation in MirrorSourceConnector](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1031%3A+Control+offset+translation+in+MirrorSourceConnector): **  
Add the emit.offset-syncs.enabled configuration, which can be used to disable configuration synchronization. 
  * **[KIP-1017: Health check endpoint for Kafka Connect](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1017%3A+Health+check+endpoint+for+Kafka+Connect): **  
Add a REST endpoint that can be used to determine if Kafka Connect workers are healthy. 



## Conclusion

I hope that this post has given you a sense of all the exciting things that are going on in Kafka 3.9. For more details, take a look at the [release notes](https://archive.apache.org/dist/kafka/3.9.0/RELEASE_NOTES.html), or simply [download](https://kafka.apache.org/downloads) the release for yourself. 

This was a community effort, so thank you to everyone who contributed to this release: A. Sophie Blee-Goldman, abhi-ksolves, Abhijeet Kumar, Abhinav Dixit, Adrian Preston, Alieh Saeedi, Alyssa Huang, Anatoly Popov, Andras Katona, Andrew Schofield, Andy Wilkinson, Anna Sophie Blee-Goldman, Antoine Pourchet, Apoorv Mittal, Arnav Dadarya, Arnout Engelen, Arpit Goyal, Arun Mathew, Ayoub Omari, bachmanity1, Bill Bejeck, brenden20, Bruno Cadonna, Chia Chuan Yu, Chia-Ping Tsai, ChickenchickenLove, Chirag Wadhwa, Chris Egerton, Christo Lolov, Ming-Yen Chung, Colin P. McCabe, Cy, David Arthur, David Jacot, Demonic, dengziming, Dimitar Dimitrov, Dmitry Werner, Dongnuo Lyu, dujian0068, Edoardo Comar, Farbod Ahmadian, Federico Valeri, Fiore Mario Vitale, Florin Akermann, Francois Visconte, Ganesh Sadanala, Gantigmaa Selenge, Gaurav Narula, gongxuanzhang, Greg Harris, Gyeongwon Do, Harry Fallows, Hongten, Ian McDonald, Igor Soarez, Ismael Juma, Ivan Yurchenko, Jakub Scholz, Jason Gustafson, Jeff Kim, Jim Galasyn, Jinyong Choi, Johnny Hsu, José Armando García Sancio, Josep Prat, Jun Rao, Justine Olshan, Kamal Chandraprakash, Ken Huang, Kevin Wu, Kirk True, Kondrat Bertalan, Krishna Agarwal, KrishVora01, Kuan-Po (Cooper) Tseng, Lee Dongjin, Lianet Magrans, Logan Zhu, Loïc GREFFIER, Lucas Brutschy, Luke Chen, Maciej Moscicki, Manikumar Reddy, Mason Chen, Matthias J. Sax, Max Riedel, Mickael Maison, Murali Basani, Nancy, Nicolas Guyomar, Nikolay, Okada Haruki, Omnia Ibrahim, PaulRMellor, Pavel Pozdeev, Phuc-Hong-Tran, Piotr Rzysko, PoAn Yang, Ritika Reddy, Rohan, Ron Dagostino, Sanskar Jhajharia, Satish Duggana, Sean Quah, Sebastien Viale, Shawn Hsu, ShivsundarR, Sushant Mahajan, TaiJuWu, TengYao Chi, TingIāu "Ting" Ki, vamossagar12, Vedarth Sharma, Vikas Balani, Vikas Singh, Viktor Somogyi-Vass, Vinay Agarwal, Vincent Rose, Volk, Wang Xiaoqing, Xiduo You, xijiu, Xuan-Zhang Gong, Yash Mayya, Zhengke Zhou. 


