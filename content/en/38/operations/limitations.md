---
title: Limitations
description: Limitations
weight: 13
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Limitations

  * While a cluster is being migrated from ZK mode to KRaft mode, we do not support changing the _metadata version_ (also known as the _inter.broker.protocol.version_.) Please do not attempt to do this during a migration, or you may break the cluster.
  * After the migration has been finalized, it is not possible to revert back to ZooKeeper mode.
  * During the migration, if a ZK broker is running with multiple log directories, any directory failure will cause the broker to shutdown. Brokers with broken log directories will only be able to migrate to KRaft once the directories are repaired. For further details refer to [KAFKA-16431](https://issues.apache.org/jira/browse/KAFKA-16431). 
  * As noted above, some features are not fully implemented in KRaft mode. If you are using one of those features, you will not be able to migrate to KRaft yet.


