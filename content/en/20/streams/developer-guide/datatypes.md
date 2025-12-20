---
title: Data Types and Serialization
description: 
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->


Every Kafka Streams application must provide SerDes (Serializer/Deserializer) for the data types of record keys and record values (e.g. `java.lang.String`) to materialize the data when necessary. Operations that require such SerDes information include: `stream()`, `table()`, `to()`, `through()`, `groupByKey()`, `groupBy()`.

You can provide SerDes by using either of these methods:

  * By setting default SerDes in the `java.util.Properties` config instance.
  * By specifying explicit SerDes when calling the appropriate API methods, thus overriding the defaults.






# Configuring SerDes

SerDes specified in the Streams configuration are used as the default in your Kafka Streams application.
    
    
    import org.apache.kafka.common.serialization.Serdes;
    import org.apache.kafka.streams.StreamsConfig;
    
    Properties settings = new Properties();
    // Default serde for keys of data records (here: built-in serde for String type)
    settings.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
    // Default serde for values of data records (here: built-in serde for Long type)
    settings.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.Long().getClass().getName());
    

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
    

If some of your incoming records are corrupted or ill-formatted, they will cause the deserializer class to report an error. Since 1.0.x we have introduced an `DeserializationExceptionHandler` interface which allows you to customize how to handle such records. The customized implementation of the interface can be specified via the `StreamsConfig`. For more details, please feel free to read the [Configuring a Streams Application](config-streams.html#default-deserialization-exception-handler) section. 

# Available SerDes

## Primitive and basic types

Apache Kafka includes several built-in serde implementations for Java primitives and basic types such as `byte[]` in its `kafka-clients` Maven artifact:
    
    
    <dependency>
        <groupId>org.apache.kafka</groupId>
        <artifactId>kafka-clients</artifactId>
        <version>2.0.0</version>
    </dependency>
    

This artifact provides the following serde implementations under the package [org.apache.kafka.common.serialization](https://github.com/apache/kafka/blob/2.0/clients/src/main/java/org/apache/kafka/common/serialization), which you can leverage when e.g., defining default serializers in your Streams configuration.  
  
<table>  
<tr>  
<th>

Data type
</th>  
<th>

Serde
</th> </tr>  
<tr>  
<td>

byte[]
</td>  
<td>

`Serdes.ByteArray()`, `Serdes.Bytes()` (see tip below)
</td> </tr>  
<tr>  
<td>

ByteBuffer
</td>  
<td>

`Serdes.ByteBuffer()`
</td> </tr>  
<tr>  
<td>

Double
</td>  
<td>

`Serdes.Double()`
</td> </tr>  
<tr>  
<td>

Integer
</td>  
<td>

`Serdes.Integer()`
</td> </tr>  
<tr>  
<td>

Long
</td>  
<td>

`Serdes.Long()`
</td> </tr>  
<tr>  
<td>

String
</td>  
<td>

`Serdes.String()`
</td> </tr> </table>

**Tip**

[Bytes](https://github.com/apache/kafka/blob/2.0/clients/src/main/java/org/apache/kafka/common/utils/Bytes.java) is a wrapper for Java's `byte[]` (byte array) that supports proper equality and ordering semantics. You may want to consider using `Bytes` instead of `byte[]` in your applications.

## JSON

The code examples of Kafka Streams also include a basic serde implementation for JSON:

  * [JsonPOJOSerializer](https://github.com/apache/kafka/blob/2.0/streams/examples/src/main/java/org/apache/kafka/streams/examples/pageview/JsonPOJOSerializer.java)
  * [JsonPOJODeserializer](https://github.com/apache/kafka/blob/2.0/streams/examples/src/main/java/org/apache/kafka/streams/examples/pageview/JsonPOJODeserializer.java)



You can construct a unified JSON serde from the `JsonPOJOSerializer` and `JsonPOJODeserializer` via `Serdes.serdeFrom(<serializerInstance>, <deserializerInstance>)`. The [PageViewTypedDemo](https://github.com/apache/kafka/blob/2.0/streams/examples/src/main/java/org/apache/kafka/streams/examples/pageview/PageViewTypedDemo.java) example demonstrates how to use this JSON serde.

# Implementing custom SerDes

If you need to implement custom SerDes, your best starting point is to take a look at the source code references of existing SerDes (see previous section). Typically, your workflow will be similar to:

  1. Write a _serializer_ for your data type `T` by implementing [org.apache.kafka.common.serialization.Serializer](https://github.com/apache/kafka/blob/2.0/clients/src/main/java/org/apache/kafka/common/serialization/Serializer.java).
  2. Write a _deserializer_ for `T` by implementing [org.apache.kafka.common.serialization.Deserializer](https://github.com/apache/kafka/blob/2.0/clients/src/main/java/org/apache/kafka/common/serialization/Deserializer.java).
  3. Write a _serde_ for `T` by implementing [org.apache.kafka.common.serialization.Serde](https://github.com/apache/kafka/blob/2.0/clients/src/main/java/org/apache/kafka/common/serialization/Serde.java), which you either do manually (see existing SerDes in the previous section) or by leveraging helper functions in [Serdes](https://github.com/apache/kafka/blob/2.0/clients/src/main/java/org/apache/kafka/common/serialization/Serdes.java) such as `Serdes.serdeFrom(Serializer<T>, Deserializer<T>)`.



# Kafka Streams DSL for Scala Implicit SerDes[](scala-dsl-serdes "Permalink to this headline")

When using the [Kafka Streams DSL for Scala](dsl-api.html#scala-dsl) you're not required to configure a default SerDes. In fact, it's not supported. SerDes are instead provided implicitly by default implementations for common primitive datatypes. See the [Implicit SerDes](dsl-api.html#scala-dsl-implicit-serdes) and [User-Defined SerDes](dsl-api.html#scala-dsl-user-defined-serdes) sections in the DSL API documentation for details

  * [Documentation](/documentation)
  * [Kafka Streams](/documentation/streams)
  * [Developer Guide](/documentation/streams/developer-guide/)


