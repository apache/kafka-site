---
title: Migration Phases
description: Migration Phases
weight: 12
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Migration Phases

In general, the migration process passes through several phases. 

  * In the **initial phase** , all the brokers are in ZK mode, and there is a ZK-based controller.
  * During the **initial metadata load** , a KRaft quorum loads the metadata from ZooKeeper,
  * In **hybrid phase** , some brokers are in ZK mode, but there is a KRaft controller.
  * In **dual-write phase** , all brokers are KRaft, but the KRaft controller is continuing to write to ZK.
  * When the migration has been **finalized** , we no longer write metadata to ZooKeeper.


