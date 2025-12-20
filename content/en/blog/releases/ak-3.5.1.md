---
date: 2023-07-21
title: Apache Kafka 3.5.1 Release Announcement
linkTitle: AK 3.5.1
author: Divij Vaidya (@DivijVaidya)
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




We are proud to announce the release of Apache Kafka 3.5.1. This is a security patch release. It upgrades the dependency, snappy-java, to a version which is not vulnerable to [CVE-2023-34455](https://nvd.nist.gov/vuln/detail/CVE-2023-34455). You can find more information about the CVE at [Kafka CVE list](https://kafka.apache.org/cve-list#CVE-2023-3445). For a full list of changes, be sure to check the [release notes](https://archive.apache.org/dist/kafka/3.5.1/RELEASE_NOTES.html).

See the [Upgrading to 3.5.1 from any version 0.8.x through 3.4.x](https://kafka.apache.org/35/documentation.html#upgrade_3_5_1) section in the documentation for the list of notable changes and detailed upgrade steps.

## Kafka Broker, Controller, Producer, Consumer and Admin Client

  * Upgraded the dependency, snappy-java, to a version which is not vulnerable to [CVE-2023-34455.](https://nvd.nist.gov/vuln/detail/CVE-2023-34455) You can find more information about the CVE at [Kafka CVE list.](https://kafka.apache.org/cve-list#CVE-2023-34455)
  * Fixed a regression introduced in 3.3.0, which caused `security.protocol` configuration values to be restricted to upper case only. After the fix, `security.protocol` values are case insensitive. See [KAFKA-15053](https://issues.apache.org/jira/browse/KAFKA-15053) for details. 



## Summary

This was a community effort, so thank you to everyone who contributed to this release, including all our users and our 22 authors. Please report an unintended omission. 

Alyssa Huang, Aman Singh, andymg3, Bo Gao, Calvin Liu, Chia-Ping Tsai, Chris Egerton, d00791190, Damon Xie, David Arthur, David Jacot, Divij Vaidya, DL1231, ezio, Manikumar Reddy, Manyanda Chitimbo, Mickael Maison, minjian.cai, Proven Provenzano, Sambhav Jain, vamossagar12, Yash Mayya


