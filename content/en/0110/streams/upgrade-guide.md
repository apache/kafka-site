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

If you want to upgrade from 0.10.2.x to 0.11.0 you don't need to do any code changes as the public API is fully backward compatible. However, some configuration parameters were deprecated and thus it is recommend to update your code eventually to allow for future upgrades. See below a complete list of 0.11.0 API and semantical changes that allow you to advance your application and/or simplify your code base, including the usage of new features. 

If you want to upgrade from 0.10.1.x to 0.11.0, also see the [**Upgrade Section for 0.10.2**](/0110/upgrade/#upgrade_1020_streams). It highlights incompatible changes you need to consider to upgrade your code and application. See below a complete list of 0.10.2 and 0.11.0 API and semantical changes that allow you to advance your application and/or simplify your code base, including the usage of new features. 

Upgrading from 0.10.0.x to 0.11.0.x directly is also possible. Note, that a brokers must be on version 0.10.1 or higher to run a Kafka Streams application version 0.10.1 or higher. See Streams API changes in 0.10.1, Streams API changes in 0.10.2, and Streams API changes in 0.11.0 for a complete list of API changes. Upgrading to 0.11.0.3 requires two rolling bounces with config `upgrade.from="0.10.0"` set for first upgrade phase (cf. [KIP-268](https://cwiki.apache.org/confluence/display/KAFKA/KIP-268%3A+Simplify+Kafka+Streams+Rebalance+Metadata+Upgrade)). As an alternative, an offline upgrade is also possible. 

  * prepare your application instances for a rolling bounce and make sure that config `upgrade.from` is set to `"0.10.0"` for new version 0.11.0.3 
  * bounce each instance of your application once 
  * prepare your newly deployed 0.11.0.3 application instances for a second round of rolling bounces; make sure to remove the value for config `upgrade.mode`
  * bounce each instance of your application once more to complete the upgrade 



Upgrading from 0.10.0.x to 0.11.0.0, 0.11.0.1, or 0.11.0.2 requires an offline upgrade (rolling bounce upgrade is not supported) 

  * stop all old (0.10.0.x) application instances 
  * update your code and swap old code and jar file with new code and new jar file 
  * restart all new (0.11.0.0, 0.11.0.1, or 0.11.0.2) application instances 



# Streams API changes in 0.11.0.0

Updates in `StreamsConfig`: 

  * new configuration parameter `processing.guarantee` is added 
  * configuration parameter `key.serde` was deprecated and replaced by `default.key.serde`
  * configuration parameter `value.serde` was deprecated and replaced by `default.value.serde`
  * configuration parameter `timestamp.extractor` was deprecated and replaced by `default.timestamp.extractor`
  * method `#keySerde()` was deprecated and replaced by `#defaultKeySerde()`
  * method `#valueSerde()` was deprecated and replaced by `#defaultValueSerde()`
  * new method `#defaultTimestampExtractor()` was added 



New methods in `TopologyBuilder`: 

  * added overloads for `#addSource()` that allow to define a `TimestampExtractor` per source node 
  * added overloads for `#addGlobalStore()` that allow to define a `TimestampExtractor` per source node associated with the global store 



New methods in `KStreamBuilder`: 

  * added overloads for `#stream()` that allow to define a `TimestampExtractor` per input stream 
  * added overloads for `#table()` that allow to define a `TimestampExtractor` per input table 
  * added overloads for `#globalKTable()` that allow to define a `TimestampExtractor` per global table 



Deprecated methods in `KTable`: 

  * `void foreach(final ForeachAction<? super K, ? super V> action)`
  * `void print()`
  * `void print(final String streamName)`
  * `void print(final Serde<K> keySerde, final Serde<V> valSerde)`
  * `void print(final Serde<K> keySerde, final Serde<V> valSerde, final String streamName)`
  * `void writeAsText(final String filePath)`
  * `void writeAsText(final String filePath, final String streamName)`
  * `void writeAsText(final String filePath, final Serde<K> keySerde, final Serde<V> valSerde)`
  * `void writeAsText(final String filePath, final String streamName, final Serde<K> keySerde, final Serde<V> valSerde)`



The above methods have been deprecated in favor of using the Interactive Queries API. If you want to query the current content of the state store backing the KTable, use the following approach: 

  * Make a call to `KafkaStreams.store(final String storeName, final QueryableStoreType<T> queryableStoreType)`
  * Then make a call to `ReadOnlyKeyValueStore.all()` to iterate over the keys of a `KTable`. 



If you want to view the changelog stream of the `KTable` then you could call `KTable.toStream().print()`. 

Metrics using exactly-once semantics: 

If exactly-once processing is enabled via the `processing.guarantees` parameter, internally Streams switches from a producer per thread to a producer per task runtime model. In order to distinguish the different producers, the producer's `client.id` additionally encodes the task-ID for this case. Because the producer's `client.id` is used to report JMX metrics, it might be required to update tools that receive those metrics. 

Producer's `client.id` naming schema: 

  * at-least-once (default): `[client.Id]-StreamThread-[sequence-number]`
  * exactly-once: `[client.Id]-StreamThread-[sequence-number]-[taskId]`



`[client.Id]` is either set via Streams configuration parameter `client.id` or defaults to `[application.id]-[processId]` (`[processId]` is a random UUID). 

# Notable changes in 0.10.2.1

Parameter updates in `StreamsConfig`: 

  * The default config values of embedded producer's `retries` and consumer's `max.poll.interval.ms` have been changed to improve the resiliency of a Kafka Streams application 



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



[Previous](/0110/streams/architecture) Next

  * [Documentation](/documentation)
  * [Kafka Streams API](/streams)


