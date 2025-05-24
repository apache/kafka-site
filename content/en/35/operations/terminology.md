---
title: Terminology
description: Terminology
weight: 11
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Terminology

We use the term "migration" here to refer to the process of changing a Kafka cluster's metadata system from ZooKeeper to KRaft and migrating existing metadata. An "upgrade" refers to installing a newer version of Kafka. It is not recommended to upgrade the software at the same time as performing a metadata migration. 

We also use the term "ZK mode" to refer to Kafka brokers which are using ZooKeeper as their metadata system. "KRaft mode" refers Kafka brokers which are using a KRaft controller quorum as their metadata system. 
