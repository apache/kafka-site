---
title: Upgrading
description: 
weight: 5
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

## Upgrading from 0.8.x, 0.9.x, 0.10.0.x, 0.10.1.x, 0.10.2.x, 0.11.0.x, 1.0.x, 1.1.x, or 2.0.0 to 2.1.0

**Note that 2.1.x contains a change to the internal schema used to store consumer offsets. Once the upgrade is complete, it will not be possible to downgrade to previous versions. See the rolling upgrade notes below for more detail.**

**For a rolling upgrade:**

  1. Update server.properties on all brokers and add the following properties. CURRENT_KAFKA_VERSION refers to the version you are upgrading from. CURRENT_MESSAGE_FORMAT_VERSION refers to the message format version currently in use. If you have previously overridden the message format version, you should keep its current value. Alternatively, if you are upgrading from a version prior to 0.11.0.x, then CURRENT_MESSAGE_FORMAT_VERSION should be set to match CURRENT_KAFKA_VERSION. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2, 0.9.0, 0.10.0, 0.10.1, 0.10.2, 0.11.0, 1.0, 1.1).
     * log.message.format.version=CURRENT_MESSAGE_FORMAT_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.)
If you are upgrading from 0.11.0.x, 1.0.x, 1.1.x, or 2.0.x and you have not overridden the message format, then you only need to override the inter-broker protocol version. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (0.11.0, 1.0, 1.1, 2.0).
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. Once you have done so, the brokers will be running the latest version and you can verify that the cluster's behavior and performance meets expectations. It is still possible to downgrade at this point if there are any problems. 
  3. Once the cluster's behavior and performance has been verified, bump the protocol version by editing `inter.broker.protocol.version` and setting it to 2.1. 
  4. Restart the brokers one by one for the new protocol version to take effect. Once the brokers begin using the latest protocol version, it will no longer be possible to downgrade the cluster to an older version. 
  5. If you have overridden the message format version as instructed above, then you need to do one more rolling restart to upgrade it to its latest version. Once all (or most) consumers have been upgraded to 0.11.0 or later, change log.message.format.version to 2.1 on each broker and restart them one by one. Note that the older Scala clients, which are no longer maintained, do not support the message format introduced in 0.11, so to avoid conversion costs (or to take advantage of exactly once semantics), the newer Java clients must be used. 



**Additional Upgrade Notes:**

  1. Offset expiration semantics has slightly changed in this version. According to the new semantics, offsets of partitions in a group will not be removed while the group is subscribed to the corresponding topic and is still active (has active consumers). If group becomes empty all its offsets will be removed after default offset retention period (or the one set by broker) has passed (unless the group becomes active again). Offsets associated with standalone (simple) consumers, that do not use Kafka group management, will be removed after default offset retention period (or the one set by broker) has passed since their last commit.
  2. The default for console consumer's `enable.auto.commit` property when no `group.id` is provided is now set to `false`. This is to avoid polluting the consumer coordinator cache as the auto-generated group is not likely to be used by other consumers.
  3. The default value for the producer's `retries` config was changed to `Integer.MAX_VALUE`, as we introduced `delivery.timeout.ms` in [KIP-91](https://cwiki.apache.org/confluence/display/KAFKA/KIP-91+Provide+Intuitive+User+Timeouts+in+The+Producer), which sets an upper bound on the total time between sending a record and receiving acknowledgement from the broker. By default, the delivery timeout is set to 2 minutes.
  4. By default, MirrorMaker now overrides `delivery.timeout.ms` to `Integer.MAX_VALUE` when configuring the producer. If you have overridden the value of `retries` in order to fail faster, you will instead need to override `delivery.timeout.ms`.
  5. The `ListGroup` API now expects, as a recommended alternative, `Describe Group` access to the groups a user should be able to list. Even though the old `Describe Cluster` access is still supported for backward compatibility, using it for this API is not advised.
  6. [KIP-336](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=87298242) deprecates the ExtendedSerializer and ExtendedDeserializer interfaces and propagates the usage of Serializer and Deserializer. ExtendedSerializer and ExtendedDeserializer were introduced with [KIP-82](https://cwiki.apache.org/confluence/display/KAFKA/KIP-82+-+Add+Record+Headers) to provide record headers for serializers and deserializers in a Java 7 compatible fashion. Now we consolidated these interfaces as Java 7 support has been dropped since.



### Notable changes in 2.1.0

  * Jetty has been upgraded to 9.4.12, which excludes TLS_RSA_* ciphers by default because they do not support forward secrecy, see https://github.com/eclipse/jetty.project/issues/2807 for more information.
  * Unclean leader election is automatically enabled by the controller when `unclean.leader.election.enable` config is dynamically updated by using per-topic config override.
  * The `AdminClient` has added a method `AdminClient#metrics()`. Now any application using the `AdminClient` can gain more information and insight by viewing the metrics captured from the `AdminClient`. For more information see [KIP-324](https://cwiki.apache.org/confluence/display/KAFKA/KIP-324%3A+Add+method+to+get+metrics%28%29+in+AdminClient)
  * Kafka now supports Zstandard compression from [KIP-110](https://cwiki.apache.org/confluence/display/KAFKA/KIP-110%3A+Add+Codec+for+ZStandard+Compression). You must upgrade the broker as well as clients to make use of it. Consumers prior to 2.1.0 will not be able to read from topics which use Zstandard compression, so you should not enable it for a topic until all downstream consumers are upgraded. See the KIP for more detail. 



## Upgrading from 0.8.x, 0.9.x, 0.10.0.x, 0.10.1.x, 0.10.2.x, 0.11.0.x, 1.0.x, or 1.1.x to 2.0.0

Kafka 2.0.0 introduces wire protocol changes. By following the recommended rolling upgrade plan below, you guarantee no downtime during the upgrade. However, please review the notable changes in 2.0.0 before upgrading. 

**For a rolling upgrade:**

  1. Update server.properties on all brokers and add the following properties. CURRENT_KAFKA_VERSION refers to the version you are upgrading from. CURRENT_MESSAGE_FORMAT_VERSION refers to the message format version currently in use. If you have previously overridden the message format version, you should keep its current value. Alternatively, if you are upgrading from a version prior to 0.11.0.x, then CURRENT_MESSAGE_FORMAT_VERSION should be set to match CURRENT_KAFKA_VERSION. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2, 0.9.0, 0.10.0, 0.10.1, 0.10.2, 0.11.0, 1.0, 1.1).
     * log.message.format.version=CURRENT_MESSAGE_FORMAT_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.)
If you are upgrading from 0.11.0.x, 1.0.x, or 1.1.x and you have not overridden the message format, then you only need to override the inter-broker protocol format. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (0.11.0, 1.0, 1.1).
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing `inter.broker.protocol.version` and setting it to 2.0. 
  4. Restart the brokers one by one for the new protocol version to take effect.
  5. If you have overridden the message format version as instructed above, then you need to do one more rolling restart to upgrade it to its latest version. Once all (or most) consumers have been upgraded to 0.11.0 or later, change log.message.format.version to 2.0 on each broker and restart them one by one. Note that the older Scala consumer does not support the new message format introduced in 0.11, so to avoid the performance cost of down-conversion (or to take advantage of exactly once semantics), the newer Java consumer must be used.



**Additional Upgrade Notes:**

  1. If you are willing to accept downtime, you can simply take all the brokers down, update the code and start them back up. They will start with the new protocol by default.
  2. Bumping the protocol version and restarting can be done any time after the brokers are upgraded. It does not have to be immediately after. Similarly for the message format version.
  3. If you are using Java8 method references in your Kafka Streams code you might need to update your code to resolve method ambiguities. Hot-swapping the jar-file only might not work.
  4. ACLs should not be added to prefixed resources, (added in [KIP-290](https://cwiki.apache.org/confluence/display/KAFKA/KIP-290%3A+Support+for+Prefixed+ACLs)), until all brokers in the cluster have been updated. 

**NOTE:** any prefixed ACLs added to a cluster, even after the cluster is fully upgraded, will be ignored should the cluster be downgraded again. 



### Notable changes in 2.0.0

  * [KIP-186](https://cwiki.apache.org/confluence/x/oYtjB) increases the default offset retention time from 1 day to 7 days. This makes it less likely to "lose" offsets in an application that commits infrequently. It also increases the active set of offsets and therefore can increase memory usage on the broker. Note that the console consumer currently enables offset commit by default and can be the source of a large number of offsets which this change will now preserve for 7 days instead of 1. You can preserve the existing behavior by setting the broker config `offsets.retention.minutes` to 1440.
  * Support for Java 7 has been dropped, Java 8 is now the minimum version required.
  * The default value for `ssl.endpoint.identification.algorithm` was changed to `https`, which performs hostname verification (man-in-the-middle attacks are possible otherwise). Set `ssl.endpoint.identification.algorithm` to an empty string to restore the previous behaviour. 
  * [KAFKA-5674](https://issues.apache.org/jira/browse/KAFKA-5674) extends the lower interval of `max.connections.per.ip minimum` to zero and therefore allows IP-based filtering of inbound connections.
  * [KIP-272](https://cwiki.apache.org/confluence/display/KAFKA/KIP-272%3A+Add+API+version+tag+to+broker%27s+RequestsPerSec+metric) added API version tag to the metric `kafka.network:type=RequestMetrics,name=RequestsPerSec,request={Produce|FetchConsumer|FetchFollower|...}`. This metric now becomes `kafka.network:type=RequestMetrics,name=RequestsPerSec,request={Produce|FetchConsumer|FetchFollower|...},version={0|1|2|3|...}`. This will impact JMX monitoring tools that do not automatically aggregate. To get the total count for a specific request type, the tool needs to be updated to aggregate across different versions. 
  * [KIP-225](https://cwiki.apache.org/confluence/x/uaBzB) changed the metric "records.lag" to use tags for topic and partition. The original version with the name format "{topic}-{partition}.records-lag" has been removed.
  * The Scala consumers, which have been deprecated since 0.11.0.0, have been removed. The Java consumer has been the recommended option since 0.10.0.0. Note that the Scala consumers in 1.1.0 (and older) will continue to work even if the brokers are upgraded to 2.0.0.
  * The Scala producers, which have been deprecated since 0.10.0.0, have been removed. The Java producer has been the recommended option since 0.9.0.0. Note that the behaviour of the default partitioner in the Java producer differs from the default partitioner in the Scala producers. Users migrating should consider configuring a custom partitioner that retains the previous behaviour. Note that the Scala producers in 1.1.0 (and older) will continue to work even if the brokers are upgraded to 2.0.0.
  * MirrorMaker and ConsoleConsumer no longer support the Scala consumer, they always use the Java consumer.
  * The ConsoleProducer no longer supports the Scala producer, it always uses the Java producer.
  * A number of deprecated tools that rely on the Scala clients have been removed: ReplayLogProducer, SimpleConsumerPerformance, SimpleConsumerShell, ExportZkOffsets, ImportZkOffsets, UpdateOffsetsInZK, VerifyConsumerRebalance.
  * The deprecated kafka.tools.ProducerPerformance has been removed, please use org.apache.kafka.tools.ProducerPerformance.
  * New Kafka Streams configuration parameter `upgrade.from` added that allows rolling bounce upgrade from older version. 
  * [KIP-284](https://cwiki.apache.org/confluence/x/DVyHB) changed the retention time for Kafka Streams repartition topics by setting its default value to `Long.MAX_VALUE`.
  * Updated `ProcessorStateManager` APIs in Kafka Streams for registering state stores to the processor topology. For more details please read the Streams [Upgrade Guide](/21/streams/upgrade-guide#streams_api_changes_200).
  * In earlier releases, Connect's worker configuration required the `internal.key.converter` and `internal.value.converter` properties. In 2.0, these are [no longer required](https://cwiki.apache.org/confluence/x/AZQ7B) and default to the JSON converter. You may safely remove these properties from your Connect standalone and distributed worker configurations:  
`internal.key.converter=org.apache.kafka.connect.json.JsonConverter` `internal.key.converter.schemas.enable=false` `internal.value.converter=org.apache.kafka.connect.json.JsonConverter` `internal.value.converter.schemas.enable=false`
  * [KIP-266](https://cwiki.apache.org/confluence/x/5kiHB) adds a new consumer configuration `default.api.timeout.ms` to specify the default timeout to use for `KafkaConsumer` APIs that could block. The KIP also adds overloads for such blocking APIs to support specifying a specific timeout to use for each of them instead of using the default timeout set by `default.api.timeout.ms`. In particular, a new `poll(Duration)` API has been added which does not block for dynamic partition assignment. The old `poll(long)` API has been deprecated and will be removed in a future version. Overloads have also been added for other `KafkaConsumer` methods like `partitionsFor`, `listTopics`, `offsetsForTimes`, `beginningOffsets`, `endOffsets` and `close` that take in a `Duration`.
  * Also as part of KIP-266, the default value of `request.timeout.ms` has been changed to 30 seconds. The previous value was a little higher than 5 minutes to account for maximum time that a rebalance would take. Now we treat the JoinGroup request in the rebalance as a special case and use a value derived from `max.poll.interval.ms` for the request timeout. All other request types use the timeout defined by `request.timeout.ms`
  * The internal method `kafka.admin.AdminClient.deleteRecordsBefore` has been removed. Users are encouraged to migrate to `org.apache.kafka.clients.admin.AdminClient.deleteRecords`.
  * The AclCommand tool `--producer` convenience option uses the [KIP-277](https://cwiki.apache.org/confluence/display/KAFKA/KIP-277+-+Fine+Grained+ACL+for+CreateTopics+API) finer grained ACL on the given topic. 
  * [KIP-176](https://cwiki.apache.org/confluence/display/KAFKA/KIP-176%3A+Remove+deprecated+new-consumer+option+for+tools) removes the `--new-consumer` option for all consumer based tools. This option is redundant since the new consumer is automatically used if --bootstrap-server is defined. 
  * [KIP-290](https://cwiki.apache.org/confluence/display/KAFKA/KIP-290%3A+Support+for+Prefixed+ACLs) adds the ability to define ACLs on prefixed resources, e.g. any topic starting with 'foo'.
  * [KIP-283](https://cwiki.apache.org/confluence/display/KAFKA/KIP-283%3A+Efficient+Memory+Usage+for+Down-Conversion) improves message down-conversion handling on Kafka broker, which has typically been a memory-intensive operation. The KIP adds a mechanism by which the operation becomes less memory intensive by down-converting chunks of partition data at a time which helps put an upper bound on memory consumption. With this improvement, there is a change in `FetchResponse` protocol behavior where the broker could send an oversized message batch towards the end of the response with an invalid offset. Such oversized messages must be ignored by consumer clients, as is done by `KafkaConsumer`. 

KIP-283 also adds new topic and broker configurations `message.downconversion.enable` and `log.message.downconversion.enable` respectively to control whether down-conversion is enabled. When disabled, broker does not perform any down-conversion and instead sends an `UNSUPPORTED_VERSION` error to the client.

  * Dynamic broker configuration options can be stored in ZooKeeper using kafka-configs.sh before brokers are started. This option can be used to avoid storing clear passwords in server.properties as all password configs may be stored encrypted in ZooKeeper.
  * ZooKeeper hosts are now re-resolved if connection attempt fails. But if your ZooKeeper host names resolve to multiple addresses and some of them are not reachable, then you may need to increase the connection timeout `zookeeper.connection.timeout.ms`.



### New Protocol Versions

  * [KIP-279](https://cwiki.apache.org/confluence/display/KAFKA/KIP-279%3A+Fix+log+divergence+between+leader+and+follower+after+fast+leader+fail+over): OffsetsForLeaderEpochResponse v1 introduces a partition-level `leader_epoch` field. 
  * [KIP-219](https://cwiki.apache.org/confluence/display/KAFKA/KIP-219+-+Improve+quota+communication): Bump up the protocol versions of non-cluster action requests and responses that are throttled on quota violation.
  * [KIP-290](https://cwiki.apache.org/confluence/display/KAFKA/KIP-290%3A+Support+for+Prefixed+ACLs): Bump up the protocol versions ACL create, describe and delete requests and responses.



### Upgrading a 1.1 Kafka Streams Application

  * Upgrading your Streams application from 1.1 to 2.0 does not require a broker upgrade. A Kafka Streams 2.0 application can connect to 2.0, 1.1, 1.0, 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * Note that in 2.0 we have removed the public APIs that are deprecated prior to 1.0; users leveraging on those deprecated APIs need to make code changes accordingly. See [Streams API changes in 2.0.0](/21/streams/upgrade-guide#streams_api_changes_200) for more details. 



## Upgrading from 0.8.x, 0.9.x, 0.10.0.x, 0.10.1.x, 0.10.2.x, 0.11.0.x, or 1.0.x to 1.1.x

Kafka 1.1.0 introduces wire protocol changes. By following the recommended rolling upgrade plan below, you guarantee no downtime during the upgrade. However, please review the notable changes in 1.1.0 before upgrading. 

**For a rolling upgrade:**

  1. Update server.properties on all brokers and add the following properties. CURRENT_KAFKA_VERSION refers to the version you are upgrading from. CURRENT_MESSAGE_FORMAT_VERSION refers to the message format version currently in use. If you have previously overridden the message format version, you should keep its current value. Alternatively, if you are upgrading from a version prior to 0.11.0.x, then CURRENT_MESSAGE_FORMAT_VERSION should be set to match CURRENT_KAFKA_VERSION. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2, 0.9.0, 0.10.0, 0.10.1, 0.10.2, 0.11.0, 1.0).
     * log.message.format.version=CURRENT_MESSAGE_FORMAT_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.)
If you are upgrading from 0.11.0.x or 1.0.x and you have not overridden the message format, then you only need to override the inter-broker protocol format. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (0.11.0 or 1.0).
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing `inter.broker.protocol.version` and setting it to 1.1. 
  4. Restart the brokers one by one for the new protocol version to take effect. 
  5. If you have overridden the message format version as instructed above, then you need to do one more rolling restart to upgrade it to its latest version. Once all (or most) consumers have been upgraded to 0.11.0 or later, change log.message.format.version to 1.1 on each broker and restart them one by one. Note that the older Scala consumer does not support the new message format introduced in 0.11, so to avoid the performance cost of down-conversion (or to take advantage of exactly once semantics), the newer Java consumer must be used.



**Additional Upgrade Notes:**

  1. If you are willing to accept downtime, you can simply take all the brokers down, update the code and start them back up. They will start with the new protocol by default.
  2. Bumping the protocol version and restarting can be done any time after the brokers are upgraded. It does not have to be immediately after. Similarly for the message format version.
  3. If you are using Java8 method references in your Kafka Streams code you might need to update your code to resolve method ambiguties. Hot-swapping the jar-file only might not work.



### Notable changes in 1.1.1

  * New Kafka Streams configuration parameter `upgrade.from` added that allows rolling bounce upgrade from version 0.10.0.x 
  * See the [**Kafka Streams upgrade guide**](/21/streams/upgrade-guide.html) for details about this new config. 


### Notable changes in 1.1.0

  * The kafka artifact in Maven no longer depends on log4j or slf4j-log4j12. Similarly to the kafka-clients artifact, users can now choose the logging back-end by including the appropriate slf4j module (slf4j-log4j12, logback, etc.). The release tarball still includes log4j and slf4j-log4j12.
  * [KIP-225](https://cwiki.apache.org/confluence/x/uaBzB) changed the metric "records.lag" to use tags for topic and partition. The original version with the name format "{topic}-{partition}.records-lag" is deprecated and will be removed in 2.0.0.
  * Kafka Streams is more robust against broker communication errors. Instead of stopping the Kafka Streams client with a fatal exception, Kafka Streams tries to self-heal and reconnect to the cluster. Using the new `AdminClient` you have better control of how often Kafka Streams retries and can [configure](/21/streams/developer-guide/config-streams) fine-grained timeouts (instead of hard coded retries as in older version).
  * Kafka Streams rebalance time was reduced further making Kafka Streams more responsive.
  * Kafka Connect now supports message headers in both sink and source connectors, and to manipulate them via simple message transforms. Connectors must be changed to explicitly use them. A new `HeaderConverter` is introduced to control how headers are (de)serialized, and the new "SimpleHeaderConverter" is used by default to use string representations of values.
  * kafka.tools.DumpLogSegments now automatically sets deep-iteration option if print-data-log is enabled explicitly or implicitly due to any of the other options like decoder.



### New Protocol Versions

  * [KIP-226](https://cwiki.apache.org/confluence/display/KAFKA/KIP-226+-+Dynamic+Broker+Configuration) introduced DescribeConfigs Request/Response v1.
  * [KIP-227](https://cwiki.apache.org/confluence/display/KAFKA/KIP-227%3A+Introduce+Incremental+FetchRequests+to+Increase+Partition+Scalability) introduced Fetch Request/Response v7.



### Upgrading a 1.0 Kafka Streams Application

  * Upgrading your Streams application from 1.0 to 1.1 does not require a broker upgrade. A Kafka Streams 1.1 application can connect to 1.0, 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * See [Streams API changes in 1.1.0](/21/streams/upgrade-guide#streams_api_changes_110) for more details. 



## Upgrading from 0.8.x, 0.9.x, 0.10.0.x, 0.10.1.x, 0.10.2.x or 0.11.0.x to 1.0.0

Kafka 1.0.0 introduces wire protocol changes. By following the recommended rolling upgrade plan below, you guarantee no downtime during the upgrade. However, please review the notable changes in 1.0.0 before upgrading. 

**For a rolling upgrade:**

  1. Update server.properties on all brokers and add the following properties. CURRENT_KAFKA_VERSION refers to the version you are upgrading from. CURRENT_MESSAGE_FORMAT_VERSION refers to the message format version currently in use. If you have previously overridden the message format version, you should keep its current value. Alternatively, if you are upgrading from a version prior to 0.11.0.x, then CURRENT_MESSAGE_FORMAT_VERSION should be set to match CURRENT_KAFKA_VERSION. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2, 0.9.0, 0.10.0, 0.10.1, 0.10.2, 0.11.0).
     * log.message.format.version=CURRENT_MESSAGE_FORMAT_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.)
If you are upgrading from 0.11.0.x and you have not overridden the message format, you must set both the message format version and the inter-broker protocol version to 0.11.0. 
     * inter.broker.protocol.version=0.11.0
     * log.message.format.version=0.11.0
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing `inter.broker.protocol.version` and setting it to 1.0. 
  4. Restart the brokers one by one for the new protocol version to take effect. 
  5. If you have overridden the message format version as instructed above, then you need to do one more rolling restart to upgrade it to its latest version. Once all (or most) consumers have been upgraded to 0.11.0 or later, change log.message.format.version to 1.0 on each broker and restart them one by one. If you are upgrading from 0.11.0 and log.message.format.version is set to 0.11.0, you can update the config and skip the rolling restart. Note that the older Scala consumer does not support the new message format introduced in 0.11, so to avoid the performance cost of down-conversion (or to take advantage of exactly once semantics), the newer Java consumer must be used.



**Additional Upgrade Notes:**

  1. If you are willing to accept downtime, you can simply take all the brokers down, update the code and start them back up. They will start with the new protocol by default.
  2. Bumping the protocol version and restarting can be done any time after the brokers are upgraded. It does not have to be immediately after. Similarly for the message format version.



### Notable changes in 1.0.2

  * New Kafka Streams configuration parameter `upgrade.from` added that allows rolling bounce upgrade from version 0.10.0.x 
  * See the [**Kafka Streams upgrade guide**](/21/streams/upgrade-guide.html) for details about this new config. 


### Notable changes in 1.0.1

  * Restored binary compatibility of AdminClient's Options classes (e.g. CreateTopicsOptions, DeleteTopicsOptions, etc.) with 0.11.0.x. Binary (but not source) compatibility had been broken inadvertently in 1.0.0.



### Notable changes in 1.0.0

  * Topic deletion is now enabled by default, since the functionality is now stable. Users who wish to to retain the previous behavior should set the broker config `delete.topic.enable` to `false`. Keep in mind that topic deletion removes data and the operation is not reversible (i.e. there is no "undelete" operation)
  * For topics that support timestamp search if no offset can be found for a partition, that partition is now included in the search result with a null offset value. Previously, the partition was not included in the map. This change was made to make the search behavior consistent with the case of topics not supporting timestamp search. 
  * If the `inter.broker.protocol.version` is 1.0 or later, a broker will now stay online to serve replicas on live log directories even if there are offline log directories. A log directory may become offline due to IOException caused by hardware failure. Users need to monitor the per-broker metric `offlineLogDirectoryCount` to check whether there is offline log directory. 
  * Added KafkaStorageException which is a retriable exception. KafkaStorageException will be converted to NotLeaderForPartitionException in the response if the version of client's FetchRequest or ProducerRequest does not support KafkaStorageException. 
  * -XX:+DisableExplicitGC was replaced by -XX:+ExplicitGCInvokesConcurrent in the default JVM settings. This helps avoid out of memory exceptions during allocation of native memory by direct buffers in some cases.
  * The overridden `handleError` method implementations have been removed from the following deprecated classes in the `kafka.api` package: `FetchRequest`, `GroupCoordinatorRequest`, `OffsetCommitRequest`, `OffsetFetchRequest`, `OffsetRequest`, `ProducerRequest`, and `TopicMetadataRequest`. This was only intended for use on the broker, but it is no longer in use and the implementations have not been maintained. A stub implementation has been retained for binary compatibility.
  * The Java clients and tools now accept any string as a client-id.
  * The deprecated tool `kafka-consumer-offset-checker.sh` has been removed. Use `kafka-consumer-groups.sh` to get consumer group details.
  * SimpleAclAuthorizer now logs access denials to the authorizer log by default.
  * Authentication failures are now reported to clients as one of the subclasses of `AuthenticationException`. No retries will be performed if a client connection fails authentication.
  * Custom `SaslServer` implementations may throw `SaslAuthenticationException` to provide an error message to return to clients indicating the reason for authentication failure. Implementors should take care not to include any security-critical information in the exception message that should not be leaked to unauthenticated clients.
  * The `app-info` mbean registered with JMX to provide version and commit id will be deprecated and replaced with metrics providing these attributes.
  * Kafka metrics may now contain non-numeric values. `org.apache.kafka.common.Metric#value()` has been deprecated and will return `0.0` in such cases to minimise the probability of breaking users who read the value of every client metric (via a `MetricsReporter` implementation or by calling the `metrics()` method). `org.apache.kafka.common.Metric#metricValue()` can be used to retrieve numeric and non-numeric metric values.
  * Every Kafka rate metric now has a corresponding cumulative count metric with the suffix `-total` to simplify downstream processing. For example, `records-consumed-rate` has a corresponding metric named `records-consumed-total`.
  * Mx4j will only be enabled if the system property `kafka_mx4jenable` is set to `true`. Due to a logic inversion bug, it was previously enabled by default and disabled if `kafka_mx4jenable` was set to `true`.
  * The package `org.apache.kafka.common.security.auth` in the clients jar has been made public and added to the javadocs. Internal classes which had previously been located in this package have been moved elsewhere.
  * When using an Authorizer and a user doesn't have required permissions on a topic, the broker will return TOPIC_AUTHORIZATION_FAILED errors to requests irrespective of topic existence on broker. If the user have required permissions and the topic doesn't exists, then the UNKNOWN_TOPIC_OR_PARTITION error code will be returned. 
  * config/consumer.properties file updated to use new consumer config properties.



### New Protocol Versions

  * [KIP-112](https://cwiki.apache.org/confluence/display/KAFKA/KIP-112%3A+Handle+disk+failure+for+JBOD): LeaderAndIsrRequest v1 introduces a partition-level `is_new` field. 
  * [KIP-112](https://cwiki.apache.org/confluence/display/KAFKA/KIP-112%3A+Handle+disk+failure+for+JBOD): UpdateMetadataRequest v4 introduces a partition-level `offline_replicas` field. 
  * [KIP-112](https://cwiki.apache.org/confluence/display/KAFKA/KIP-112%3A+Handle+disk+failure+for+JBOD): MetadataResponse v5 introduces a partition-level `offline_replicas` field. 
  * [KIP-112](https://cwiki.apache.org/confluence/display/KAFKA/KIP-112%3A+Handle+disk+failure+for+JBOD): ProduceResponse v4 introduces error code for KafkaStorageException. 
  * [KIP-112](https://cwiki.apache.org/confluence/display/KAFKA/KIP-112%3A+Handle+disk+failure+for+JBOD): FetchResponse v6 introduces error code for KafkaStorageException. 
  * [KIP-152](https://cwiki.apache.org/confluence/display/KAFKA/KIP-152+-+Improve+diagnostics+for+SASL+authentication+failures): SaslAuthenticate request has been added to enable reporting of authentication failures. This request will be used if the SaslHandshake request version is greater than 0. 



### Upgrading a 0.11.0 Kafka Streams Application

  * Upgrading your Streams application from 0.11.0 to 1.0 does not require a broker upgrade. A Kafka Streams 1.0 application can connect to 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). However, Kafka Streams 1.0 requires 0.10 message format or newer and does not work with older message formats. 
  * If you are monitoring on streams metrics, you will need make some changes to the metrics names in your reporting and monitoring code, because the metrics sensor hierarchy was changed. 
  * There are a few public APIs including `ProcessorContext#schedule()`, `Processor#punctuate()` and `KStreamBuilder`, `TopologyBuilder` are being deprecated by new APIs. We recommend making corresponding code changes, which should be very minor since the new APIs look quite similar, when you upgrade. 
  * See [Streams API changes in 1.0.0](/21/streams/upgrade-guide#streams_api_changes_100) for more details. 



### Upgrading a 0.10.2 Kafka Streams Application

  * Upgrading your Streams application from 0.10.2 to 1.0 does not require a broker upgrade. A Kafka Streams 1.0 application can connect to 1.0, 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * If you are monitoring on streams metrics, you will need make some changes to the metrics names in your reporting and monitoring code, because the metrics sensor hierarchy was changed. 
  * There are a few public APIs including `ProcessorContext#schedule()`, `Processor#punctuate()` and `KStreamBuilder`, `TopologyBuilder` are being deprecated by new APIs. We recommend making corresponding code changes, which should be very minor since the new APIs look quite similar, when you upgrade. 
  * If you specify customized `key.serde`, `value.serde` and `timestamp.extractor` in configs, it is recommended to use their replaced configure parameter as these configs are deprecated. 
  * See [Streams API changes in 0.11.0](/21/streams/upgrade-guide#streams_api_changes_0110) for more details. 



### Upgrading a 0.10.1 Kafka Streams Application

  * Upgrading your Streams application from 0.10.1 to 1.0 does not require a broker upgrade. A Kafka Streams 1.0 application can connect to 1.0, 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * You need to recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * If you are monitoring on streams metrics, you will need make some changes to the metrics names in your reporting and monitoring code, because the metrics sensor hierarchy was changed. 
  * There are a few public APIs including `ProcessorContext#schedule()`, `Processor#punctuate()` and `KStreamBuilder`, `TopologyBuilder` are being deprecated by new APIs. We recommend making corresponding code changes, which should be very minor since the new APIs look quite similar, when you upgrade. 
  * If you specify customized `key.serde`, `value.serde` and `timestamp.extractor` in configs, it is recommended to use their replaced configure parameter as these configs are deprecated. 
  * If you use a custom (i.e., user implemented) timestamp extractor, you will need to update this code, because the `TimestampExtractor` interface was changed. 
  * If you register custom metrics, you will need to update this code, because the `StreamsMetric` interface was changed. 
  * See [Streams API changes in 1.0.0](/21/streams/upgrade-guide#streams_api_changes_100), [Streams API changes in 0.11.0](/21/streams/upgrade-guide#streams_api_changes_0110) and [Streams API changes in 0.10.2](/21/streams/upgrade-guide#streams_api_changes_0102) for more details. 



### Upgrading a 0.10.0 Kafka Streams Application

  * Upgrading your Streams application from 0.10.0 to 1.0 does require a broker upgrade because a Kafka Streams 1.0 application can only connect to 0.1, 0.11.0, 0.10.2, or 0.10.1 brokers. 
  * There are couple of API changes, that are not backward compatible (cf. [Streams API changes in 1.0.0](/21/streams/upgrade-guide#streams_api_changes_100), [Streams API changes in 0.11.0](/21/streams#streams_api_changes_0110), [Streams API changes in 0.10.2](/21/streams#streams_api_changes_0102), and [Streams API changes in 0.10.1](/21/streams#streams_api_changes_0101) for more details). Thus, you need to update and recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * Upgrading from 0.10.0.x to 1.0.2 requires two rolling bounces with config `upgrade.from="0.10.0"` set for first upgrade phase (cf. [KIP-268](https://cwiki.apache.org/confluence/display/KAFKA/KIP-268%3A+Simplify+Kafka+Streams+Rebalance+Metadata+Upgrade)). As an alternative, an offline upgrade is also possible. 
    * prepare your application instances for a rolling bounce and make sure that config `upgrade.from` is set to `"0.10.0"` for new version 0.11.0.3 
    * bounce each instance of your application once 
    * prepare your newly deployed 1.0.2 application instances for a second round of rolling bounces; make sure to remove the value for config `upgrade.mode`
    * bounce each instance of your application once more to complete the upgrade 
  * Upgrading from 0.10.0.x to 1.0.0 or 1.0.1 requires an offline upgrade (rolling bounce upgrade is not supported) 
    * stop all old (0.10.0.x) application instances 
    * update your code and swap old code and jar file with new code and new jar file 
    * restart all new (1.0.0 or 1.0.1) application instances 



## Upgrading from 0.8.x, 0.9.x, 0.10.0.x, 0.10.1.x or 0.10.2.x to 0.11.0.0

Kafka 0.11.0.0 introduces a new message format version as well as wire protocol changes. By following the recommended rolling upgrade plan below, you guarantee no downtime during the upgrade. However, please review the notable changes in 0.11.0.0 before upgrading. 

Starting with version 0.10.2, Java clients (producer and consumer) have acquired the ability to communicate with older brokers. Version 0.11.0 clients can talk to version 0.10.0 or newer brokers. However, if your brokers are older than 0.10.0, you must upgrade all the brokers in the Kafka cluster before upgrading your clients. Version 0.11.0 brokers support 0.8.x and newer clients. 

**For a rolling upgrade:**

  1. Update server.properties on all brokers and add the following properties. CURRENT_KAFKA_VERSION refers to the version you are upgrading from. CURRENT_MESSAGE_FORMAT_VERSION refers to the current message format version currently in use. If you have not overridden the message format previously, then CURRENT_MESSAGE_FORMAT_VERSION should be set to match CURRENT_KAFKA_VERSION. 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2, 0.9.0, 0.10.0, 0.10.1 or 0.10.2).
     * log.message.format.version=CURRENT_MESSAGE_FORMAT_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.)
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing `inter.broker.protocol.version` and setting it to 0.11.0, but do not change `log.message.format.version` yet. 
  4. Restart the brokers one by one for the new protocol version to take effect. 
  5. Once all (or most) consumers have been upgraded to 0.11.0 or later, then change log.message.format.version to 0.11.0 on each broker and restart them one by one. Note that the older Scala consumer does not support the new message format, so to avoid the performance cost of down-conversion (or to take advantage of exactly once semantics), the new Java consumer must be used.



**Additional Upgrade Notes:**

  1. If you are willing to accept downtime, you can simply take all the brokers down, update the code and start them back up. They will start with the new protocol by default.
  2. Bumping the protocol version and restarting can be done any time after the brokers are upgraded. It does not have to be immediately after. Similarly for the message format version.
  3. It is also possible to enable the 0.11.0 message format on individual topics using the topic admin tool (`bin/kafka-topics.sh`) prior to updating the global setting `log.message.format.version`.
  4. If you are upgrading from a version prior to 0.10.0, it is NOT necessary to first update the message format to 0.10.0 before you switch to 0.11.0.



### Upgrading a 0.10.2 Kafka Streams Application

  * Upgrading your Streams application from 0.10.2 to 0.11.0 does not require a broker upgrade. A Kafka Streams 0.11.0 application can connect to 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * If you specify customized `key.serde`, `value.serde` and `timestamp.extractor` in configs, it is recommended to use their replaced configure parameter as these configs are deprecated. 
  * See [Streams API changes in 0.11.0](/21/streams/upgrade-guide#streams_api_changes_0110) for more details. 



### Upgrading a 0.10.1 Kafka Streams Application

  * Upgrading your Streams application from 0.10.1 to 0.11.0 does not require a broker upgrade. A Kafka Streams 0.11.0 application can connect to 0.11.0, 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * You need to recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * If you specify customized `key.serde`, `value.serde` and `timestamp.extractor` in configs, it is recommended to use their replaced configure parameter as these configs are deprecated. 
  * If you use a custom (i.e., user implemented) timestamp extractor, you will need to update this code, because the `TimestampExtractor` interface was changed. 
  * If you register custom metrics, you will need to update this code, because the `StreamsMetric` interface was changed. 
  * See [Streams API changes in 0.11.0](/21/streams/upgrade-guide#streams_api_changes_0110) and [Streams API changes in 0.10.2](/21/streams/upgrade-guide#streams_api_changes_0102) for more details. 



### Upgrading a 0.10.0 Kafka Streams Application

  * Upgrading your Streams application from 0.10.0 to 0.11.0 does require a broker upgrade because a Kafka Streams 0.11.0 application can only connect to 0.11.0, 0.10.2, or 0.10.1 brokers. 
  * There are couple of API changes, that are not backward compatible (cf. [Streams API changes in 0.11.0](/21/streams#streams_api_changes_0110), [Streams API changes in 0.10.2](/21/streams#streams_api_changes_0102), and [Streams API changes in 0.10.1](/21/streams#streams_api_changes_0101) for more details). Thus, you need to update and recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * Upgrading from 0.10.0.x to 0.11.0.3 requires two rolling bounces with config `upgrade.from="0.10.0"` set for first upgrade phase (cf. [KIP-268](https://cwiki.apache.org/confluence/display/KAFKA/KIP-268%3A+Simplify+Kafka+Streams+Rebalance+Metadata+Upgrade)). As an alternative, an offline upgrade is also possible. 
    * prepare your application instances for a rolling bounce and make sure that config `upgrade.from` is set to `"0.10.0"` for new version 0.11.0.3 
    * bounce each instance of your application once 
    * prepare your newly deployed 0.11.0.3 application instances for a second round of rolling bounces; make sure to remove the value for config `upgrade.mode`
    * bounce each instance of your application once more to complete the upgrade 
  * Upgrading from 0.10.0.x to 0.11.0.0, 0.11.0.1, or 0.11.0.2 requires an offline upgrade (rolling bounce upgrade is not supported) 
    * stop all old (0.10.0.x) application instances 
    * update your code and swap old code and jar file with new code and new jar file 
    * restart all new (0.11.0.0 , 0.11.0.1, or 0.11.0.2) application instances 



### Notable changes in 0.11.0.3

  * New Kafka Streams configuration parameter `upgrade.from` added that allows rolling bounce upgrade from version 0.10.0.x 
  * See the [**Kafka Streams upgrade guide**](/21/streams/upgrade-guide.html) for details about this new config. 


### Notable changes in 0.11.0.0

  * Unclean leader election is now disabled by default. The new default favors durability over availability. Users who wish to to retain the previous behavior should set the broker config `unclean.leader.election.enable` to `true`.
  * Producer configs `block.on.buffer.full`, `metadata.fetch.timeout.ms` and `timeout.ms` have been removed. They were initially deprecated in Kafka 0.9.0.0.
  * The `offsets.topic.replication.factor` broker config is now enforced upon auto topic creation. Internal auto topic creation will fail with a GROUP_COORDINATOR_NOT_AVAILABLE error until the cluster size meets this replication factor requirement.
  * When compressing data with snappy, the producer and broker will use the compression scheme's default block size (2 x 32 KB) instead of 1 KB in order to improve the compression ratio. There have been reports of data compressed with the smaller block size being 50% larger than when compressed with the larger block size. For the snappy case, a producer with 5000 partitions will require an additional 315 MB of JVM heap.
  * Similarly, when compressing data with gzip, the producer and broker will use 8 KB instead of 1 KB as the buffer size. The default for gzip is excessively low (512 bytes). 
  * The broker configuration `max.message.bytes` now applies to the total size of a batch of messages. Previously the setting applied to batches of compressed messages, or to non-compressed messages individually. A message batch may consist of only a single message, so in most cases, the limitation on the size of individual messages is only reduced by the overhead of the batch format. However, there are some subtle implications for message format conversion (see below for more detail). Note also that while previously the broker would ensure that at least one message is returned in each fetch request (regardless of the total and partition-level fetch sizes), the same behavior now applies to one message batch.
  * GC log rotation is enabled by default, see KAFKA-3754 for details.
  * Deprecated constructors of RecordMetadata, MetricName and Cluster classes have been removed.
  * Added user headers support through a new Headers interface providing user headers read and write access.
  * ProducerRecord and ConsumerRecord expose the new Headers API via `Headers headers()` method call.
  * ExtendedSerializer and ExtendedDeserializer interfaces are introduced to support serialization and deserialization for headers. Headers will be ignored if the configured serializer and deserializer are not the above classes.
  * A new config, `group.initial.rebalance.delay.ms`, was introduced. This config specifies the time, in milliseconds, that the `GroupCoordinator` will delay the initial consumer rebalance. The rebalance will be further delayed by the value of `group.initial.rebalance.delay.ms` as new members join the group, up to a maximum of `max.poll.interval.ms`. The default value for this is 3 seconds. During development and testing it might be desirable to set this to 0 in order to not delay test execution time. 
  * `org.apache.kafka.common.Cluster#partitionsForTopic`, `partitionsForNode` and `availablePartitionsForTopic` methods will return an empty list instead of `null` (which is considered a bad practice) in case the metadata for the required topic does not exist. 
  * Streams API configuration parameters `timestamp.extractor`, `key.serde`, and `value.serde` were deprecated and replaced by `default.timestamp.extractor`, `default.key.serde`, and `default.value.serde`, respectively. 
  * For offset commit failures in the Java consumer's `commitAsync` APIs, we no longer expose the underlying cause when instances of `RetriableCommitFailedException` are passed to the commit callback. See [KAFKA-5052](https://issues.apache.org/jira/browse/KAFKA-5052) for more detail. 



### New Protocol Versions

  * [KIP-107](https://cwiki.apache.org/confluence/display/KAFKA/KIP-107%3A+Add+purgeDataBefore\(\)+API+in+AdminClient): FetchRequest v5 introduces a partition-level `log_start_offset` field. 
  * [KIP-107](https://cwiki.apache.org/confluence/display/KAFKA/KIP-107%3A+Add+purgeDataBefore\(\)+API+in+AdminClient): FetchResponse v5 introduces a partition-level `log_start_offset` field. 
  * [KIP-82](https://cwiki.apache.org/confluence/display/KAFKA/KIP-82+-+Add+Record+Headers): ProduceRequest v3 introduces an array of `header` in the message protocol, containing `key` field and `value` field.
  * [KIP-82](https://cwiki.apache.org/confluence/display/KAFKA/KIP-82+-+Add+Record+Headers): FetchResponse v5 introduces an array of `header` in the message protocol, containing `key` field and `value` field.



### Notes on Exactly Once Semantics

Kafka 0.11.0 includes support for idempotent and transactional capabilities in the producer. Idempotent delivery ensures that messages are delivered exactly once to a particular topic partition during the lifetime of a single producer. Transactional delivery allows producers to send data to multiple partitions such that either all messages are successfully delivered, or none of them are. Together, these capabilities enable "exactly once semantics" in Kafka. More details on these features are available in the user guide, but below we add a few specific notes on enabling them in an upgraded cluster. Note that enabling EoS is not required and there is no impact on the broker's behavior if unused.

  1. Only the new Java producer and consumer support exactly once semantics.
  2. These features depend crucially on the 0.11.0 message format. Attempting to use them on an older format will result in unsupported version errors.
  3. Transaction state is stored in a new internal topic `__transaction_state`. This topic is not created until the the first attempt to use a transactional request API. Similar to the consumer offsets topic, there are several settings to control the topic's configuration. For example, `transaction.state.log.min.isr` controls the minimum ISR for this topic. See the configuration section in the user guide for a full list of options.
  4. For secure clusters, the transactional APIs require new ACLs which can be turned on with the `bin/kafka-acls.sh`. tool.
  5. EoS in Kafka introduces new request APIs and modifies several existing ones. See [KIP-98](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging#KIP-98-ExactlyOnceDeliveryandTransactionalMessaging-RPCProtocolSummary) for the full details



### Notes on the new message format in 0.11.0

The 0.11.0 message format includes several major enhancements in order to support better delivery semantics for the producer (see [KIP-98](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)) and improved replication fault tolerance (see [KIP-101](https://cwiki.apache.org/confluence/display/KAFKA/KIP-101+-+Alter+Replication+Protocol+to+use+Leader+Epoch+rather+than+High+Watermark+for+Truncation)). Although the new format contains more information to make these improvements possible, we have made the batch format much more efficient. As long as the number of messages per batch is more than 2, you can expect lower overall overhead. For smaller batches, however, there may be a small performance impact. See [here](bit.ly/kafka-eos-perf) for the results of our initial performance analysis of the new message format. You can also find more detail on the message format in the [KIP-98](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging#KIP-98-ExactlyOnceDeliveryandTransactionalMessaging-MessageFormat) proposal. 

One of the notable differences in the new message format is that even uncompressed messages are stored together as a single batch. This has a few implications for the broker configuration `max.message.bytes`, which limits the size of a single batch. First, if an older client produces messages to a topic partition using the old format, and the messages are individually smaller than `max.message.bytes`, the broker may still reject them after they are merged into a single batch during the up-conversion process. Generally this can happen when the aggregate size of the individual messages is larger than `max.message.bytes`. There is a similar effect for older consumers reading messages down-converted from the new format: if the fetch size is not set at least as large as `max.message.bytes`, the consumer may not be able to make progress even if the individual uncompressed messages are smaller than the configured fetch size. This behavior does not impact the Java client for 0.10.1.0 and later since it uses an updated fetch protocol which ensures that at least one message can be returned even if it exceeds the fetch size. To get around these problems, you should ensure 1) that the producer's batch size is not set larger than `max.message.bytes`, and 2) that the consumer's fetch size is set at least as large as `max.message.bytes`. 

Most of the discussion on the performance impact of upgrading to the 0.10.0 message format remains pertinent to the 0.11.0 upgrade. This mainly affects clusters that are not secured with TLS since "zero-copy" transfer is already not possible in that case. In order to avoid the cost of down-conversion, you should ensure that consumer applications are upgraded to the latest 0.11.0 client. Significantly, since the old consumer has been deprecated in 0.11.0.0, it does not support the new message format. You must upgrade to use the new consumer to use the new message format without the cost of down-conversion. Note that 0.11.0 consumers support backwards compatibility with 0.10.0 brokers and upward, so it is possible to upgrade the clients first before the brokers. 

## Upgrading from 0.8.x, 0.9.x, 0.10.0.x or 0.10.1.x to 0.10.2.0

0.10.2.0 has wire protocol changes. By following the recommended rolling upgrade plan below, you guarantee no downtime during the upgrade. However, please review the notable changes in 0.10.2.0 before upgrading. 

Starting with version 0.10.2, Java clients (producer and consumer) have acquired the ability to communicate with older brokers. Version 0.10.2 clients can talk to version 0.10.0 or newer brokers. However, if your brokers are older than 0.10.0, you must upgrade all the brokers in the Kafka cluster before upgrading your clients. Version 0.10.2 brokers support 0.8.x and newer clients. 

**For a rolling upgrade:**

  1. Update server.properties file on all brokers and add the following properties: 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2, 0.9.0, 0.10.0 or 0.10.1).
     * log.message.format.version=CURRENT_KAFKA_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.) 
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing inter.broker.protocol.version and setting it to 0.10.2. 
  4. If your previous message format is 0.10.0, change log.message.format.version to 0.10.2 (this is a no-op as the message format is the same for 0.10.0, 0.10.1 and 0.10.2). If your previous message format version is lower than 0.10.0, do not change log.message.format.version yet - this parameter should only change once all consumers have been upgraded to 0.10.0.0 or later.
  5. Restart the brokers one by one for the new protocol version to take effect. 
  6. If log.message.format.version is still lower than 0.10.0 at this point, wait until all consumers have been upgraded to 0.10.0 or later, then change log.message.format.version to 0.10.2 on each broker and restart them one by one. 



**Note:** If you are willing to accept downtime, you can simply take all the brokers down, update the code and start all of them. They will start with the new protocol by default. 

**Note:** Bumping the protocol version and restarting can be done any time after the brokers were upgraded. It does not have to be immediately after. 

### Upgrading a 0.10.1 Kafka Streams Application

  * Upgrading your Streams application from 0.10.1 to 0.10.2 does not require a broker upgrade. A Kafka Streams 0.10.2 application can connect to 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though). 
  * You need to recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * If you use a custom (i.e., user implemented) timestamp extractor, you will need to update this code, because the `TimestampExtractor` interface was changed. 
  * If you register custom metrics, you will need to update this code, because the `StreamsMetric` interface was changed. 
  * See [Streams API changes in 0.10.2](/21/streams/upgrade-guide#streams_api_changes_0102) for more details. 



### Upgrading a 0.10.0 Kafka Streams Application

  * Upgrading your Streams application from 0.10.0 to 0.10.2 does require a broker upgrade because a Kafka Streams 0.10.2 application can only connect to 0.10.2 or 0.10.1 brokers. 
  * There are couple of API changes, that are not backward compatible (cf. [Streams API changes in 0.10.2](/21/streams#streams_api_changes_0102) for more details). Thus, you need to update and recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * Upgrading from 0.10.0.x to 0.10.2.2 requires two rolling bounces with config `upgrade.from="0.10.0"` set for first upgrade phase (cf. [KIP-268](https://cwiki.apache.org/confluence/display/KAFKA/KIP-268%3A+Simplify+Kafka+Streams+Rebalance+Metadata+Upgrade)). As an alternative, an offline upgrade is also possible. 
    * prepare your application instances for a rolling bounce and make sure that config `upgrade.from` is set to `"0.10.0"` for new version 0.10.2.2 
    * bounce each instance of your application once 
    * prepare your newly deployed 0.10.2.2 application instances for a second round of rolling bounces; make sure to remove the value for config `upgrade.mode`
    * bounce each instance of your application once more to complete the upgrade 
  * Upgrading from 0.10.0.x to 0.10.2.0 or 0.10.2.1 requires an offline upgrade (rolling bounce upgrade is not supported) 
    * stop all old (0.10.0.x) application instances 
    * update your code and swap old code and jar file with new code and new jar file 
    * restart all new (0.10.2.0 or 0.10.2.1) application instances 



### Notable changes in 0.10.2.2

  * New configuration parameter `upgrade.from` added that allows rolling bounce upgrade from version 0.10.0.x 



### Notable changes in 0.10.2.1

  * The default values for two configurations of the StreamsConfig class were changed to improve the resiliency of Kafka Streams applications. The internal Kafka Streams producer `retries` default value was changed from 0 to 10. The internal Kafka Streams consumer `max.poll.interval.ms` default value was changed from 300000 to `Integer.MAX_VALUE`. 



### Notable changes in 0.10.2.0

  * The Java clients (producer and consumer) have acquired the ability to communicate with older brokers. Version 0.10.2 clients can talk to version 0.10.0 or newer brokers. Note that some features are not available or are limited when older brokers are used. 
  * Several methods on the Java consumer may now throw `InterruptException` if the calling thread is interrupted. Please refer to the `KafkaConsumer` Javadoc for a more in-depth explanation of this change.
  * Java consumer now shuts down gracefully. By default, the consumer waits up to 30 seconds to complete pending requests. A new close API with timeout has been added to `KafkaConsumer` to control the maximum wait time.
  * Multiple regular expressions separated by commas can be passed to MirrorMaker with the new Java consumer via the --whitelist option. This makes the behaviour consistent with MirrorMaker when used the old Scala consumer.
  * Upgrading your Streams application from 0.10.1 to 0.10.2 does not require a broker upgrade. A Kafka Streams 0.10.2 application can connect to 0.10.2 and 0.10.1 brokers (it is not possible to connect to 0.10.0 brokers though).
  * The Zookeeper dependency was removed from the Streams API. The Streams API now uses the Kafka protocol to manage internal topics instead of modifying Zookeeper directly. This eliminates the need for privileges to access Zookeeper directly and "StreamsConfig.ZOOKEEPER_CONFIG" should not be set in the Streams app any more. If the Kafka cluster is secured, Streams apps must have the required security privileges to create new topics.
  * Several new fields including "security.protocol", "connections.max.idle.ms", "retry.backoff.ms", "reconnect.backoff.ms" and "request.timeout.ms" were added to StreamsConfig class. User should pay attention to the default values and set these if needed. For more details please refer to [3.5 Kafka Streams Configs](/21/#streamsconfigs).



### New Protocol Versions

  * [KIP-88](https://cwiki.apache.org/confluence/display/KAFKA/KIP-88%3A+OffsetFetch+Protocol+Update): OffsetFetchRequest v2 supports retrieval of offsets for all topics if the `topics` array is set to `null`. 
  * [KIP-88](https://cwiki.apache.org/confluence/display/KAFKA/KIP-88%3A+OffsetFetch+Protocol+Update): OffsetFetchResponse v2 introduces a top-level `error_code` field. 
  * [KIP-103](https://cwiki.apache.org/confluence/display/KAFKA/KIP-103%3A+Separation+of+Internal+and+External+traffic): UpdateMetadataRequest v3 introduces a `listener_name` field to the elements of the `end_points` array. 
  * [KIP-108](https://cwiki.apache.org/confluence/display/KAFKA/KIP-108%3A+Create+Topic+Policy): CreateTopicsRequest v1 introduces a `validate_only` field. 
  * [KIP-108](https://cwiki.apache.org/confluence/display/KAFKA/KIP-108%3A+Create+Topic+Policy): CreateTopicsResponse v1 introduces an `error_message` field to the elements of the `topic_errors` array. 



## Upgrading from 0.8.x, 0.9.x or 0.10.0.X to 0.10.1.0

0.10.1.0 has wire protocol changes. By following the recommended rolling upgrade plan below, you guarantee no downtime during the upgrade. However, please notice the Potential breaking changes in 0.10.1.0 before upgrade.   
Note: Because new protocols are introduced, it is important to upgrade your Kafka clusters before upgrading your clients (i.e. 0.10.1.x clients only support 0.10.1.x or later brokers while 0.10.1.x brokers also support older clients). 

**For a rolling upgrade:**

  1. Update server.properties file on all brokers and add the following properties: 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2.0, 0.9.0.0 or 0.10.0.0).
     * log.message.format.version=CURRENT_KAFKA_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.) 
  2. Upgrade the brokers one at a time: shut down the broker, update the code, and restart it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing inter.broker.protocol.version and setting it to 0.10.1.0. 
  4. If your previous message format is 0.10.0, change log.message.format.version to 0.10.1 (this is a no-op as the message format is the same for both 0.10.0 and 0.10.1). If your previous message format version is lower than 0.10.0, do not change log.message.format.version yet - this parameter should only change once all consumers have been upgraded to 0.10.0.0 or later.
  5. Restart the brokers one by one for the new protocol version to take effect. 
  6. If log.message.format.version is still lower than 0.10.0 at this point, wait until all consumers have been upgraded to 0.10.0 or later, then change log.message.format.version to 0.10.1 on each broker and restart them one by one. 



**Note:** If you are willing to accept downtime, you can simply take all the brokers down, update the code and start all of them. They will start with the new protocol by default. 

**Note:** Bumping the protocol version and restarting can be done any time after the brokers were upgraded. It does not have to be immediately after. 

### Potential breaking changes in 0.10.1.0

  * The log retention time is no longer based on last modified time of the log segments. Instead it will be based on the largest timestamp of the messages in a log segment.
  * The log rolling time is no longer depending on log segment create time. Instead it is now based on the timestamp in the messages. More specifically. if the timestamp of the first message in the segment is T, the log will be rolled out when a new message has a timestamp greater than or equal to T + log.roll.ms 
  * The open file handlers of 0.10.0 will increase by ~33% because of the addition of time index files for each segment.
  * The time index and offset index share the same index size configuration. Since each time index entry is 1.5x the size of offset index entry. User may need to increase log.index.size.max.bytes to avoid potential frequent log rolling. 
  * Due to the increased number of index files, on some brokers with large amount the log segments (e.g. >15K), the log loading process during the broker startup could be longer. Based on our experiment, setting the num.recovery.threads.per.data.dir to one may reduce the log loading time. 



### Upgrading a 0.10.0 Kafka Streams Application

  * Upgrading your Streams application from 0.10.0 to 0.10.1 does require a broker upgrade because a Kafka Streams 0.10.1 application can only connect to 0.10.1 brokers. 
  * There are couple of API changes, that are not backward compatible (cf. [Streams API changes in 0.10.1](/21/streams/upgrade-guide#streams_api_changes_0101) for more details). Thus, you need to update and recompile your code. Just swapping the Kafka Streams library jar file will not work and will break your application. 
  * Upgrading from 0.10.0.x to 0.10.1.2 requires two rolling bounces with config `upgrade.from="0.10.0"` set for first upgrade phase (cf. [KIP-268](https://cwiki.apache.org/confluence/display/KAFKA/KIP-268%3A+Simplify+Kafka+Streams+Rebalance+Metadata+Upgrade)). As an alternative, an offline upgrade is also possible. 
    * prepare your application instances for a rolling bounce and make sure that config `upgrade.from` is set to `"0.10.0"` for new version 0.10.1.2 
    * bounce each instance of your application once 
    * prepare your newly deployed 0.10.1.2 application instances for a second round of rolling bounces; make sure to remove the value for config `upgrade.mode`
    * bounce each instance of your application once more to complete the upgrade 
  * Upgrading from 0.10.0.x to 0.10.1.0 or 0.10.1.1 requires an offline upgrade (rolling bounce upgrade is not supported) 
    * stop all old (0.10.0.x) application instances 
    * update your code and swap old code and jar file with new code and new jar file 
    * restart all new (0.10.1.0 or 0.10.1.1) application instances 



### Notable changes in 0.10.1.0

  * The new Java consumer is no longer in beta and we recommend it for all new development. The old Scala consumers are still supported, but they will be deprecated in the next release and will be removed in a future major release. 
  * The `--new-consumer`/`--new.consumer` switch is no longer required to use tools like MirrorMaker and the Console Consumer with the new consumer; one simply needs to pass a Kafka broker to connect to instead of the ZooKeeper ensemble. In addition, usage of the Console Consumer with the old consumer has been deprecated and it will be removed in a future major release. 
  * Kafka clusters can now be uniquely identified by a cluster id. It will be automatically generated when a broker is upgraded to 0.10.1.0. The cluster id is available via the kafka.server:type=KafkaServer,name=ClusterId metric and it is part of the Metadata response. Serializers, client interceptors and metric reporters can receive the cluster id by implementing the ClusterResourceListener interface. 
  * The BrokerState "RunningAsController" (value 4) has been removed. Due to a bug, a broker would only be in this state briefly before transitioning out of it and hence the impact of the removal should be minimal. The recommended way to detect if a given broker is the controller is via the kafka.controller:type=KafkaController,name=ActiveControllerCount metric. 
  * The new Java Consumer now allows users to search offsets by timestamp on partitions. 
  * The new Java Consumer now supports heartbeating from a background thread. There is a new configuration `max.poll.interval.ms` which controls the maximum time between poll invocations before the consumer will proactively leave the group (5 minutes by default). The value of the configuration `request.timeout.ms` must always be larger than `max.poll.interval.ms` because this is the maximum time that a JoinGroup request can block on the server while the consumer is rebalancing, so we have changed its default value to just above 5 minutes. Finally, the default value of `session.timeout.ms` has been adjusted down to 10 seconds, and the default value of `max.poll.records` has been changed to 500.
  * When using an Authorizer and a user doesn't have **Describe** authorization on a topic, the broker will no longer return TOPIC_AUTHORIZATION_FAILED errors to requests since this leaks topic names. Instead, the UNKNOWN_TOPIC_OR_PARTITION error code will be returned. This may cause unexpected timeouts or delays when using the producer and consumer since Kafka clients will typically retry automatically on unknown topic errors. You should consult the client logs if you suspect this could be happening.
  * Fetch responses have a size limit by default (50 MB for consumers and 10 MB for replication). The existing per partition limits also apply (1 MB for consumers and replication). Note that neither of these limits is an absolute maximum as explained in the next point. 
  * Consumers and replicas can make progress if a message larger than the response/partition size limit is found. More concretely, if the first message in the first non-empty partition of the fetch is larger than either or both limits, the message will still be returned. 
  * Overloaded constructors were added to `kafka.api.FetchRequest` and `kafka.javaapi.FetchRequest` to allow the caller to specify the order of the partitions (since order is significant in v3). The previously existing constructors were deprecated and the partitions are shuffled before the request is sent to avoid starvation issues. 



### New Protocol Versions

  * ListOffsetRequest v1 supports accurate offset search based on timestamps. 
  * MetadataResponse v2 introduces a new field: "cluster_id". 
  * FetchRequest v3 supports limiting the response size (in addition to the existing per partition limit), it returns messages bigger than the limits if required to make progress and the order of partitions in the request is now significant. 
  * JoinGroup v1 introduces a new field: "rebalance_timeout". 



## Upgrading from 0.8.x or 0.9.x to 0.10.0.0

0.10.0.0 has potential breaking changes (please review before upgrading) and possible  performance impact following the upgrade. By following the recommended rolling upgrade plan below, you guarantee no downtime and no performance impact during and following the upgrade.   
Note: Because new protocols are introduced, it is important to upgrade your Kafka clusters before upgrading your clients. 

**Notes to clients with version 0.9.0.0:** Due to a bug introduced in 0.9.0.0, clients that depend on ZooKeeper (old Scala high-level Consumer and MirrorMaker if used with the old consumer) will not work with 0.10.0.x brokers. Therefore, 0.9.0.0 clients should be upgraded to 0.9.0.1 **before** brokers are upgraded to 0.10.0.x. This step is not necessary for 0.8.X or 0.9.0.1 clients. 

**For a rolling upgrade:**

  1. Update server.properties file on all brokers and add the following properties: 
     * inter.broker.protocol.version=CURRENT_KAFKA_VERSION (e.g. 0.8.2 or 0.9.0.0).
     * log.message.format.version=CURRENT_KAFKA_VERSION (See potential performance impact following the upgrade for the details on what this configuration does.) 
  2. Upgrade the brokers. This can be done a broker at a time by simply bringing it down, updating the code, and restarting it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing inter.broker.protocol.version and setting it to 0.10.0.0. NOTE: You shouldn't touch log.message.format.version yet - this parameter should only change once all consumers have been upgraded to 0.10.0.0 
  4. Restart the brokers one by one for the new protocol version to take effect. 
  5. Once all consumers have been upgraded to 0.10.0, change log.message.format.version to 0.10.0 on each broker and restart them one by one. 



**Note:** If you are willing to accept downtime, you can simply take all the brokers down, update the code and start all of them. They will start with the new protocol by default. 

**Note:** Bumping the protocol version and restarting can be done any time after the brokers were upgraded. It does not have to be immediately after. 

### Potential performance impact following upgrade to 0.10.0.0

The message format in 0.10.0 includes a new timestamp field and uses relative offsets for compressed messages. The on disk message format can be configured through log.message.format.version in the server.properties file. The default on-disk message format is 0.10.0. If a consumer client is on a version before 0.10.0.0, it only understands message formats before 0.10.0. In this case, the broker is able to convert messages from the 0.10.0 format to an earlier format before sending the response to the consumer on an older version. However, the broker can't use zero-copy transfer in this case. Reports from the Kafka community on the performance impact have shown CPU utilization going from 20% before to 100% after an upgrade, which forced an immediate upgrade of all clients to bring performance back to normal. To avoid such message conversion before consumers are upgraded to 0.10.0.0, one can set log.message.format.version to 0.8.2 or 0.9.0 when upgrading the broker to 0.10.0.0. This way, the broker can still use zero-copy transfer to send the data to the old consumers. Once consumers are upgraded, one can change the message format to 0.10.0 on the broker and enjoy the new message format that includes new timestamp and improved compression. The conversion is supported to ensure compatibility and can be useful to support a few apps that have not updated to newer clients yet, but is impractical to support all consumer traffic on even an overprovisioned cluster. Therefore, it is critical to avoid the message conversion as much as possible when brokers have been upgraded but the majority of clients have not. 

For clients that are upgraded to 0.10.0.0, there is no performance impact. 

**Note:** By setting the message format version, one certifies that all existing messages are on or below that message format version. Otherwise consumers before 0.10.0.0 might break. In particular, after the message format is set to 0.10.0, one should not change it back to an earlier format as it may break consumers on versions before 0.10.0.0. 

**Note:** Due to the additional timestamp introduced in each message, producers sending small messages may see a message throughput degradation because of the increased overhead. Likewise, replication now transmits an additional 8 bytes per message. If you're running close to the network capacity of your cluster, it's possible that you'll overwhelm the network cards and see failures and performance issues due to the overload. 

**Note:** If you have enabled compression on producers, you may notice reduced producer throughput and/or lower compression rate on the broker in some cases. When receiving compressed messages, 0.10.0 brokers avoid recompressing the messages, which in general reduces the latency and improves the throughput. In certain cases, however, this may reduce the batching size on the producer, which could lead to worse throughput. If this happens, users can tune linger.ms and batch.size of the producer for better throughput. In addition, the producer buffer used for compressing messages with snappy is smaller than the one used by the broker, which may have a negative impact on the compression ratio for the messages on disk. We intend to make this configurable in a future Kafka release. 

### Potential breaking changes in 0.10.0.0

  * Starting from Kafka 0.10.0.0, the message format version in Kafka is represented as the Kafka version. For example, message format 0.9.0 refers to the highest message version supported by Kafka 0.9.0. 
  * Message format 0.10.0 has been introduced and it is used by default. It includes a timestamp field in the messages and relative offsets are used for compressed messages. 
  * ProduceRequest/Response v2 has been introduced and it is used by default to support message format 0.10.0 
  * FetchRequest/Response v2 has been introduced and it is used by default to support message format 0.10.0 
  * MessageFormatter interface was changed from `def writeTo(key: Array[Byte], value: Array[Byte], output: PrintStream)` to `def writeTo(consumerRecord: ConsumerRecord[Array[Byte], Array[Byte]], output: PrintStream)`
  * MessageReader interface was changed from `def readMessage(): KeyedMessage[Array[Byte], Array[Byte]]` to `def readMessage(): ProducerRecord[Array[Byte], Array[Byte]]`
  * MessageFormatter's package was changed from `kafka.tools` to `kafka.common`
  * MessageReader's package was changed from `kafka.tools` to `kafka.common`
  * MirrorMakerMessageHandler no longer exposes the `handle(record: MessageAndMetadata[Array[Byte], Array[Byte]])` method as it was never called. 
  * The 0.7 KafkaMigrationTool is no longer packaged with Kafka. If you need to migrate from 0.7 to 0.10.0, please migrate to 0.8 first and then follow the documented upgrade process to upgrade from 0.8 to 0.10.0. 
  * The new consumer has standardized its APIs to accept `java.util.Collection` as the sequence type for method parameters. Existing code may have to be updated to work with the 0.10.0 client library. 
  * LZ4-compressed message handling was changed to use an interoperable framing specification (LZ4f v1.5.1). To maintain compatibility with old clients, this change only applies to Message format 0.10.0 and later. Clients that Produce/Fetch LZ4-compressed messages using v0/v1 (Message format 0.9.0) should continue to use the 0.9.0 framing implementation. Clients that use Produce/Fetch protocols v2 or later should use interoperable LZ4f framing. A list of interoperable LZ4 libraries is available at http://www.lz4.org/ 


### Notable changes in 0.10.0.0

  * Starting from Kafka 0.10.0.0, a new client library named **Kafka Streams** is available for stream processing on data stored in Kafka topics. This new client library only works with 0.10.x and upward versioned brokers due to message format changes mentioned above. For more information please read [Streams documentation](/21/streams).
  * The default value of the configuration parameter `receive.buffer.bytes` is now 64K for the new consumer.
  * The new consumer now exposes the configuration parameter `exclude.internal.topics` to restrict internal topics (such as the consumer offsets topic) from accidentally being included in regular expression subscriptions. By default, it is enabled.
  * The old Scala producer has been deprecated. Users should migrate their code to the Java producer included in the kafka-clients JAR as soon as possible. 
  * The new consumer API has been marked stable. 



## Upgrading from 0.8.0, 0.8.1.X, or 0.8.2.X to 0.9.0.0

0.9.0.0 has potential breaking changes (please review before upgrading) and an inter-broker protocol change from previous versions. This means that upgraded brokers and clients may not be compatible with older versions. It is important that you upgrade your Kafka cluster before upgrading your clients. If you are using MirrorMaker downstream clusters should be upgraded first as well. 

**For a rolling upgrade:**

  1. Update server.properties file on all brokers and add the following property: inter.broker.protocol.version=0.8.2.X 
  2. Upgrade the brokers. This can be done a broker at a time by simply bringing it down, updating the code, and restarting it. 
  3. Once the entire cluster is upgraded, bump the protocol version by editing inter.broker.protocol.version and setting it to 0.9.0.0.
  4. Restart the brokers one by one for the new protocol version to take effect 



**Note:** If you are willing to accept downtime, you can simply take all the brokers down, update the code and start all of them. They will start with the new protocol by default. 

**Note:** Bumping the protocol version and restarting can be done any time after the brokers were upgraded. It does not have to be immediately after. 

### Potential breaking changes in 0.9.0.0

  * Java 1.6 is no longer supported. 
  * Scala 2.9 is no longer supported. 
  * Broker IDs above 1000 are now reserved by default to automatically assigned broker IDs. If your cluster has existing broker IDs above that threshold make sure to increase the reserved.broker.max.id broker configuration property accordingly. 
  * Configuration parameter replica.lag.max.messages was removed. Partition leaders will no longer consider the number of lagging messages when deciding which replicas are in sync. 
  * Configuration parameter replica.lag.time.max.ms now refers not just to the time passed since last fetch request from replica, but also to time since the replica last caught up. Replicas that are still fetching messages from leaders but did not catch up to the latest messages in replica.lag.time.max.ms will be considered out of sync. 
  * Compacted topics no longer accept messages without key and an exception is thrown by the producer if this is attempted. In 0.8.x, a message without key would cause the log compaction thread to subsequently complain and quit (and stop compacting all compacted topics). 
  * MirrorMaker no longer supports multiple target clusters. As a result it will only accept a single --consumer.config parameter. To mirror multiple source clusters, you will need at least one MirrorMaker instance per source cluster, each with its own consumer configuration. 
  * Tools packaged under _org.apache.kafka.clients.tools.*_ have been moved to _org.apache.kafka.tools.*_. All included scripts will still function as usual, only custom code directly importing these classes will be affected. 
  * The default Kafka JVM performance options (KAFKA_JVM_PERFORMANCE_OPTS) have been changed in kafka-run-class.sh. 
  * The kafka-topics.sh script (kafka.admin.TopicCommand) now exits with non-zero exit code on failure. 
  * The kafka-topics.sh script (kafka.admin.TopicCommand) will now print a warning when topic names risk metric collisions due to the use of a '.' or '_' in the topic name, and error in the case of an actual collision. 
  * The kafka-console-producer.sh script (kafka.tools.ConsoleProducer) will use the Java producer instead of the old Scala producer be default, and users have to specify 'old-producer' to use the old producer. 
  * By default, all command line tools will print all logging messages to stderr instead of stdout. 



### Notable changes in 0.9.0.1

  * The new broker id generation feature can be disabled by setting broker.id.generation.enable to false. 
  * Configuration parameter log.cleaner.enable is now true by default. This means topics with a cleanup.policy=compact will now be compacted by default, and 128 MB of heap will be allocated to the cleaner process via log.cleaner.dedupe.buffer.size. You may want to review log.cleaner.dedupe.buffer.size and the other log.cleaner configuration values based on your usage of compacted topics. 
  * Default value of configuration parameter fetch.min.bytes for the new consumer is now 1 by default. 



### Deprecations in 0.9.0.0

  * Altering topic configuration from the kafka-topics.sh script (kafka.admin.TopicCommand) has been deprecated. Going forward, please use the kafka-configs.sh script (kafka.admin.ConfigCommand) for this functionality. 
  * The kafka-consumer-offset-checker.sh (kafka.tools.ConsumerOffsetChecker) has been deprecated. Going forward, please use kafka-consumer-groups.sh (kafka.admin.ConsumerGroupCommand) for this functionality. 
  * The kafka.tools.ProducerPerformance class has been deprecated. Going forward, please use org.apache.kafka.tools.ProducerPerformance for this functionality (kafka-producer-perf-test.sh will also be changed to use the new class). 
  * The producer config block.on.buffer.full has been deprecated and will be removed in future release. Currently its default value has been changed to false. The KafkaProducer will no longer throw BufferExhaustedException but instead will use max.block.ms value to block, after which it will throw a TimeoutException. If block.on.buffer.full property is set to true explicitly, it will set the max.block.ms to Long.MAX_VALUE and metadata.fetch.timeout.ms will not be honoured



## Upgrading from 0.8.1 to 0.8.2

0.8.2 is fully compatible with 0.8.1. The upgrade can be done one broker at a time by simply bringing it down, updating the code, and restarting it. 

## Upgrading from 0.8.0 to 0.8.1

0.8.1 is fully compatible with 0.8. The upgrade can be done one broker at a time by simply bringing it down, updating the code, and restarting it. 

## Upgrading from 0.7

Release 0.7 is incompatible with newer releases. Major changes were made to the API, ZooKeeper data structures, and protocol, and configuration in order to add replication (Which was missing in 0.7). The upgrade from 0.7 to later versions requires a [special tool](https://cwiki.apache.org/confluence/display/KAFKA/Migrating+from+0.7+to+0.8) for migration. This migration can be done without downtime. 
