---
title: Testing a Streams Application
description: 
weight: 7
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Testing a Streams Application

To test a Kafka Streams application, Kafka provides a test-utils artifact that can be added as regular dependency to your test code base. Example `pom.xml` snippet when using Maven: 
    
    
    <dependency>
        <groupId>org.apache.kafka</groupId>
        <artifactId>kafka-streams-test-utils</artifactId>
        <version>1.1.0</version>
        <scope>test</scope>
    </dependency>
        

The test-utils package provides a `TopologyTestDriver` that can be used pipe data through a `Topology` that is either assembled manually using Processor API or via the DSL using `StreamsBuilder`. The test driver simulates the library runtime that continuously fetches records from input topics and processes them by traversing the topology. You can use the test driver to verify that your specified processor topology computes the correct result with the manually piped in data records. The test driver captures the results records and allows to query its embedded state stores. 
    
    
    // Processor API
    Topology topology = new Topology();
    topology.addSource("sourceProcessor", "input-topic");
    topology.addProcessor("processor", ..., "sourceProcessor");
    topology.addSink("sinkProcessor", "output-topic", "processor");
    // or
    // using DSL
    StreamsBuilder builder = new StreamsBuilder();
    builder.stream("input-topic").filter(...).to("output-topic");
    Topology topology = builder.build();
    
    // setup test driver
    Properties config = new Properties();
    config.put(StreamsConfig.APPLICATION_ID_CONFIG, "test");
    config.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummy:1234");
    TopologyTestDriver testDriver = new TopologyTestDriver(topology, config);
        

The test driver accepts `ConsumerRecord`s with key and value type `byte[]`. Because `byte[]` types can be problematic, you can use the `ConsumerRecordFactory` to generate those records by providing regular Java types for key and values and the corresponding serializers. 
    
    
    ConsumerRecordFactory<String, Integer> factory = new ConsumerRecordFactory<>("input-topic", new StringSerializer(), new IntegerSerializer());
    testDriver.pipe(factory.create("key", 42L));
        

To verify the output, the test driver produces `ProducerRecord`s with key and value type `byte[]`. For result verification, you can specify corresponding deserializers when reading the output record from the driver. 
    
    
    ProducerRecord<String, Integer> outputRecord = testDriver.readOutput("output-topic", new StringDeserializer(), new LongDeserializer());
        

For result verification, you can use `OutputVerifier`. It offers helper methods to compare only certain parts of the result record: for example, you might only care about the key and value, but not the timestamp of the result record. 
    
    
    OutputVerifier.compareKeyValue(outputRecord, "key", 42L); // throws AssertionError if key or value does not match
        

`TopologyTestDriver` supports punctuations, too. Event-time punctuations are triggered automatically based on the processed records' timestamps. Wall-clock-time punctuations can also be triggered by advancing the test driver's wall-clock-time (the driver mocks wall-clock-time internally to give users control over it). 
    
    
    testDriver.advanceWallClockTime(20L);
        

Additionally, you can access state stores via the test driver before or after a test. Accessing stores before a test is useful to pre-populate a store with some initial values. After data was processed, expected updates to the store can be verified. 
    
    
    KeyValueStore store = testDriver.getKeyValueStore("store-name");
        

Note, that you should always close the test driver at the end to make sure all resources are release properly. 
    
    
    testDriver.close();
        

# Example

The following example demonstrates how to use the test driver and helper classes. The example creates a topology that computes the maximum value per key using a key-value-store. While processing, no output is generated, but only the store is updated. Output is only sent downstream based on event-time and wall-clock punctuations. 
    
    
    private TopologyTestDriver testDriver;
    private KeyValueStore<String, Long> store;
    
    private StringDeserializer stringDeserializer = new StringDeserializer();
    private LongDeserializer longDeserializer = new LongDeserializer();
    private ConsumerRecordFactory<String, Long> recordFactory = new ConsumerRecordFactory<>(new StringSerializer(), new LongSerializer());
    
    @Before
    public void setup() {
        Topology topology = new Topology();
        topology.addSource("sourceProcessor", "input-topic");
        topology.addProcessor("aggregator", new CustomMaxAggregatorSupplier(), "sourceProcessor");
        topology.addStateStore(
            Stores.keyValueStoreBuilder(
                Stores.inMemoryKeyValueStore("aggStore"),
                Serdes.String(),
                Serdes.Long()).withLoggingDisabled(), // need to disable logging to allow store pre-populating
            "aggregator");
        topology.addSink("sinkProcessor", "result-topic", "aggregator");
    
        // setup test driver
        Properties config = new Properties();
        config.setProperty(StreamsConfig.APPLICATION_ID_CONFIG, "maxAggregation");
        config.setProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummy:1234");
        config.setProperty(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        config.setProperty(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.Long().getClass().getName());
        testDriver = new TopologyTestDriver(topology, config);
    
        // pre-populate store
        store = testDriver.getKeyValueStore("aggStore");
        store.put("a", 21L);
    }
    
    @After
    public void tearDown() {
        testDriver.close();
    }
    
    @Test
    public void shouldFlushStoreForFirstInput() {
        testDriver.pipeInput(recordFactory.create("input-topic", "a", 1L, 9999L));
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 21L);
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    }
    
    @Test
    public void shouldNotUpdateStoreForSmallerValue() {
        testDriver.pipeInput(recordFactory.create("input-topic", "a", 1L, 9999L));
        Assert.assertThat(store.get("a"), equalTo(21L));
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 21L);
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    }
    
    @Test
    public void shouldNotUpdateStoreForLargerValue() {
        testDriver.pipeInput(recordFactory.create("input-topic", "a", 42L, 9999L));
        Assert.assertThat(store.get("a"), equalTo(42L));
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 42L);
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    }
    
    @Test
    public void shouldUpdateStoreForNewKey() {
        testDriver.pipeInput(recordFactory.create("input-topic", "b", 21L, 9999L));
        Assert.assertThat(store.get("b"), equalTo(21L));
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 21L);
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "b", 21L);
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    }
    
    @Test
    public void shouldPunctuateIfEvenTimeAdvances() {
        testDriver.pipeInput(recordFactory.create("input-topic", "a", 1L, 9999L));
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 21L);
    
        testDriver.pipeInput(recordFactory.create("input-topic", "a", 1L, 9999L));
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    
        testDriver.pipeInput(recordFactory.create("input-topic", "a", 1L, 10000L));
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 21L);
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    }
    
    @Test
    public void shouldPunctuateIfWallClockTimeAdvances() {
        testDriver.advanceWallClockTime(60000);
        OutputVerifier.compareKeyValue(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer), "a", 21L);
        Assert.assertNull(testDriver.readOutput("result-topic", stringDeserializer, longDeserializer));
    }
    
    public class CustomMaxAggregatorSupplier implements ProcessorSupplier<String, Long> {
        @Override
        public Processor<String, Long> get() {
            return new CustomMaxAggregator();
        }
    }
    
    public class CustomMaxAggregator implements Processor<String, Long> {
        ProcessorContext context;
        private KeyValueStore<String, Long> store;
    
        @SuppressWarnings("unchecked")
        @Override
        public void init(ProcessorContext context) {
            this.context = context;
            context.schedule(60000, PunctuationType.WALL_CLOCK_TIME, new Punctuator() {
                @Override
                public void punctuate(long timestamp) {
                    flushStore();
                }
            });
            context.schedule(10000, PunctuationType.STREAM_TIME, new Punctuator() {
                @Override
                public void punctuate(long timestamp) {
                    flushStore();
                }
            });
            store = (KeyValueStore<String, Long>) context.getStateStore("aggStore");
        }
    
        @Override
        public void process(String key, Long value) {
            Long oldValue = store.get(key);
            if (oldValue == null || value > oldValue) {
                store.put(key, value);
            }
        }
    
        private void flushStore() {
            KeyValueIterator<String, Long> it = store.all();
            while (it.hasNext()) {
                KeyValue<String, Long> next = it.next();
                context.forward(next.key, next.value);
            }
        }
    
        @Override
        public void punctuate(long timestamp) {} // deprecated; not used
    
        @Override
        public void close() {}
    }
        

[Previous](/11/streams/developer-guide/datatypes) [Next](/11/streams/developer-guide/interactive-queries)

  * [Documentation](/documentation)
  * [Kafka Streams](/streams)
  * [Developer Guide](/streams/developer-guide/)


