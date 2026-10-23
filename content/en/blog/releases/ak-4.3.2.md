---
date: 2026-10-23
title: Apache Kafka 4.3.2 Release Announcement
linkTitle: AK 4.3.2
author: Ken Huang
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

We are proud to announce the release of Apache Kafka 4.3.2. This is a bugfix release that fixes around 60 issues since the 4.3.1 release, most notably two potential data loss issues in tiered storage size-based retention and time index truncation. For a full list of changes, be sure to check the [release notes](https://downloads.apache.org/kafka/4.3.2/RELEASE_NOTES.html).

See the [Upgrading to 4.3.2](https://kafka.apache.org/43/getting-started/upgrade/#upgrading-to-432) section in the documentation for the list of notable changes and detailed upgrade steps.

## Notable fixes

* Fixed a tiered storage bug in which size-based retention could delete data that was still within retention from both local and remote tiers after a leader election ([KAFKA-20732](https://issues.apache.org/jira/browse/KAFKA-20732)).
* Fixed a potential data loss issue in which the time index could be truncated across a broker restart, causing segments that were still within retention to be deleted by time-based retention ([KAFKA-20979](https://issues.apache.org/jira/browse/KAFKA-20979)).
* Fixed several Kafka Streams bugs that could cause a `StreamThread` to die after task corruption, task recycling, or state updater timeouts ([KAFKA-20808](https://issues.apache.org/jira/browse/KAFKA-20808), [KAFKA-20827](https://issues.apache.org/jira/browse/KAFKA-20827), [KAFKA-20721](https://issues.apache.org/jira/browse/KAFKA-20721)), and an issue in which the state directory could be cleaned prematurely, forcing a from-scratch restore ([KAFKA-20805](https://issues.apache.org/jira/browse/KAFKA-20805)).
* Updated dependencies to address published CVEs in jackson-databind, lz4-java, log4j and Jetty.

## Summary

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 57 contributors: Adam Horky, Adam Souquières, Alan Lau, Alieh Saeedi, Alyssa Huang, Anastasia Vela, Andrew Schofield, Apoorv Mittal, Avishek Das, Bill Bejeck, Chia-Ping Tsai, ChickenchickenLove, Chris Egerton, Daeho Kwon, David Jacot, Dongnuo Lyu, Evan Zhou, Federico Valeri, Gabriella Fu, Gaurav Narula, Gavin Wang, Gergely Harmadas, imavishek, Izzy Harker, Justine Olshan, Ken Huang, Kevin Wu, Kuan-Po Tseng, Lianet Magrans, Lucas Brutschy, Lucy Liu, Luke Chen, Manikumar Reddy, Matthias J. Sax, Mickael Maison, Mingi Cho, Nick Telford, Nikita Shupletsov, nileshkumar3, Omnia Ibrahim, Paolo Patierno, Parker Chang, PoAn Yang, Rishabh Saraswat, Russole Chen, Sean Quah, Sepuri Sai Krishna, Shay Elkin, Srinivas Akhil Mallela, subbudvk, Sushant Mahajan, Tamas Kornai, TengYao Chi, Truc Nguyen, Uladzislau Blok, Zheguang Zhao, zhiyan-tang
