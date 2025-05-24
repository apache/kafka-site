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

  * Brokers that are in **ZK mode** store their metadata in Apache ZooKepeer. This is the old mode of handling metadata.
  * Brokers that are in **KRaft mode** store their metadata in a KRaft quorum. This is the new and improved mode of handling metadata.
  * **Migration** is the process of moving cluster metadata from ZooKeeper into a KRaft quorum.


