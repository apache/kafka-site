---
title: "Apache Kafka 3.9.2 Release Announcement"
linkTitle: "AK 3.9.2"
date: 2026-02-21
author: "PoAn Yang"
aliases:
  - /blog/2026/02/21/apache-kafka-3-9-2-release-announcement/
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

We are proud to announce the release of Apache Kafka 3.9.2. This bug-fix release contains several critical fixes and security updates. Notably, this release includes KIP-1252, which addresses inconsistent behavior between ZooKeeper and KRaft modes.

For a full list of changes, be sure to check the [release notes](https://downloads.apache.org/kafka/3.9.2/RELEASE_NOTES.html).

## Kafka Broker, Controller

* [KIP-1252: AlterConfigPolicy compatibility in legacy Zookeeper mode](https://cwiki.apache.org/confluence/x/c4XMFw)
  Addresses AlterConfigPolicy incompatibility between ZK and KRaft modes. A new server configuration `alter.config.policy.kraft.compatibility.enable` (default: `false`) allows operators to opt into KRaft-compatible behavior in ZooKeeper mode, ensuring consistent policy validation across both deployment modes.

## Summary

This was a community effort, so thank you to everyone who contributed to this release: Alieh Saeedi, Alyssa Huang, Arpit Goyal, Bill Bejeck, Calvin Liu, Chang-Chi Hsu, Chia-Ping Tsai, ChickenchickenLove, Clemens Hutter, Colin Patrick McCabe, Dániel Urbán, David Arthur, David Jacot, Dongnuo Lyu, Donny Nadolny, Edoardo Comar, Erik Anderson, Fatih, Federico Valeri, Gaurav Narula, Genseric Ghiro, Gergely Harmadas, Harish Vishwanath, Ismael Juma, Janindu Pathirana, Jian, jimmy, José Armando García Sancio, Jun Rao, Justine Olshan, Kaushik Raina, Ken Huang, Kevin Wu, Kuan-Po Tseng, Lan Ding, Lianet Magrans, Lucas Brutschy, Luke Chen, majialong, Manikumar Reddy, Masahiro Mori, Matthias J. Sax, Mickael Maison, Ming-Yen Chung, Nikita Shupletsov, Okada Haruki, Oleksandr Luzhniy, Paolo Patierno, PoAn Yang, Rajini Sivaram, Ritika Reddy, Shashank, Shicheng Rao, shub-est, TengYao Chi, Viktor Somogyi-Vass, Vincent Jiang
