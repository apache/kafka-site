---
date: 2026-07-31
title: "Designing Reliable Gateway-to-Kafka Event Delivery: Batching, Acknowledgments, and Backpressure"
linkTitle: "Reliable Gateway-to-Kafka Event Delivery"
author: "Yilia Lin (@Yilialinn), Apache APISIX Committer"
description: "How Apache Kafka and Apache APISIX can form a route-aware event pipeline with explicit batching, acknowledgement, backpressure, ordering, and consumer-idempotence boundaries."
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

An API gateway that exports access, audit, or security events to Apache Kafka is a producer, even when its integration is called a `logger`. That producer sits beside the request path and usually sends events outside the HTTP response contract. It has queues, batch thresholds, acknowledgement settings, failure modes, and a shutdown boundary. If those details remain implicit, teams may incorrectly treat a successful HTTP response and a durable Kafka record as the same event.

Kafka is valuable in this architecture because its distributed log separates event production from event processing. Retained records can be replayed after a consumer fix, partitions provide scoped ordering, consumer groups scale independent processors, and the same event stream can serve operational analytics, security detection, and other authorized uses without coupling those consumers to the gateway.

Apache APISIX provides the other half of the pattern: a route-aware control point that can create and send structured gateway events without adding a Kafka producer to every upstream service. This article uses the APISIX `kafka-logger` plugin to connect Kafka’s producer and broker semantics to a concrete gateway implementation. It does not claim exactly-once delivery or results from tests that have not been run.

## Why Kafka fits gateway event distribution

Sending every event directly from a gateway to every downstream system creates temporal coupling. A slow analytics service can affect export latency, adding a new consumer requires another integration, and recovery depends on whether the destination retained enough information. Kafka replaces those point-to-point connections with a durable event boundary. The gateway produces once; authorized consumer groups process at their own pace; retention permits replay within the configured window.

This decoupling is useful only when the event contract is stable. Kafka preserves records; it cannot decide whether an event represents request start, response completion, or a committed business transaction. Likewise, ordering is per partition, not global, and retention is finite unless configured otherwise. These are design tools rather than automatic end-to-end guarantees.

APISIX makes the boundary manageable at the edge. Operators can enable a logger on selected Routes, define a common JSON format, attach a request ID, keep bodies excluded, and adjust buffering independently of application deployments. The practical benefit is consistent gateway telemetry across heterogeneous services while Kafka supplies durable distribution and replay.

## Define the event contract at the Route

Before tuning a producer, decide what is being produced. Gateway events may support traffic analysis, incident investigation, audit evidence, billing, fraud detection, or model-usage accounting. Those purposes have different correctness and privacy requirements.

A stable contract should answer:

- Which gateway event creates a record?
- Which identifier lets a consumer recognize the same logical event again?
- Which timestamp represents request start, request completion, or export time?
- Which fields may contain credentials, personal data, or request content?
- Which schema changes are backward compatible?
- Which system remains authoritative if a record is missing?

APISIX supports a JSON `log_format` whose string values can reference APISIX or NGINX variables. When the `request-id` plugin establishes a request ID, the logger can include it as an event identifier. Use that value for deduplication only when the gateway controls it or the client-supplied ID has been validated for the required uniqueness scope. Otherwise, generate a separate gateway-controlled event ID; neither identifier proves that the source emitted exactly once.

The following Route is deliberately bounded. The values illustrate the current configuration surface, not universally recommended production sizing:

```json
{
  "uri": "/orders/*",
  "plugins": {
    "request-id": {
      "header_name": "X-Request-Id",
      "include_in_response": true
    },
    "kafka-logger": {
      "name": "orders-gateway-events",
      "brokers": [
        {
          "host": "kafka-1.internal.example",
          "port": 9092
        },
        {
          "host": "kafka-2.internal.example",
          "port": 9092
        }
      ],
      "kafka_topic": "gateway-events-v1",
      "producer_type": "async",
      "required_acks": -1,
      "timeout": 3,
      "producer_batch_num": 200,
      "producer_batch_size": 1048576,
      "producer_max_buffering": 50000,
      "producer_time_linger": 1,
      "include_req_body": false,
      "include_resp_body": false,
      "log_format": {
        "schema_version": "1",
        "event_id": "$request_id",
        "route_id": "$route_id",
        "service_id": "$service_id",
        "status": "$status",
        "request_time_seconds": "$request_time"
      }
    }
  },
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "orders.internal.example:8080": 1
    }
  }
}
```

Request and response bodies remain excluded. That is a useful privacy default, but headers and URIs may still contain secrets or personal data. Allow, transform, or remove fields according to the event’s purpose. Truncation limits control size; they do not sanitize sensitive content.

## Treat the two batching layers as one budget

This path is not a single `send()` call. APISIX logging plugins first place entries in a batch processor. The asynchronous Kafka producer then applies its own message-count, byte, linger, and buffer limits.

At the plugin layer, the batch processor flushes according to its size and timing conditions. Its documented controls include `batch_max_size`, `inactive_timeout`, `buffer_duration`, `max_retry_count`, and `retry_delay`. If the buffer cannot accept another entry, the logger can return a buffer-overflow error. A client request may therefore succeed while its gateway event does not enter the next delivery stage.

At the producer layer:

- `producer_batch_num` bounds the message count used for batching.
- `producer_batch_size` sets a byte threshold.
- `producer_time_linger` sets the flush interval in seconds.
- `producer_max_buffering` limits buffered messages for the asynchronous producer.
- `timeout` limits how long an upstream send may take.

Kafka benefits when producers form efficient batches, but larger buffers and longer linger also increase the amount of gateway state that exists only in process memory. Size both APISIX layers as one memory-and-delay budget. Estimate the event-size distribution, the maximum acceptable export delay, and the traffic duration the in-memory queues should absorb during a broker slowdown.

If a business transaction must fail whenever its audit record cannot be committed, asynchronous access logging is the wrong transaction boundary. Put that durable write in the application workflow. APISIX remains useful for centralized operational events; Kafka remains useful for distributing and replaying them, but neither changes the business definition of success.

## Connect acknowledgements to Kafka’s replication model

APISIX exposes `required_acks` values `1` and `-1`; it does not allow `0`.

With `required_acks: 1`, the partition leader responds after writing locally. If it fails before followers replicate the record, an acknowledged write can be lost. With `required_acks: -1`, the setting corresponds to Kafka’s `acks=all`: the leader waits for the current in-sync replicas to acknowledge the write.

The stronger setting matters because Kafka’s replication model can reject writes instead of silently reducing the intended durability. `min.insync.replicas` defines the minimum ISR size required when producing with `acks=all`. A common design is replication factor three, `min.insync.replicas=2`, and `acks=all`; when the ISR falls below two, the produce request fails rather than being accepted under the intended threshold.

This improves the broker boundary, not the entire gateway-to-consumer path. An event can still fail before entering the APISIX buffer, remain only in memory during process termination, time out with an ambiguous result, or expire under Kafka retention. APISIX lets operators select the acknowledgement mode per logger, while Kafka enforces the configured replica condition and retains successful records for downstream processing.

Do not project Kafka Java producer features onto a different client implementation. The configuration above does not establish that the APISIX path uses Kafka transactions or producer idempotence. The end-to-end path should not be assumed exactly once: events may be duplicated after ambiguous retries, and events may be missing if they never reach Kafka or are lost from an in-memory gateway buffer.

## Make backpressure visible

Asynchronous export keeps routine broker delay outside the client response, but it also separates request success from export success. The queue is therefore an operational signal, not an implementation detail.

When the APISIX Prometheus plugin is enabled, `apisix_batch_process_entries` reports remaining entries in logging-plugin batches and labels them with the logger’s configured `name`. Naming the logger `orders-gateway-events` links the metric to a Route, topic, and runbook. Operators should combine that signal with APISIX overflow or send errors, Kafka broker errors, consumer lag, and a reconciliation count between produced request IDs and consumed event IDs.

A short queue increase may be normal batching. A queue that remains above a tested threshold, repeated overflow errors, or a widening source-to-consumer difference is more actionable. Kafka consumer lag answers a different question—how far consumers trail the retained log—so it complements rather than replaces the APISIX pending-entry metric.

The overflow policy needs a business owner. Possible responses include dropping noncritical events, rejecting traffic, writing to a durable spool, or moving critical audit events to a synchronous workflow. APISIX exposes the edge-side pressure; Kafka exposes broker and consumer progress. The system owner decides the consequence.

## Design for retries, ordering, and replay

Network failures rarely divide neatly into `sent` and `not sent`. A broker can append and replicate a batch, then lose the acknowledgement when the connection closes. A retry may create another copy; declining to retry may omit a record the broker never received.

Use a stable `event_id` and make consumer side effects idempotent. A consumer can store the ID with the derived result in one database transaction, use a unique constraint to reject repeats, and record duplicate counts for diagnosis. The deduplication window should cover the maximum Kafka retention or replay period that the workflow permits.

Kafka orders records within a partition. APISIX exposes an optional `key` for partition allocation. If one entity requires ordered events, select a stable key only after verifying how the current producer handles it and whether the resulting distribution is balanced. A constant Route key can concentrate traffic on one partition; unrelated random keys remove entity-level ordering. Consumers should treat the partition key, schema version, and event ID as parts of the contract.

Replay is where Kafka’s value becomes especially visible. After correcting a consumer or adding a new authorized processor, a consumer group can read retained gateway events without asking APISIX or every upstream service to emit them again. Replay also repeats side effects unless consumers are idempotent, so retention and deduplication policies must be designed together.

## Validate failure boundaries before making claims

This article does not report fault-test or performance results. Before production use, run controlled scenarios with numbered requests, record the APISIX request IDs, consume the Kafka topic, and compare the sets.

At minimum, evaluate:

1. normal traffic for schema and steady-state batching;
2. broker unavailability for queue growth, timeouts, retries, and overflow;
3. insufficient ISR for the expected `acks=all` rejection;
4. graceful and abrupt APISIX termination while entries are buffered;
5. a network interruption after a broker append for ambiguous outcomes;
6. sensitive or oversized inputs for exclusion and sanitization;
7. consumer restart and Kafka replay for idempotent side effects.

For each scenario, report attempted IDs, consumed IDs, duplicates, missing IDs, queue observations, and relevant errors. Do not turn that ledger into an unqualified delivery percentage, and do not publish throughput or latency numbers without a reproducible environment and workload.

## Production checklist

Before enabling gateway-to-Kafka event delivery:

- define the event purpose, schema version, identifier, timestamps, and privacy boundary;
- use APISIX Route-level configuration to apply a consistent contract without modifying each upstream;
- size both batching layers against memory and delay budgets;
- select `required_acks` together with Kafka replication factor and `min.insync.replicas`;
- monitor APISIX pending entries and errors alongside Kafka broker and consumer signals;
- document buffer-overflow, timeout, retention, and process-termination outcomes;
- choose partition keys only for explicit ordering requirements;
- make consumer side effects idempotent and test replay;
- state which records may still be missing or duplicated.

The useful architecture is the combination: APISIX provides centralized, route-aware event creation, privacy controls, buffering, and edge observability; Kafka provides durable distribution, partitioned ordering, retention, replay, and independent consumer groups. Reliability comes from making the boundary between them explicit and validating the complete system—not from treating one acknowledgement setting as an end-to-end guarantee.

## References

- [Apache APISIX kafka-logger configuration](https://apisix.apache.org/docs/apisix/plugins/kafka-logger/)
- [Apache APISIX batch processor behavior](https://apisix.apache.org/docs/apisix/batch-processor/)
- [Apache Kafka producer configuration](/{version}/configuration/producer-configs/)
- [Apache Kafka topic configuration](/{version}/configuration/topic-configs/)
