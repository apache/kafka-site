---
title: Data Types and Serialization
description: 
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Data Types and Serialization

Every Kafka Streams application must provide SerDes (Serializer/Deserializer) for the data types of record keys and record values (e.g. `java.lang.String`) to materialize the data when necessary. Operations that require such SerDes information include: `stream()`, `table()`, `to()`, `through()`, `groupByKey()`, `groupBy()`.

You can provide SerDes by using either of these methods:

  * By setting default SerDes via a `StreamsConfig` instance.
  * By specifying explicit SerDes when calling the appropriate API methods, thus overriding the defaults.



**Table of Contents**

  * Configuring SerDes
  * Overriding default SerDes
  * Available SerDes
    * Primitive and basic types
    * JSON
    * Implementing custom serdes

# Configuring SerDes

SerDes specified in the Streams configuration via `StreamsConfig` are used as the default in your Kafka Streams application.
    
        import org.apache.kafka.common.serialization.Serdes;
    import org.apache.kafka.streams.StreamsConfig;
    
    Properties settings = new Properties();
    // Default serde for keys of data records (here: built-in serde for String type)
    settings.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
    // Default serde for values of data records (here: built-in serde for Long type)
    settings.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.Long().getClass().getName());
    
    StreamsConfig config = new StreamsConfig(settings);
    

# Overriding default SerDes

You can also specify SerDes explicitly by passing them to the appropriate API methods, which overrides the default serde settings:
    
        import org.apache.kafka.common.serialization.Serde;
    import org.apache.kafka.common.serialization.Serdes;
    
    final Serde<String> stringSerde = Serdes.String();
    final Serde<Long> longSerde = Serdes.Long();
    
    // The stream userCountByRegion has type `String` for record keys (for region)
    // and type `Long` for record values (for user counts).
    KStream<String, Long> userCountByRegion = ...;
    userCountByRegion.to("RegionCountsTopic", Produced.with(stringSerde, longSerde));
    

If you want to override serdes selectively, i.e., keep the defaults for some fields, then don't specify the serde whenever you want to leverage the default settings:
    
        import org.apache.kafka.common.serialization.Serde;
    import org.apache.kafka.common.serialization.Serdes;
    
    // Use the default serializer for record keys (here: region as String) by not specifying the key serde,
    // but override the default serializer for record values (here: userCount as Long).
    final Serde<Long> longSerde = Serdes.Long();
    KStream<String, Long> userCountByRegion = ...;
    userCountByRegion.to("RegionCountsTopic", Produced.valueSerde(Serdes.Long()));
    

# Available SerDes

# Primitive and basic types

Apache Kafka includes several built-in serde implementations for Java primitives and basic types such as `byte[]` in its `kafka-clients` Maven artifact:
    
        <dependency>
        <groupId>org.apache.kafka</groupId>
        <artifactId>kafka-clients</artifactId>
        <version>1.1.0</version>
    </dependency>
    

This artifact provides the following serde implementations under the package [org.apache.kafka.common.serialization](https://github.com/apache/kafka/blob/1.1/clients/src/main/java/org/apache/kafka/common/serialization), which you can leverage when e.g., defining default serializers in your Streams configuration.

Data type | Serde  
---|---  
byte[] | `Serdes.ByteArray()`, `Serdes.Bytes()` (see tip below)  
ByteBuffer | `Serdes.ByteBuffer()`  
Double | `Serdes.Double()`  
Integer | `Serdes.Integer()`  
Long | `Serdes.Long()`  
String | `Serdes.String()`  
  
**Tip**

[Bytes](https://github.com/apache/kafka/blob/1.1/clients/src/main/java/org/apache/kafka/common/utils/Bytes.java) is a wrapper for Java's `byte[]` (byte array) that supports proper equality and ordering semantics. You may want to consider using `Bytes` instead of `byte[]` in your applications.

# JSON

The code examples of Kafka Streams also include a basic serde implementation for JSON:

    * [JsonPOJOSerializer](https://github.com/apache/kafka/blob/1.1/streams/examples/src/main/java/org/apache/kafka/streams/examples/pageview/JsonPOJOSerializer.java)
    * [JsonPOJODeserializer](https://github.com/apache/kafka/blob/1.1/streams/examples/src/main/java/org/apache/kafka/streams/examples/pageview/JsonPOJODeserializer.java)

You can construct a unified JSON serde from the `JsonPOJOSerializer` and `JsonPOJODeserializer` via `Serdes.serdeFrom(<serializerInstance>, <deserializerInstance>)`. The [PageViewTypedDemo](https://github.com/apache/kafka/blob/1.1/streams/examples/src/main/java/org/apache/kafka/streams/examples/pageview/PageViewTypedDemo.java) example demonstrates how to use this JSON serde.

# Implementing custom SerDes

If you need to implement custom SerDes, your best starting point is to take a look at the source code references of existing SerDes (see previous section). Typically, your workflow will be similar to:

    1. Write a _serializer_ for your data type `T` by implementing [org.apache.kafka.common.serialization.Serializer](https://github.com/apache/kafka/blob/1.1/clients/src/main/java/org/apache/kafka/common/serialization/Serializer.java).
    2. Write a _deserializer_ for `T` by implementing [org.apache.kafka.common.serialization.Deserializer](https://github.com/apache/kafka/blob/1.1/clients/src/main/java/org/apache/kafka/common/serialization/Deserializer.java).
    3. Write a _serde_ for `T` by implementing [org.apache.kafka.common.serialization.Serde](https://github.com/apache/kafka/blob/1.1/clients/src/main/java/org/apache/kafka/common/serialization/Serde.java), which you either do manually (see existing SerDes in the previous section) or by leveraging helper functions in [Serdes](https://github.com/apache/kafka/blob/1.1/clients/src/main/java/org/apache/kafka/common/serialization/Serdes.java) such as `Serdes.serdeFrom(Serializer<T>, Deserializer<T>)`.

[Previous](/11/streams/developer-guide/processor-api) [Next](/11/streams/developer-guide/testing)

    * [Documentation](/documentation)
    * [Kafka Streams](/streams)
    * [Developer Guide](/streams/developer-guide/)
