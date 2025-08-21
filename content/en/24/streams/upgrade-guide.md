---
title: Upgrade Guide
description: 
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Upgrade Guide and API Changes

[Introduction](/24/streams/) [Run Demo App](/24/streams/quickstart) [Tutorial: Write App](/24/streams/tutorial) [Concepts](/24/streams/core-concepts) [Architecture](/24/streams/architecture) [Developer Guide](/24/streams/developer-guide/) [Upgrade](/24/streams/upgrade-guide)

Upgrading from any older version to 2.4.1 is possible: you will need to do two rolling bounces, where during the first rolling bounce phase you set the config `upgrade.from="older version"` (possible values are `"0.10.0" - "2.3"`) and during the second you remove it. This is required to safely upgrade to the new cooperative rebalancing protocol of the embedded consumer. Note that you will remain using the old eager rebalancing protocol if you skip or delay the second rolling bounce, but you can safely switch over to cooperative at any time once the entire group is on 2.4+ by removing the config value and bouncing. For more details please refer to [KIP-429](https://cwiki.apache.org/confluence/x/vAclBg): 

  * prepare your application instances for a rolling bounce and make sure that config `upgrade.from` is set to the version from which it is being upgrade.
  * bounce each instance of your application once 
  * prepare your newly deployed 2.4.1 application instances for a second round of rolling bounces; make sure to remove the value for config `upgrade.mode`
  * bounce each instance of your application once more to complete the upgrade 



As an alternative, an offline upgrade is also possible. Upgrading from any versions as old as 0.10.0.x to 2.4.1 in offline mode require the following steps: 

  * stop all old (e.g., 0.10.0.x) application instances 
  * update your code and swap old code and jar file with new code and new jar file 
  * restart all new (2.4.1) application instances 



To run a Kafka Streams application version 2.2.1, 2.3.0, or higher a broker version 0.11.0 or higher is required and the on-disk message format must be 0.11 or higher. Brokers must be on version 0.10.1 or higher to run a Kafka Streams application version 0.10.1 to 2.2.0. Additionally, on-disk message format must be 0.10 or higher to run a Kafka Streams application version 1.0 to 2.2.0. For Kafka Streams 0.10.0, broker version 0.10.0 or higher is required. 

Since 2.2.0 release, Kafka Streams depends on a RocksDBs version that requires MacOS 10.13 or higher.

Another important thing to keep in mind: in deprecated `KStreamBuilder` class, when a `KTable` is created from a source topic via `KStreamBuilder.table()`, its materialized state store will reuse the source topic as its changelog topic for restoring, and will disable logging to avoid appending new updates to the source topic; in the `StreamsBuilder` class introduced in 1.0, this behavior was changed accidentally: we still reuse the source topic as the changelog topic for restoring, but will also create a separate changelog topic to append the update records from source topic to. In the 2.0 release, we have fixed this issue and now users can choose whether or not to reuse the source topic based on the `StreamsConfig#TOPOLOGY_OPTIMIZATION`: if you are upgrading from the old `KStreamBuilder` class and hence you need to change your code to use the new `StreamsBuilder`, you should set this config value to `StreamsConfig#OPTIMIZE` to continue reusing the source topic; if you are upgrading from 1.0 or 1.1 where you are already using `StreamsBuilder` and hence have already created a separate changelog topic, you should set this config value to `StreamsConfig#NO_OPTIMIZATION` when upgrading to 2.4.1 in order to use that changelog topic for restoring the state store. More details about the new config `StreamsConfig#TOPOLOGY_OPTIMIZATION` can be found in [KIP-295](https://cwiki.apache.org/confluence/display/KAFKA/KIP-295%3A+Add+Streams+Configuration+Allowing+for+Optional+Topology+Optimization). 

# Streams API changes in 2.4.0

As of 2.4.0 Kafka Streams offers a KTable-KTable foreign-key join (as per [KIP-213](https://cwiki.apache.org/confluence/display/KAFKA/KIP-213+Support+non-key+joining+in+KTable)). This joiner allows for records to be joined between two KTables with different keys. Both [INNER and LEFT foreign-key joins](/24/streams/developer-guide/dsl-api.html#ktable-ktable-fk-join) are supported. 

In the 2.4 release, you now can name all operators in a Kafka Streams DSL topology via [KIP-307](https://cwiki.apache.org/confluence/display/KAFKA/KIP-307%3A+Allow+to+define+custom+processor+names+with+KStreams+DSL). Giving your operators meaningful names makes it easier to understand the topology description (`Topology#describe()#toString()`) and understand the full context of what your Kafka Streams application is doing.   
There are new overloads on most `KStream` and `KTable` methods that accept a `Named` object. Typically you'll provide a name for the DSL operation by using `Named.as("my operator name")`. Naming of repartition topics for aggregation operations will still use `Grouped` and join operations will use either `Joined` or the new `StreamJoined` object. 

Before the 2.4.0 version of Kafka Streams, users of the DSL could not name the state stores involved in a stream-stream join. If users changed their topology and added a operator before the join, the internal names of the state stores would shift, requiring an application reset when redeploying. In the 2.4.0 release, Kafka Streams adds the `StreamJoined` class, which gives users the ability to name the join processor, repartition topic(s) (if a repartition is required), and the state stores involved in the join. Also, by naming the state stores, the changelog topics backing the state stores are named as well. It's important to note that naming the stores **will not** make them queryable via Interactive Queries.   
Another feature delivered by `StreamJoined` is that you can now configure the type of state store used in the join. You can elect to use in-memory stores or custom state stores for a stream-stream join. Note that the provided stores will not be available for querying via Interactive Queries. With the addition of `StreamJoined`, stream-stream join operations using `Joined` have been deprecated. Please switch over to stream-stream join methods using the new overloaded methods. You can get more details from [KIP-479](https://cwiki.apache.org/confluence/display/KAFKA/KIP-479%3A+Add+StreamJoined+config+object+to+Join). 

With the introduction of incremental cooperative rebalancing, Streams no longer requires all tasks be revoked at the beginning of a rebalance. Instead, at the completion of the rebalance only those tasks which are to be migrated to another consumer for overall load balance will need to be closed and revoked. This changes the semantics of the `StateListener` a bit, as it will not necessarily transition to `REBALANCING` at the beginning of a rebalance anymore. Note that this means IQ will now be available at all times except during state restoration, including while a rebalance is in progress. If restoration is occurring when a rebalance begins, we will continue to actively restore the state stores and/or process standby tasks during a cooperative rebalance. Note that with this new rebalancing protocol, you may sometimes see a rebalance be followed by a second short rebalance that ensures all tasks are safely distributed. For details on please see [KIP-429](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%3A+Kafka+Consumer+Incremental+Rebalance+Protocol). 

The 2.4.0 release contains newly added and reworked metrics. [KIP-444](https://cwiki.apache.org/confluence/display/KAFKA/KIP-444%3A+Augment+metrics+for+Kafka+Streams) adds new _client level_ (i.e., `KafkaStreams` instance level) metrics to the existing thread-level, task-level, and processor-/state-store-level metrics. For a full list of available client level metrics, see the [KafkaStreams monitoring](/24/#kafka_streams_client_monitoring) section in the operations guide.   
Furthermore, RocksDB metrics are exposed via [KIP-471](https://cwiki.apache.org/confluence/display/KAFKA/KIP-471%3A+Expose+RocksDB+Metrics+in+Kafka+Streams). For a full list of available RocksDB metrics, see the [RocksDB monitoring](/24/#kafka_streams_rocksdb_monitoring) section in the operations guide. 

Kafka Streams `test-utils` got improved via [KIP-470](https://cwiki.apache.org/confluence/display/KAFKA/KIP-470%3A+TopologyTestDriver+test+input+and+output+usability+improvements) to simplify the process of using `TopologyTestDriver` to test your application code. We deprecated `ConsumerRecordFactory`, `TopologyTestDriver#pipeInput()`, `OutputVerifier`, as well as `TopologyTestDriver#readOutput()` and replace them with `TestInputTopic` and `TestOutputTopic`, respectively. We also introduced a new class `TestRecord` that simplifies assertion code. For full details see the [Testing section](/24/streams/developer-guide/testing.html) in the developer guide. 

In 2.4.0, we deprecated `WindowStore#put(K key, V value)` that should never be used. Instead the existing `WindowStore#put(K key, V value, long windowStartTimestamp)` should be used ([KIP-474](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=115526545)). 

Furthermore, the `PartitionGrouper` interface and its corresponding configuration parameter `partition.grouper` were deprecated ([KIP-528](https://cwiki.apache.org/confluence/display/KAFKA/KIP-528%3A+Deprecate+PartitionGrouper+configuration+and+interface)) and will be removed in the next major release ([KAFKA-7785](https://issues.apache.org/jira/browse/KAFKA-7785). Hence, this feature won't be supported in the future any longer and you need to updated your code accordingly. If you use a custom `PartitionGrouper` and stop to use it, the created tasks might change. Hence, you will need to reset your application to upgrade it. 

# Streams API changes in 2.3.0

Version 2.3.0 adds the Suppress operator to the `kafka-streams-scala` Ktable API.

As of 2.3.0 Streams now offers an in-memory version of the window ([KIP-428](https://cwiki.apache.org/confluence/display/KAFKA/KIP-428%3A+Add+in-memory+window+store)) and the session ([KIP-445](https://cwiki.apache.org/confluence/display/KAFKA/KIP-445%3A+In-memory+Session+Store)) store, in addition to the persistent ones based on RocksDB. The new public interfaces `inMemoryWindowStore()` and `inMemorySessionStore()` are added to `Stores` and provide the built-in in-memory window or session store. 

As of 2.3.0 we've updated how to turn on optimizations. Now to enable optimizations, you need to do two things. First add this line to your properties `properties.setProperty(StreamsConfig.TOPOLOGY_OPTIMIZATION, StreamsConfig.OPTIMIZE);`, as you have done before. Second, when constructing your `KafkaStreams` instance, you'll need to pass your configuration properties when building your topology by using the overloaded `StreamsBuilder.build(Properties)` method. For example `KafkaStreams myStream = new KafkaStreams(streamsBuilder.build(properties), properties)`. 

In 2.3.0 we have added default implementation to `close()` and `configure()` for `Serializer`, `Deserializer` and `Serde` so that they can be implemented by lambda expression. For more details please read [KIP-331](https://cwiki.apache.org/confluence/display/KAFKA/KIP-331+Add+default+implementation+to+close%28%29+and+configure%28%29+for+Serializer%2C+Deserializer+and+Serde). 

To improve operator semantics, new store types are added that allow storing an additional timestamp per key-value pair or window. Some DSL operators (for example KTables) are using those new stores. Hence, you can now retrieve the last update timestamp via Interactive Queries if you specify `TimestampedKeyValueStoreType` or `TimestampedWindowStoreType` as your `QueryableStoreType`. While this change is mainly transparent, there are some corner cases that may require code changes: **Caution: If you receive an untyped store and use a cast, you might need to update your code to cast to the correct type. Otherwise, you might get an exception similar to`java.lang.ClassCastException: class org.apache.kafka.streams.state.ValueAndTimestamp cannot be cast to class YOUR-VALUE-TYPE` upon getting a value from the store.** Additionally, `TopologyTestDriver#getStateStore()` only returns non-built-in stores and throws an exception if a built-in store is accessed. For more details please read [KIP-258](https://cwiki.apache.org/confluence/display/KAFKA/KIP-258%3A+Allow+to+Store+Record+Timestamps+in+RocksDB). 

To improve type safety, a new operator `KStream#flatTransformValues` is added. For more details please read [KIP-313](https://cwiki.apache.org/confluence/display/KAFKA/KIP-313%3A+Add+KStream.flatTransform+and+KStream.flatTransformValues). 

Kafka Streams used to set the configuration parameter `max.poll.interval.ms` to `Integer.MAX_VALUE`. This default value is removed and Kafka Streams uses the consumer default value now. For more details please read [KIP-442](https://cwiki.apache.org/confluence/display/KAFKA/KIP-442%3A+Return+to+default+max+poll+interval+in+Streams). 

Default configuration for repartition topic was changed: The segment size for index files (`segment.index.bytes`) is no longer 50MB, but uses the cluster default. Similarly, the configuration `segment.ms` in no longer 10 minutes, but uses the cluster default configuration. Lastly, the retention period (`retention.ms`) is changed from `Long.MAX_VALUE` to `-1` (infinite). For more details please read [KIP-443](https://cwiki.apache.org/confluence/display/KAFKA/KIP-443%3A+Return+to+default+segment.ms+and+segment.index.bytes+in+Streams+repartition+topics). 

To avoid memory leaks, `RocksDBConfigSetter` has a new `close()` method that is called on shutdown. Users should implement this method to release any memory used by RocksDB config objects, by closing those objects. For more details please read [KIP-453](https://cwiki.apache.org/confluence/display/KAFKA/KIP-453%3A+Add+close%28%29+method+to+RocksDBConfigSetter). 

RocksDB dependency was updated to version `5.18.3`. The new version allows to specify more RocksDB configurations, including `WriteBufferManager` which helps to limit RocksDB off-heap memory usage. For more details please read [KAFKA-8215](https://issues.apache.org/jira/browse/KAFKA-8215). 

# Notable changes in Kafka Streams 2.2.1

As of Kafka Streams 2.2.1 a message format 0.11 or higher is required; this implies that brokers must be on version 0.11.0 or higher. 

# Streams API changes in 2.2.0

We've simplified the `KafkaStreams#state` transition diagram during the starting up phase a bit in 2.2.0: in older versions the state will transit from `CREATED` to `RUNNING`, and then to `REBALANCING` to get the first stream task assignment, and then back to `RUNNING`; starting in 2.2.0 it will transit from `CREATED` directly to `REBALANCING` and then to `RUNNING`. If you have registered a `StateListener` that captures state transition events, you may need to adjust your listener implementation accordingly for this simplification (in practice, your listener logic should be very unlikely to be affected at all). 

In `WindowedSerdes`, we've added a new static constructor to return a `TimeWindowSerde` with configurable window size. This is to help users to construct time window serdes to read directly from a time-windowed store's changelog. More details can be found in [KIP-393](https://cwiki.apache.org/confluence/display/KAFKA/KIP-393%3A+Time+windowed+serde+to+properly+deserialize+changelog+input+topic). 

In 2.2.0 we have extended a few public interfaces including `KafkaStreams` to extend `AutoCloseable` so that they can be used in a try-with-resource statement. For a full list of public interfaces that get impacted please read [KIP-376](https://cwiki.apache.org/confluence/display/KAFKA/KIP-376%3A+Implement+AutoClosable+on+appropriate+classes+that+want+to+be+used+in+a+try-with-resource+statement). 

# Streams API changes in 2.1.0

We updated `TopologyDescription` API to allow for better runtime checking. Users are encouraged to use `#topicSet()` and `#topicPattern()` accordingly on `TopologyDescription.Source` nodes, instead of using `#topics()`, which has since been deprecated. Similarly, use `#topic()` and `#topicNameExtractor()` to get descriptions of `TopologyDescription.Sink` nodes. For more details, see [KIP-321](https://cwiki.apache.org/confluence/display/KAFKA/KIP-321%3A+Update+TopologyDescription+to+better+represent+Source+and+Sink+Nodes). 

We've added a new class `Grouped` and deprecated `Serialized`. The intent of adding `Grouped` is the ability to name repartition topics created when performing aggregation operations. Users can name the potential repartition topic using the `Grouped#as()` method which takes a `String` and is used as part of the repartition topic name. The resulting repartition topic name will still follow the pattern of `${application-id}->name<-repartition`. The `Grouped` class is now favored over `Serialized` in `KStream#groupByKey()`, `KStream#groupBy()`, and `KTable#groupBy()`. Note that Kafka Streams does not automatically create repartition topics for aggregation operations. Additionally, we've updated the `Joined` class with a new method `Joined#withName` enabling users to name any repartition topics required for performing Stream/Stream or Stream/Table join. For more details repartition topic naming, see [KIP-372](https://cwiki.apache.org/confluence/display/KAFKA/KIP-372%3A+Naming+Repartition+Topics+for+Joins+and+Grouping). As a result we've updated the Kafka Streams Scala API and removed the `Serialized` class in favor of adding `Grouped`. If you just rely on the implicit `Serialized`, you just need to recompile; if you pass in `Serialized` explicitly, sorry you'll have to make code changes. 

We've added a new config named `max.task.idle.ms` to allow users specify how to handle out-of-order data within a task that may be processing multiple topic-partitions (see [Out-of-Order Handling](/24/streams/core-concepts.html#streams_out_of_ordering) section for more details). The default value is set to `0`, to favor minimized latency over synchronization between multiple input streams from topic-partitions. If users would like to wait for longer time when some of the topic-partitions do not have data available to process and hence cannot determine its corresponding stream time, they can override this config to a larger value. 

We've added the missing `SessionBytesStoreSupplier#retentionPeriod()` to be consistent with the `WindowBytesStoreSupplier` which allows users to get the specified retention period for session-windowed stores. We've also added the missing `StoreBuilder#withCachingDisabled()` to allow users to turn off caching for their customized stores. 

We added a new serde for UUIDs (`Serdes.UUIDSerde`) that you can use via `Serdes.UUID()` (cf. [KIP-206](https://cwiki.apache.org/confluence/display/KAFKA/KIP-206%3A+Add+support+for+UUID+serialization+and+deserialization)). 

We updated a list of methods that take `long` arguments as either timestamp (fix point) or duration (time period) and replaced them with `Instant` and `Duration` parameters for improved semantics. Some old methods base on `long` are deprecated and users are encouraged to update their code.   
In particular, aggregation windows (hopping/tumbling/unlimited time windows and session windows) as well as join windows now take `Duration` arguments to specify window size, hop, and gap parameters. Also, window sizes and retention times are now specified as `Duration` type in `Stores` class. The `Window` class has new methods `#startTime()` and `#endTime()` that return window start/end timestamp as `Instant`. For interactive queries, there are new `#fetch(...)` overloads taking `Instant` arguments. Additionally, punctuations are now registerd via `ProcessorContext#schedule(Duration interval, ...)`. For more details, see [KIP-358](https://cwiki.apache.org/confluence/display/KAFKA/KIP-358%3A+Migrate+Streams+API+to+Duration+instead+of+long+ms+times). 

We deprecated `KafkaStreams#close(...)` and replaced it with `KafkaStreams#close(Duration)` that accepts a single timeout argument Note: the new `#close(Duration)` method has improved (but slightly different) semantics. For more details, see [KIP-358](https://cwiki.apache.org/confluence/display/KAFKA/KIP-358%3A+Migrate+Streams+API+to+Duration+instead+of+long+ms+times). 

The newly exposed `AdminClient` metrics are now available when calling the `KafkaStream#metrics()` method. For more details on exposing `AdminClients` metrics see [KIP-324](https://cwiki.apache.org/confluence/display/KAFKA/KIP-324%3A+Add+method+to+get+metrics%28%29+in+AdminClient)

We deprecated the notion of segments in window stores as those are intended to be an implementation details. Thus, method `Windows#segments()` and variable `Windows#segments` were deprecated. If you implement custom windows, you should update your code accordingly. Similarly, `WindowBytesStoreSupplier#segments()` was deprecated and replaced with `WindowBytesStoreSupplier#segmentInterval()`. If you implement custom window store, you need to update your code accordingly. Finally, `Stores#persistentWindowStore(...)` were deprecated and replaced with a new overload that does not allow to specify the number of segments any longer. For more details, see [KIP-319](https://cwiki.apache.org/confluence/display/KAFKA/KIP-319%3A+Replace+segments+with+segmentInterval+in+WindowBytesStoreSupplier) (note: [KIP-328](https://cwiki.apache.org/confluence/display/KAFKA/KIP-328%3A+Ability+to+suppress+updates+for+KTables) and [KIP-358](https://cwiki.apache.org/confluence/display/KAFKA/KIP-358%3A+Migrate+Streams+API+to+Duration+instead+of+long+ms+times) 'overlap' with KIP-319). 

We've added an overloaded `StreamsBuilder#build` method that accepts an instance of `java.util.Properties` with the intent of using the `StreamsConfig#TOPOLOGY_OPTIMIZATION` config added in Kafka Streams 2.0. Before 2.1, when building a topology with the DSL, Kafka Streams writes the physical plan as the user makes calls on the DSL. Now by providing a `java.util.Properties` instance when executing a `StreamsBuilder#build` call, Kafka Streams can optimize the physical plan of the topology, provided the `StreamsConfig#TOPOLOGY_OPTIMIZATION` config is set to `StreamsConfig#OPTIMIZE`. By setting `StreamsConfig#OPTIMIZE` in addition to the `KTable` optimization of reusing the source topic as the changelog topic, the topology may be optimized to merge redundant repartition topics into one repartition topic. The original no parameter version of `StreamsBuilder#build` is still available for those who wish to not optimize their topology. Note that enabling optimization of the topology may require you to do an application reset when redeploying the application. For more details, see [KIP-312](https://cwiki.apache.org/confluence/display/KAFKA/KIP-312%3A+Add+Overloaded+StreamsBuilder+Build+Method+to+Accept+java.util.Properties)

We are introducing static membership towards Kafka Streams user. This feature reduces unnecessary rebalances during normal application upgrades or rolling bounces. For more details on how to use it, checkout [static membership design](/24/design/#static_membership). Note, Kafka Streams uses the same `ConsumerConfig#GROUP_INSTANCE_ID_CONFIG`, and you only need to make sure it is uniquely defined across different stream instances in one application. 

# Streams API changes in 2.0.0

In 2.0.0 we have added a few new APIs on the `ReadOnlyWindowStore` interface (for details please read Streams API changes below). If you have customized window store implementations that extends the `ReadOnlyWindowStore` interface you need to make code changes. 

In addition, if you using Java 8 method references in your Kafka Streams code you might need to update your code to resolve method ambiguities. Hot-swapping the jar-file only might not work for this case. See below a complete list of 2.0.0 API and semantic changes that allow you to advance your application and/or simplify your code base. 

We moved `Consumed` interface from `org.apache.kafka.streams` to `org.apache.kafka.streams.kstream` as it was mistakenly placed in the previous release. If your code has already used it there is a simple one-liner change needed in your import statement. 

We have also removed some public APIs that are deprecated prior to 1.0.x in 2.0.0. See below for a detailed list of removed APIs. 

We have removed the `skippedDueToDeserializationError-rate` and `skippedDueToDeserializationError-total` metrics. Deserialization errors, and all other causes of record skipping, are now accounted for in the pre-existing metrics `skipped-records-rate` and `skipped-records-total`. When a record is skipped, the event is now logged at WARN level. If these warnings become burdensome, we recommend explicitly filtering out unprocessable records instead of depending on record skipping semantics. For more details, see [KIP-274](https://cwiki.apache.org/confluence/display/KAFKA/KIP-274%3A+Kafka+Streams+Skipped+Records+Metrics). As of right now, the potential causes of skipped records are: 

  * `null` keys in table sources
  * `null` keys in table-table inner/left/outer/right joins
  * `null` keys or values in stream-table joins
  * `null` keys or values in stream-stream joins
  * `null` keys or values in aggregations on grouped streams
  * `null` keys or values in reductions on grouped streams
  * `null` keys in aggregations on windowed streams
  * `null` keys in reductions on windowed streams
  * `null` keys in aggregations on session-windowed streams
  * Errors producing results, when the configured `default.production.exception.handler` decides to `CONTINUE` (the default is to `FAIL` and throw an exception). 
  * Errors deserializing records, when the configured `default.deserialization.exception.handler` decides to `CONTINUE` (the default is to `FAIL` and throw an exception). This was the case previously captured in the `skippedDueToDeserializationError` metrics. 
  * Fetched records having a negative timestamp.



We've also fixed the metrics name for time and session windowed store operations in 2.0. As a result, our current built-in stores will have their store types in the metric names as `in-memory-state`, `in-memory-lru-state`, `rocksdb-state`, `rocksdb-window-state`, and `rocksdb-session-state`. For example, a RocksDB time windowed store's put operation metrics would now be `kafka.streams:type=stream-rocksdb-window-state-metrics,client-id=([-.\w]+),task-id=([-.\w]+),rocksdb-window-state-id=([-.\w]+)`. Users need to update their metrics collecting and reporting systems for their time and session windowed stores accordingly. For more details, please read the [State Store Metrics](/24/#kafka_streams_store_monitoring) section. 

We have added support for methods in `ReadOnlyWindowStore` which allows for querying a single window's key-value pair. For users who have customized window store implementations on the above interface, they'd need to update their code to implement the newly added method as well. For more details, see [KIP-261](https://cwiki.apache.org/confluence/display/KAFKA/KIP-261%3A+Add+Single+Value+Fetch+in+Window+Stores). 

We have added public `WindowedSerdes` to allow users to read from / write to a topic storing windowed table changelogs directly. In addition, in `StreamsConfig` we have also added `default.windowed.key.serde.inner` and `default.windowed.value.serde.inner` to let users specify inner serdes if the default serde classes are windowed serdes. For more details, see [KIP-265](https://cwiki.apache.org/confluence/display/KAFKA/KIP-265%3A+Make+Windowed+Serde+to+public+APIs). 

We've added message header support in the `Processor API` in Kafka 2.0.0. In particular, we have added a new API `ProcessorContext#headers()` which returns a `Headers` object that keeps track of the headers of the source topic's message that is being processed. Through this object, users can manipulate the headers map that is being propagated throughout the processor topology as well. For more details please feel free to read the [Developer Guide](/24/streams/developer-guide/processor-api.html#accessing-processor-context) section. 

We have deprecated constructors of `KafkaStreams` that take a `StreamsConfig` as parameter. Please use the other corresponding constructors that accept `java.util.Properties` instead. For more details, see [KIP-245](https://cwiki.apache.org/confluence/display/KAFKA/KIP-245%3A+Use+Properties+instead+of+StreamsConfig+in+KafkaStreams+constructor). 

Kafka 2.0.0 allows to manipulate timestamps of output records using the Processor API ([KIP-251](https://cwiki.apache.org/confluence/display/KAFKA/KIP-251%3A+Allow+timestamp+manipulation+in+Processor+API)). To enable this new feature, `ProcessorContext#forward(...)` was modified. The two existing overloads `#forward(Object key, Object value, String childName)` and `#forward(Object key, Object value, int childIndex)` were deprecated and a new overload `#forward(Object key, Object value, To to)` was added. The new class `To` allows you to send records to all or specific downstream processors by name and to set the timestamp for the output record. Forwarding based on child index is not supported in the new API any longer. 

We have added support to allow routing records dynamically to Kafka topics. More specifically, in both the lower-level `Topology#addSink` and higher-level `KStream#to` APIs, we have added variants that take a `TopicNameExtractor` instance instead of a specific `String` typed topic name, such that for each received record from the upstream processor, the library will dynamically determine which Kafka topic to write to based on the record's key and value, as well as record context. Note that all the Kafka topics that may possibly be used are still considered as user topics and hence required to be pre-created. In addition to that, we have modified the `StreamPartitioner` interface to add the topic name parameter since the topic name now may not be known beforehand; users who have customized implementations of this interface would need to update their code while upgrading their application to use Kafka Streams 2.0.0. 

[KIP-284](https://cwiki.apache.org/confluence/x/DVyHB) changed the retention time for repartition topics by setting its default value to `Long.MAX_VALUE`. Instead of relying on data retention Kafka Streams uses the new purge data API to delete consumed data from those topics and to keep used storage small now. 

We have modified the `ProcessorStateManger#register(...)` signature and removed the deprecated `loggingEnabled` boolean parameter as it is specified in the `StoreBuilder`. Users who used this function to register their state stores into the processor topology need to simply update their code and remove this parameter from the caller. 

Kafka Streams DSL for Scala is a new Kafka Streams client library available for developers authoring Kafka Streams applications in Scala. It wraps core Kafka Streams DSL types to make it easier to call when interoperating with Scala code. For example, it includes higher order functions as parameters for transformations avoiding the need anonymous classes in Java 7 or experimental SAM type conversions in Scala 2.11, automatic conversion between Java and Scala collection types, a way to implicitly provide SerDes to reduce boilerplate from your application and make it more typesafe, and more! For more information see the [Kafka Streams DSL for Scala documentation](/24/streams/developer-guide/dsl-api.html#scala-dsl) and [KIP-270](https://cwiki.apache.org/confluence/display/KAFKA/KIP-270+-+A+Scala+Wrapper+Library+for+Kafka+Streams). 

We have removed these deprecated APIs: 

  * `KafkaStreams#toString` no longer returns the topology and runtime metadata; to get topology metadata users can call `Topology#describe()` and to get thread runtime metadata users can call `KafkaStreams#localThreadsMetadata` (they are deprecated since 1.0.0). For detailed guidance on how to update your code please read here
  * `TopologyBuilder` and `KStreamBuilder` are removed and replaced by `Topology` and `StreamsBuidler` respectively (they are deprecated since 1.0.0). For detailed guidance on how to update your code please read here
  * `StateStoreSupplier` are removed and replaced with `StoreBuilder` (they are deprecated since 1.0.0); and the corresponding `Stores#create` and `KStream, KTable, KGroupedStream` overloaded functions that use it have also been removed. For detailed guidance on how to update your code please read here
  * `KStream, KTable, KGroupedStream` overloaded functions that requires serde and other specifications explicitly are removed and replaced with simpler overloaded functions that use `Consumed, Produced, Serialized, Materialized, Joined` (they are deprecated since 1.0.0). For detailed guidance on how to update your code please read here
  * `Processor#punctuate`, `ValueTransformer#punctuate`, `ValueTransformer#punctuate` and `ProcessorContext#schedule(long)` are removed and replaced by `ProcessorContext#schedule(long, PunctuationType, Punctuator)` (they are deprecated in 1.0.0). 
  * The second `boolean` typed parameter "loggingEnabled" in `ProcessorContext#register` has been removed; users can now use `StoreBuilder#withLoggingEnabled, withLoggingDisabled` to specify the behavior when they create the state store. 
  * `KTable#writeAs, print, foreach, to, through` are removed, users can call `KTable#tostream()#writeAs` instead for the same purpose (they are deprecated since 0.11.0.0). For detailed list of removed APIs please read here
  * `StreamsConfig#KEY_SERDE_CLASS_CONFIG, VALUE_SERDE_CLASS_CONFIG, TIMESTAMP_EXTRACTOR_CLASS_CONFIG` are removed and replaced with `StreamsConfig#DEFAULT_KEY_SERDE_CLASS_CONFIG, DEFAULT_VALUE_SERDE_CLASS_CONFIG, DEFAULT_TIMESTAMP_EXTRACTOR_CLASS_CONFIG` respectively (they are deprecated since 0.11.0.0). 
  * `StreamsConfig#ZOOKEEPER_CONNECT_CONFIG` are removed as we do not need ZooKeeper dependency in Streams any more (it is deprecated since 0.10.2.0). 



# Streams API changes in 1.1.0

We have added support for methods in `ReadOnlyWindowStore` which allows for querying `WindowStore`s without the necessity of providing keys. For users who have customized window store implementations on the above interface, they'd need to update their code to implement the newly added method as well. For more details, see [KIP-205](https://cwiki.apache.org/confluence/display/KAFKA/KIP-205%3A+Add+all%28%29+and+range%28%29+API+to+ReadOnlyWindowStore). 

There is a new artifact `kafka-streams-test-utils` providing a `TopologyTestDriver`, `ConsumerRecordFactory`, and `OutputVerifier` class. You can include the new artifact as a regular dependency to your unit tests and use the test driver to test your business logic of your Kafka Streams application. For more details, see [KIP-247](https://cwiki.apache.org/confluence/display/KAFKA/KIP-247%3A+Add+public+test+utils+for+Kafka+Streams). 

The introduction of [KIP-220](https://cwiki.apache.org/confluence/display/KAFKA/KIP-220%3A+Add+AdminClient+into+Kafka+Streams%27+ClientSupplier) enables you to provide configuration parameters for the embedded admin client created by Kafka Streams, similar to the embedded producer and consumer clients. You can provide the configs via `StreamsConfig` by adding the configs with the prefix `admin.` as defined by `StreamsConfig#adminClientPrefix(String)` to distinguish them from configurations of other clients that share the same config names. 

New method in `KTable`

  * `transformValues` methods have been added to `KTable`. Similar to those on `KStream`, these methods allow for richer, stateful, value transformation similar to the Processor API.



New method in `GlobalKTable`

  * A method has been provided such that it will return the store name associated with the `GlobalKTable` or `null` if the store name is non-queryable. 



New methods in `KafkaStreams`: 

  * added overload for the constructor that allows overriding the `Time` object used for tracking system wall-clock time; this is useful for unit testing your application code. 



New methods in `KafkaClientSupplier`: 

  * added `getAdminClient(config)` that allows to override an `AdminClient` used for administrative requests such as internal topic creations, etc. 



New error handling for exceptions during production:

  * added interface `ProductionExceptionHandler` that allows implementors to decide whether or not Streams should `FAIL` or `CONTINUE` when certain exception occur while trying to produce.
  * provided an implementation, `DefaultProductionExceptionHandler` that always fails, preserving the existing behavior by default.
  * changing which implementation is used can be done by settings `default.production.exception.handler` to the fully qualified name of a class implementing this interface.



Changes in `StreamsResetter`: 

  * added options to specify input topics offsets to reset according to [KIP-171](https://cwiki.apache.org/confluence/display/KAFKA/KIP-171+-+Extend+Consumer+Group+Reset+Offset+for+Stream+Application)



# Streams API changes in 1.0.0

With 1.0 a major API refactoring was accomplished and the new API is cleaner and easier to use. This change includes the five main classes `KafkaStreams`, `KStreamBuilder`, `KStream`, `KTable`, and `TopologyBuilder` (and some more others). All changes are fully backward compatible as old API is only deprecated but not removed. We recommend to move to the new API as soon as you can. We will summarize all API changes in the next paragraphs. 

The two main classes to specify a topology via the DSL (`KStreamBuilder`) or the Processor API (`TopologyBuilder`) were deprecated and replaced by `StreamsBuilder` and `Topology` (both new classes are located in package `org.apache.kafka.streams`). Note, that `StreamsBuilder` does not extend `Topology`, i.e., the class hierarchy is different now. The new classes have basically the same methods as the old ones to build a topology via DSL or Processor API. However, some internal methods that were public in `KStreamBuilder` and `TopologyBuilder` but not part of the actual API are not present in the new classes any longer. Furthermore, some overloads were simplified compared to the original classes. See [KIP-120](https://cwiki.apache.org/confluence/display/KAFKA/KIP-120%3A+Cleanup+Kafka+Streams+builder+API) and [KIP-182](https://cwiki.apache.org/confluence/display/KAFKA/KIP-182%3A+Reduce+Streams+DSL+overloads+and+allow+easier+use+of+custom+storage+engines) for full details. 

Changing how a topology is specified also affects `KafkaStreams` constructors, that now only accept a `Topology`. Using the DSL builder class `StreamsBuilder` one can get the constructed `Topology` via `StreamsBuilder#build()`. Additionally, a new class `org.apache.kafka.streams.TopologyDescription` (and some more dependent classes) were added. Those can be used to get a detailed description of the specified topology and can be obtained by calling `Topology#describe()`. An example using this new API is shown in the [quickstart section](/24/streams/quickstart). 

New methods in `KStream`: 

  * With the introduction of [KIP-202](https://cwiki.apache.org/confluence/display/KAFKA/KIP-202+Move+merge%28%29+from+StreamsBuilder+to+KStream) a new method `merge()` has been created in `KStream` as the StreamsBuilder class's `StreamsBuilder#merge()` has been removed. The method signature was also changed, too: instead of providing multiple `KStream`s into the method at the once, only a single `KStream` is accepted. 



New methods in `KafkaStreams`: 

  * retrieve the current runtime information about the local threads via `localThreadsMetadata()`
  * observe the restoration of all state stores via `setGlobalStateRestoreListener()`, in which users can provide their customized implementation of the `org.apache.kafka.streams.processor.StateRestoreListener` interface



Deprecated / modified methods in `KafkaStreams`: 

  * `toString()`, `toString(final String indent)` were previously used to return static and runtime information. They have been deprecated in favor of using the new classes/methods `localThreadsMetadata()` / `ThreadMetadata` (returning runtime information) and `TopologyDescription` / `Topology#describe()` (returning static information). 
  * With the introduction of [KIP-182](https://cwiki.apache.org/confluence/display/KAFKA/KIP-182%3A+Reduce+Streams+DSL+overloads+and+allow+easier+use+of+custom+storage+engines) you should no longer pass in `Serde` to `KStream#print` operations. If you can't rely on using `toString` to print your keys an values, you should instead you provide a custom `KeyValueMapper` via the `Printed#withKeyValueMapper` call. 
  * `setStateListener()` now can only be set before the application start running, i.e. before `KafkaStreams.start()` is called. 



Deprecated methods in `KGroupedStream`

  * Windowed aggregations have been deprecated from `KGroupedStream` and moved to `WindowedKStream`. You can now perform a windowed aggregation by, for example, using `KGroupedStream#windowedBy(Windows)#reduce(Reducer)`. 



Modified methods in `Processor`: 

  * The Processor API was extended to allow users to schedule `punctuate` functions either based on data-driven **stream time** or wall-clock time. As a result, the original `ProcessorContext#schedule` is deprecated with a new overloaded function that accepts a user customizable `Punctuator` callback interface, which triggers its `punctuate` API method periodically based on the `PunctuationType`. The `PunctuationType` determines what notion of time is used for the punctuation scheduling: either [stream time](/24/streams/core-concepts#streams_time) or wall-clock time (by default, **stream time** is configured to represent event time via `TimestampExtractor`). In addition, the `punctuate` function inside `Processor` is also deprecated. 

Before this, users could only schedule based on stream time (i.e. `PunctuationType.STREAM_TIME`) and hence the `punctuate` function was data-driven only because stream time is determined (and advanced forward) by the timestamps derived from the input data. If there is no data arriving at the processor, the stream time would not advance and hence punctuation will not be triggered. On the other hand, When wall-clock time (i.e. `PunctuationType.WALL_CLOCK_TIME`) is used, `punctuate` will be triggered purely based on wall-clock time. So for example if the `Punctuator` function is scheduled based on `PunctuationType.WALL_CLOCK_TIME`, if these 60 records were processed within 20 seconds, `punctuate` would be called 2 times (one time every 10 seconds); if these 60 records were processed within 5 seconds, then no `punctuate` would be called at all. Users can schedule multiple `Punctuator` callbacks with different `PunctuationType`s within the same processor by simply calling `ProcessorContext#schedule` multiple times inside processor's `init()` method. 




If you are monitoring on task level or processor-node / state store level Streams metrics, please note that the metrics sensor name and hierarchy was changed: The task ids, store names and processor names are no longer in the sensor metrics names, but instead are added as tags of the sensors to achieve consistent metrics hierarchy. As a result you may need to make corresponding code changes on your metrics reporting and monitoring tools when upgrading to 1.0.0. Detailed metrics sensor can be found in the Streams Monitoring section. 

The introduction of [KIP-161](https://cwiki.apache.org/confluence/display/KAFKA/KIP-161%3A+streams+deserialization+exception+handlers) enables you to provide a default exception handler for deserialization errors when reading data from Kafka rather than throwing the exception all the way out of your streams application. You can provide the configs via the `StreamsConfig` as `StreamsConfig#DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG`. The specified handler must implement the `org.apache.kafka.streams.errors.DeserializationExceptionHandler` interface. 

The introduction of [KIP-173](https://cwiki.apache.org/confluence/display/KAFKA/KIP-173%3A+Add+prefix+to+StreamsConfig+to+enable+setting+default+internal+topic+configs) enables you to provide topic configuration parameters for any topics created by Kafka Streams. This includes repartition and changelog topics. You can provide the configs via the `StreamsConfig` by adding the configs with the prefix as defined by `StreamsConfig#topicPrefix(String)`. Any properties in the `StreamsConfig` with the prefix will be applied when creating internal topics. Any configs that aren't topic configs will be ignored. If you already use `StateStoreSupplier` or `Materialized` to provide configs for changelogs, then they will take precedence over those supplied in the config. 

# Streams API changes in 0.11.0.0

Updates in `StreamsConfig`: 

  * new configuration parameter `processing.guarantee` is added 
  * configuration parameter `key.serde` was deprecated and replaced by `default.key.serde`
  * configuration parameter `value.serde` was deprecated and replaced by `default.value.serde`
  * configuration parameter `timestamp.extractor` was deprecated and replaced by `default.timestamp.extractor`
  * method `keySerde()` was deprecated and replaced by `defaultKeySerde()`
  * method `valueSerde()` was deprecated and replaced by `defaultValueSerde()`
  * new method `defaultTimestampExtractor()` was added 



New methods in `TopologyBuilder`: 

  * added overloads for `addSource()` that allow to define a `TimestampExtractor` per source node 
  * added overloads for `addGlobalStore()` that allow to define a `TimestampExtractor` per source node associated with the global store 



New methods in `KStreamBuilder`: 

  * added overloads for `stream()` that allow to define a `TimestampExtractor` per input stream 
  * added overloads for `table()` that allow to define a `TimestampExtractor` per input table 
  * added overloads for `globalKTable()` that allow to define a `TimestampExtractor` per global table 



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



If you want to view the changelog stream of the `KTable` then you could call `KTable.toStream().print(Printed.toSysOut)`. 

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

  * set a listener to react on application state change via `setStateListener(StateListener listener)`
  * retrieve the current application state via `state()`
  * retrieve the global metrics registry via `metrics()`
  * apply a timeout when closing an application via `close(long timeout, TimeUnit timeUnit)`
  * specify a custom indent when retrieving Kafka Streams information via `toString(String indent)`



Parameter updates in `StreamsConfig`: 

  * parameter `zookeeper.connect` was deprecated; a Kafka Streams application does no longer interact with ZooKeeper for topic management but uses the new broker admin protocol (cf. [KIP-4, Section "Topic Admin Schema"](https://cwiki.apache.org/confluence/display/KAFKA/KIP-4+-+Command+line+and+centralized+administrative+operations#KIP-4-Commandlineandcentralizedadministrativeoperations-TopicAdminSchema.1)) 
  * added many new parameters for metrics, security, and client configurations 



Changes in `StreamsMetrics` interface: 

  * removed methods: `addLatencySensor()`
  * added methods: `addLatencyAndThroughputSensor()`, `addThroughputSensor()`, `recordThroughput()`, `addSensor()`, `removeSensor()`



New methods in `TopologyBuilder`: 

  * added overloads for `addSource()` that allow to define a `auto.offset.reset` policy per source node 
  * added methods `addGlobalStore()` to add global `StateStore`s 



New methods in `KStreamBuilder`: 

  * added overloads for `stream()` and `table()` that allow to define a `auto.offset.reset` policy per input stream/table 
  * added method `globalKTable()` to create a `GlobalKTable`



New joins for `KStream`: 

  * added overloads for `join()` to join with `KTable`
  * added overloads for `join()` and `leftJoin()` to join with `GlobalKTable`
  * note, join semantics in 0.10.2 were improved and thus you might see different result compared to 0.10.0.x and 0.10.1.x (cf. [Kafka Streams Join Semantics](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Streams+Join+Semantics) in the Apache Kafka wiki) 


Aligned `null`-key handling for `KTable` joins: 

  * like all other KTable operations, `KTable-KTable` joins do not throw an exception on `null` key records anymore, but drop those records silently 



New window type _Session Windows_ : 

  * added class `SessionWindows` to specify session windows 
  * added overloads for `KGroupedStream` methods `count()`, `reduce()`, and `aggregate()` to allow session window aggregations 



Changes to `TimestampExtractor`: 

  * method `extract()` has a second parameter now 
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



[Previous](/24/streams/developer-guide/app-reset-tool) Next

  * [Documentation](/documentation)
  * [Kafka Streams](/streams)


