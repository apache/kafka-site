---
date: 2026-10-22
title: Apache Kafka 4.4.0 Release Announcement
linkTitle: AK 4.4.0
author: Omnia Ibrahim
aliases:
  - /blog/2026/10/22/apache-kafka-4.4.0-release-announcement/
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

We are proud to announce the release of Apache Kafka® 4.4.0. This release contains many new features and improvements. This blog post will highlight some of the more prominent ones. For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/4.4.0/RELEASE_NOTES.html).

With 11 KIPs and over 963 commits since 4.3.0, this release introduces many new features, improvements and bug fixes to all the components.

See the [Upgrading to 4.4](https://kafka.apache.org/documentation.html#upgrade_4_4_0) section in the documentation for the list of notable changes and detailed upgrade steps.

## Deprecation Notices
* [KIP-1232: Deprecate broker.id config](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/393677342/KIP-1232+Deprecate+broker.id+config)
  Deprecates the `broker.id` broker configuration.

* [KIP-1200: Deprecate ClientQuotaCallback#updateClusterMetadata](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/373887083/KIP-1200+Deprecate+ClientQuotaCallback+updateClusterMetadata)
  Deprecates the `ClientQuotaCallback#updateClusterMetadata` method and will be removed in Kafka 5.0. Custom implementations of `ClientQuotaCallback` no longer need to override this method, as a default no-op implementation is now provided.

* [KIP-1301: Deprecate Yammer-based metrics in GroupCoordinatorMetrics](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/406623591/KIP-1301+Deprecate+Yammer-based+metrics+in+GroupCoordinatorMetrics)
  Deprecates the remaining Yammer-based classic-group metrics in `GroupCoordinatorMetrics` (NumGroups, NumOffsets, NumGroupsPreparingRebalance, NumGroupsCompletingRebalance, NumGroupsStable, NumGroupsDead), replacing them with equivalent Kafka Metrics gauges registered under the `kafka.server:type=group-coordinator-metrics` MBean.

## Kafka Broker, Controller, Producer, Consumer and Admin Client
* [KIP-1170: Unify cluster metadata bootstrapping](https://cwiki.apache.org/confluence/x/ZYoEFQ)
  Storage directories formatted by the `kafka-storage` tool are no longer forward-compatible: a broker must now be the same version as, or newer than, the `kafka-storage` tool that formatted its directory, regardless of the `--release-version` chosen at format time.

* [KIP-1191: Dead-letter queues for share groups](https://cwiki.apache.org/confluence/x/fApJFg)
  Share groups now support dead-letter queues. Records that are released beyond the max delivery count, or rejected by the share consumer, become eligible for the DLQ once the `share.version` feature is upgraded to 2. DLQ behavior is configured dynamically via `errors.deadletterqueue.topic.name`, `errors.deadletterqueue.auto.create.topics.enable`, `errors.deadletterqueue.group.enable`, `errors.deadletterqueue.topic.name.prefix`, and `errors.deadletterqueue.copy.record.enable`.

* [KIP-909: Allow Clients to Rebootstrap Upon Failed DNS Resolution](https://cwiki.apache.org/confluence/x/MJtbDg)
  Adds a new client configuration, `bootstrap.resolve.timeout.ms`, controlling how DNS resolution of `bootstrap.servers` is performed. The default of `0` preserves the historical synchronous behavior; a positive value opts into asynchronous bootstrap resolution, where the client constructor returns immediately and failures surface later as `BootstrapResolutionException`. This is an evolving feature and may change in a minor release. Kafka Streams and Kafka Connect do not yet support asynchronous bootstrap resolution.

* [KIP-1265: Mechanism for automatic detection of internal API usage](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1265%3A+Mechanism+for+automatic+detection+of+internal+API+usage)
  Introduces a build-time `api-checker` mechanism, based on explicit `@InterfaceAudience` annotations, that fails the build if an internal class is imported by or exposed through a public API — preventing internal classes from unintentionally leaking into Kafka's public surface.

* [KIP-1319: Align TxnOffsetCommit API with OffsetCommit API](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/406622772/KIP-1319+Align+TxnOffsetCommit+API+with+OffsetCommit+API)
  Introduces `TxnOffsetCommit` v6, bringing the transactional offset commit API to parity with `OffsetCommit`: it now carries topic IDs instead of topic names, renames `GenerationId` to `GenerationIdOrMemberEpoch`, and surfaces granular error codes such as `GROUP_ID_NOT_FOUND`, `STALE_MEMBER_EPOCH`, and `UNKNOWN_TOPIC_ID` instead of collapsing them into `ILLEGAL_GENERATION`.

## Kafka Streams
* [KIP-1340: Expose Both Mapped Key and Stream Key in Streams-GlobalKTable Joins](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1340%3A+Expose+Both+Mapped+Key+and+Stream+Key+in+Streams-GlobalKTable+Joins)
  Adds a new `ValueJoinerWithStreamAndMappedKey` joiner interface and new `KStream#join`/`leftJoin` overloads for KStream-GlobalKTable joins, giving users access to both the mapped join key and the original stream record key without having to recompute it. The existing `ValueJoinerWithKey`-based overloads are deprecated but unchanged in behavior.

* [KIP-1331: Streams Group Topology Description Plugin](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1331%3A+Streams+Group+Topology+Description+Plugin)
  Lets brokers record a human-readable description of a Streams group's processing topology via a pluggable backend. When `group.streams.topology.description.plugin.class` is set, Kafka Streams clients automatically push a description equivalent to `Topology#describe()` to the group coordinator, retrievable via `Admin#describeStreamsGroups` or `kafka-streams-groups.sh --describe --topology` — without access to the application's source code.

## Kafka Connect
* [KIP-1209: Add configuration to control internal topic creation in Kafka Connect](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1209:+Add+configuration+to+control+internal+topic+creation+in+Kafka+Connect)
  Kafka Connect distributed workers now support the `internal.topics.automatic.creation.enable` configuration (default `true`). When set to `false`, Connect will not automatically create its internal topics (offset, config, status, and connector-specific offset topics) and instead fails at startup if any are missing. A new `connect-internal-topics.sh` tool is provided for creating these topics manually.

## Summary

Ready to get started with Apache Kafka 4.4.0? Check out all the details in the [upgrade notes](https://kafka.apache.org/documentation.html#upgrade_4_4_0) and the [release notes](https://archive.apache.org/dist/kafka/4.4.0/RELEASE_NOTES.html), and [download](https://kafka.apache.org/downloads) Apache Kafka 4.4.0.

<!-- TODO: Confirm the contributor list below. It is the RAW `git shortlog -sn 4.3.0..4.4.0`
     output (152 names) and still contains duplicate identities (e.g. Jiayao Sun / Jiayáo Sun,
     gabriellafu / gabriellefu / gabriellefu, OmniaGM / Omnia Ibrahim, email-only handles like
     majialong, and dependabot[bot]). `release.py release-email` normalises these — run it and
     reconcile the two lists before publishing. Update the count and the "(and N AIs)" tally. -->
This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 152 contributors:
Matthias J. Sax, Ken Huang, Mickael Maison, Nick Telford, Sushant Mahajan, majialong, PoAn Yang, David Jacot, Murali Basani, OmniaGM, Alieh Saeedi, Lianet Magrans, Bill Bejeck, Ming-Yen Chung, Sean Quah, Andrew Schofield, Apoorv Mittal, TengYao Chi, ChickenchickenLove, Sanskar Jhajharia, gabriellafu, Lucy Liu, Maros Orsak, nileshkumar3, Evan Zhou, YANG-SYUAN CHOU, Alan Lau, Jess668, Lucas Brutschy, Uladzislau Blok, Chia-Yi Chiu, Eric Chang, Federico Valeri, Kuan-Po Tseng, Aditya Kousik, Gaurav Narula, Nikita Shupletsov, TaiJuWu, Gavin Wang, Jiayao Sun, Jiayáo Sun, Shekhar Prasad Rajak, Chih-Yuan Chien, Eduwer Camacaro, Gergely Harmadas, Manikumar Reddy, Mingi Cho, Paolo Patierno, Ivan Yurchenko, Nick Guo, Omnia Ibrahim, gomudayya, sstremler, Bolin Lin, Christo Lolov, CoderBruis, Dejan Stojadinović, Dongnuo Lyu, Edoardo Comar, Igor Soarez, Jian, KC.H, Kevin Wu, Lan Ding, LeiXiaoGao, Parker Chang, Russole Chen, Sebastien Viale, yangxuze, Adam Souquières, Arpit Goyal, Avishek Das, Gabriel Dutra, Hector Geraldino, Jakub Scholz, Kai Jay Tu, Kartikay Dubey, Kirk True, Luke Chen, Park Jiwon, RonGamzu, Sahil Devgon, Yunchi Pang, Zheguang Zhao, Zhiyan Tang, ashwinpankaj, dependabot[bot], gabriellefu, mannoopj, red-flames, zoo-code, 조형준, Abhijeet Kumar, Adam Horky, Alyssa Huang, Amir Sarabadani, Andy Huang, Angelo R., Anton Liauchuk, Aravind Reveendran, Arnab Nandy, Arpit Jain, Atharv Chavan, Brian Sang, Chang-Chi Hsu, Charlie Zhang, Daeho Kwon, Daniel Tschinder, David Simon, Davide Armand, Derek Ko, Diya Hussein, Dmitry Werner, Fatorin, Ganesh Manchi, Gimin Kim, Gyeongwon, Do, Hana, Ivan Malutin, Joanna-D, Jonah Hooper, José Armando García Sancio, Kamal Chandraprakash, Kenan Adel, Kondrat Bertalan, Lucas Ma, Mirko Alicastro, Nandini Singhal, Nikolaus Schuetz, Nishant Kumar, Prabhash Kumar, Rajarshi Misra, Rion Williams, Ritika Reddy, Ritikj55, S.Y. Wang, Sepuri Sai Krishna, Shivsundar R, Siddhartha Devineni, Taeik Lim, Tamas Kornai, Tommi Vainikainen, Truc Nguyen, Viktor Somogyi-Vass, Xi, Yu-Chia Ma, akhil-sabu-ibm, amandayclee, averemee-si, minjcho, subbudvk, winfriedgerlach
