---
date: 2025-09-04
title: Apache Kafka 4.1.0 Release Announcement
linkTitle: AK 4.1.0
author: Mickael Maison (@MickaelMaison)
---



We are proud to announce the release of Apache Kafka® 4.1.0. This release contains many new features and improvements. This blog post will highlight some of the more prominent ones. For a full list of changes, be sure to check the [release notes](https://downloads.apache.org/kafka/4.1.0/RELEASE_NOTES.html). 

Queues for Kafka ([KIP-932](https://cwiki.apache.org/confluence/x/4hA0Dw)) is now in preview. It's still not ready for production but you can start evaluating and testing it. See the [preview release notes](https://cwiki.apache.org/confluence/x/CIq3FQ) for more details. 

This release also introduces a new Streams Rebalance Protocol ([KIP-1071](https://cwiki.apache.org/confluence/x/2BCTEg)) in early access. It is based on the new consumer group protocol ([KIP-848](https://cwiki.apache.org/confluence/x/HhD1D)). 

See the [Upgrading to 4.1](https://kafka.apache.org/documentation.html#upgrade_4_1_0) section in the documentation for the list of notable changes and detailed upgrade steps. 

## Kafka Broker, Controller, Producer, Consumer and Admin Client

  * [KIP-877: Mechanism for plugins and connectors to register metrics](https://cwiki.apache.org/confluence/x/lY3GDQ)   
Many client-side plugins can now implement the `Monitorable` interface to easily register their own metrics. Tags identifying the plugin are automatically injected and the metrics use the `kafka.CLIENT:type=plugins` naming where CLIENT is either producer, consumer or admin. 
  * [KIP-1050: Consistent error handling for Transactions](https://cwiki.apache.org/confluence/x/8ItyEg)   
This KIP updates the error handling logic and documentation of all the transaction APIs to make it simpler to build robust applications and build third-party Kafka clients that behave the same way as the Java client. 
  * [KIP-1092: Extend Consumer#close with an option to leave the group or not](https://cwiki.apache.org/confluence/x/JQstEw)   
This adds a new `Consumer.close(CloseOptions)` method which indicates whether the consumer should explicitly leave its group when it's shutting down. This enables Streams to control when to trigger group rebalances. The `Consumer.close(Duration)` method is now deprecated. 
  * [KIP-1101: Trigger rebalance on rack topology changes](https://cwiki.apache.org/confluence/x/FouMEw)   
This KIP updates the rack-aware partition assignment from the consumer rebalance protocol and makes it a lot more memory efficient, allowing to have hundreds of members in a consumer group. 
  * [KIP-1109: Unifying Kafka Consumer Topic Metrics](https://cwiki.apache.org/confluence/x/-42MEw)   
The consumer used to replace dots in topic names by underscore it its metric names. In this release, topic metrics are also emitted with the topic names unchanged. Users should transition to these new metrics. In 5.0, the metrics with the changed topic names will be removed. 
  * [KIP-1118: Add Deadlock Protection on Producer Network Thread](https://cwiki.apache.org/confluence/x/LorREw)   
From 4.1, if `KafkaProducer.flush()` is called from the `KafkaProducer.send()` callback, then an exception is raised. Previously this could lead to a deadlock in the producer. 
  * [KIP-1139: Add support for OAuth jwt-bearer grant type](https://cwiki.apache.org/confluence/x/uIxEF)   
In addition to the client_credentials grant type, Kafka now supports the jwt-bearer grant type for OAuth. This grant type avoids putting secrets in clear in the configuration and is also supported by many OAuth providers. 
  * [KIP-1143: Deprecated Optional<String> and return String from public Endpoint#listenerName](https://cwiki.apache.org/confluence/x/LwqWF)   
This is a cleanup in the `Endpoint` class. The existing `listenerName()` method which returns `Optional<String>` is now deprecated and users should transition to the new `listenerName()` method which returns `String`. 
  * [KIP-1152: Add transactional ID pattern filter to ListTransactions API](https://cwiki.apache.org/confluence/x/4gm9F)   
When listing transactions you can now provide a pattern to filter based on the transactional ID. In environments with many transactional IDs, this avoids having to list all transactions and filter them on the client-side. 



## Kafka Streams

  * [KIP-1020: Move window.size.ms and windowed.inner.class.serde from StreamsConfig to TimeWindowedDe/Serializer and SessionWindowedDe/Serializer class](https://cwiki.apache.org/confluence/x/lAtYEQ)   
The `window.size.ms` and `windowed.inner.class.serde` configurations are now defined in TimeWindowed and SessionWindowed SerDes. 
  * [KIP-1071: Streams Rebalance Protocol](https://cwiki.apache.org/confluence/x/2BCTEg)   
This builds on KIP-848 and makes Streams task assignment a first-class citizen in the Kafka protocol. A lot of logic also moves to the coordinator such a task assignments, internal topic creations. This is currently in early access and not ready for production use. See the [upgrade guide](/documentation/streams/upgrade-guide#streams_api_changes_410) for more details. 
  * [KIP-1111: Enforcing Explicit Naming for Kafka Streams Internal Topics](https://cwiki.apache.org/confluence/x/4Y_MEw)   
Streams stores its state in internal topics whose names are generated. A new configuration, `ensure.explicit.internal.resource.naming` allows to enforce explicit naming of all internal resources to make topic names predictable and allow altering a topology and still conserve the existing topics. 



## Kafka Connect

  * [KIP-877: Mechanism for plugins and connectors to register metrics](https://cwiki.apache.org/confluence/x/lY3GDQ)   
All worker and connector plugins can now register their own metrics. For connectors and tasks this is done via their context. Other plugins can implement the `Monitorable` interface to do so. 
  * [KIP-891: Running multiple versions of Connector plugins](https://cwiki.apache.org/confluence/x/qY0ODg)   
Connect now supports installing and running multiple versions of the same connector plugins (Connectors, Converters, Transformations and Predicates). This make it easier to upgrade, and downgrade in case of issues, plugins without needing to use separate Connect clusters. 



## Summary

Ready to get started with Apache Kafka 4.1.0? Check out all the details in the [upgrade notes](https://kafka.apache.org/documentation.html#upgrade_4_1_0) and the [release notes](https://downloads.apache.org/kafka/4.1.0/RELEASE_NOTES.html), and [download](https://kafka.apache.org/downloads) Apache Kafka 4.1.0.

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 167 contributors:  
陳昱霖(Yu-Lin Chen), A. Sophie Blee-Goldman, Abhinav Dixit, Albert, Alieh Saeedi, Almog Gavra, Alyssa Huang, Andrew Schofield, Andy Li, Ao Li, Apoorv Mittal, Artem Livshits, Ayoub Omari, Azhar Ahmed, Bill Bejeck, Bolin Lin, Bruno Cadonna, Calvin Liu, Cheryl Simmons, Chia-Ping Tsai, ChickenchickenLove, Chih-Yuan Chien, Chirag Wadhwa, Chris Flood, Christo Lolov, ClarkChen, Clay Johnson, co63oc, Colin P. McCabe, Colt McNealy, Damien Gasparina, Dániel Urbán, Dave Troiano, David Arthur, David Jacot, David Mao, Dejan Stojadinović, dengziming, Dimitar Dimitrov, Divij Vaidya, DL1231, Dmitry Werner, Dongnuo Lyu, Edoardo Comar, fangxiaobing, Federico Valeri, Florian Hussonnois, Fred Zheng, Gantigmaa Selenge, Gaurav Narula, Gerard Klijs-Nefkens, Goooler, grace, Greg Harris, Guang, Guozhang Wang, Gyeongwon, Do, Hailey Ni, hgh1472, Hong-Yi Chen, Iamoshione, Ismael Juma, Istvan Toth, Janindu Pathirana, Jared Harley, Jason Taylor, Jeff Kim, Jhen-Yung Hsu, Ji-Seung Ryu, jimmy, Jimmy Wang, Jing-Jia Hung, Joao Pedro Fonseca Dantas, John Huang, John Roesler, Jonah Hooper, Jorge Esteban Quilcate Otoya, Josep Prat, José Armando García Sancio, Jun Rao, Justine Olshan, Kamal Chandraprakash, Karsten Spang, Kaushik Raina, Ken Huang, Kevin Wu, Kirk True, Kondrat Bertalan, Kuan-Po Tseng, Lan Ding, leaf-soba, Liam Miller-Cushon, Lianet Magrans, Logan Zhu, Loïc GREFFIER, Lorcan, Lucas Brutschy, lucliu1108, Luke Chen, Mahsa Seifikar, Manikumar Reddy, Manoj, Martin Sillence, Matthias J. Sax, Mehari Beyene, Mickael Maison, Milly, Ming-Yen Chung, mingdaoy, Nick Guo, Nick Telford, NICOLAS GUYOMAR, nilmadhab mondal, Okada Haruki, Omnia Ibrahim, Parker Chang, Peter Lee, Piotr P. Karwasz, PoAn Yang, Pramithas Dhakal, qingbozhang, Rajini Sivaram, Rich Chen, Ritika Reddy, Rohan, S.Y. Wang, Sanskar Jhajharia, santhoshct, Satish Duggana, Sean Quah, Sebastien Viale, Shaan, Shahbaz Aamir, ShihYuan Lin, Shivsundar R, snehashisp, Stanislav Kozlovski, Steven Schlansker, Sushant Mahajan, Swikar Patel, TaiJuWu, Ted Yan, TengYao Chi, Thomas Gebert, Thomas Thornton, Tsung-Han Ho (Miles Ho), u0184996, Uladzislau Blok, Vadym Zhytkevych, Vedarth Sharma, Vikas Singh, Viktor Somogyi-Vass, Vincent PÉRICART, Xiaobing Fang, xijiu, Xuan-Zhang Gong, yangjf2019, Yaroslav Kutsela, Yu-Syuan Jheng, YuChia Ma, Yunchi Pang, Yung, YunKui Lu, yx9o, Zachary Hamilton, Zhihong Yu 


