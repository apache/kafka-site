---
title: Upgrade Guide
description: 
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Upgrade Guide & API Changes

If you want to upgrade from 0.10.1.x to 0.10.2, see the [Upgrade Section for 0.10.2](/0102/#upgrade_1020_streams). It highlights incompatible changes you need to consider to upgrade your code and application. See below a complete list of 0.10.2 API and semantical changes that allow you to advance your application and/or simplify your code base, including the usage of new features. 

If you want to upgrade from 0.10.0.x to 0.10.1, see the [Upgrade Section for 0.10.1](/0102/#upgrade_1010_streams). It highlights incompatible changes you need to consider to upgrade your code and application. See below a complete list of 0.10.1 API changes that allow you to advance your application and/or simplify your code base, including the usage of new features. 

# Notable changes in 0.10.2.1

Parameter updates in `StreamsConfig`: 

  * of particular importance to improve the resiliency of a Kafka Streams application are two changes to default parameters of producer `retries` and consumer `max.poll.interval.ms`



# Streams API changes in 0.10.2.0

New methods in `KafkaStreams`: 

  * set a listener to react on application state change via `#setStateListener(StateListener listener)`
  * retrieve the current application state via `#state()`
  * retrieve the global metrics registry via `#metrics()`
  * apply a timeout when closing an application via `#close(long timeout, TimeUnit timeUnit)`
  * specify a custom indent when retrieving Kafka Streams information via `#toString(String indent)`



Parameter updates in `StreamsConfig`: 

  * parameter `zookeeper.connect` was deprecated; a Kafka Streams application does no longer interact with Zookeeper for topic management but uses the new broker admin protocol (cf. [KIP-4, Section "Topic Admin Schema"](https://cwiki.apache.org/confluence/display/KAFKA/KIP-4+-+Command+line+and+centralized+administrative+operations#KIP-4-Commandlineandcentralizedadministrativeoperations-TopicAdminSchema.1)) 
  * added many new parameters for metrics, security, and client configurations 



Changes in `StreamsMetrics` interface: 

  * removed methods: `#addLatencySensor()`
  * added methods: `#addLatencyAndThroughputSensor()`, `#addThroughputSensor()`, `#recordThroughput()`, `#addSensor()`, `#removeSensor()`



New methods in `TopologyBuilder`: 

  * added overloads for `#addSource()` that allow to define a `auto.offset.reset` policy per source node 
  * added methods `#addGlobalStore()` to add global `StateStore`s 



New methods in `KStreamBuilder`: 

  * added overloads for `#stream()` and `#table()` that allow to define a `auto.offset.reset` policy per input stream/table 
  * added method `#globalKTable()` to create a `GlobalKTable`



New joins for `KStream`: 

  * added overloads for `#join()` to join with `KTable`
  * added overloads for `#join()` and `leftJoin()` to join with `GlobalKTable`
  * note, join semantics in 0.10.2 were improved and thus you might see different result compared to 0.10.0.x and 0.10.1.x (cf. [Kafka Streams Join Semantics](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Streams+Join+Semantics) in the Apache Kafka wiki) 


Aligned `null`-key handling for `KTable` joins: 

  * like all other KTable operations, `KTable-KTable` joins do not throw an exception on `null` key records anymore, but drop those records silently 



New window type _Session Windows_ : 

  * added class `SessionWindows` to specify session windows 
  * added overloads for `KGroupedStream` methods `#count()`, `#reduce()`, and `#aggregate()` to allow session window aggregations 



Changes to `TimestampExtractor`: 

  * method `#extract()` has a second parameter now 
  * new default timestamp extractor class `FailOnInvalidTimestamp` (it gives the same behavior as old (and removed) default extractor `ConsumerRecordTimestampExtractor`) 
  * new alternative timestamp extractor classes `LogAndSkipOnInvalidTimestamp` and `UsePreviousTimeOnInvalidTimestamps`



Relaxed type constraints of many DSL interfaces, classes, and methods (cf. [KIP-100](https://cwiki.apache.org/confluence/display/KAFKA/KIP-100+-+Relax+Type+constraints+in+Kafka+Streams+API)). 

# Streams API changes in 0.10.1.0

Stream grouping and aggregation split into two methods: 

  * old: KStream #aggregateByKey(), #reduceByKey(), and #countByKey() 
  * new: KStream#groupByKey() plus KGroupedStream #aggregate(), #reduce(), and #count() 
  * Example: stream.countByKey() changes to stream.groupByKey().count() 



Auto Repartitioning: 

  * a call to through() after a key-changing operator and before an aggregation/join is no longer required 
  * Example: stream.selectKey(...).through(...).countByKey() changes to stream.selectKey().groupByKey().count() 



TopologyBuilder: 

  * methods #sourceTopics(String applicationId) and #topicGroups(String applicationId) got simplified to #sourceTopics() and #topicGroups() 



DSL: new parameter to specify state store names: 

  * The new Interactive Queries feature requires to specify a store name for all source KTables and window aggregation result KTables (previous parameter "operator/window name" is now the storeName) 
  * KStreamBuilder#table(String topic) changes to #topic(String topic, String storeName) 
  * KTable#through(String topic) changes to #through(String topic, String storeName) 
  * KGroupedStream #aggregate(), #reduce(), and #count() require additional parameter "String storeName"
  * Example: stream.countByKey(TimeWindows.of("windowName", 1000)) changes to stream.groupByKey().count(TimeWindows.of(1000), "countStoreName") 



Windowing: 

  * Windows are not named anymore: TimeWindows.of("name", 1000) changes to TimeWindows.of(1000) (cf. DSL: new parameter to specify state store names) 
  * JoinWindows has no default size anymore: JoinWindows.of("name").within(1000) changes to JoinWindows.of(1000) 



[Previous](/0102/streams/developer-guide) Next

  * [Documentation](/documentation)
  * [Streams](/streams)


