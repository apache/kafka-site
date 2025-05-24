---
title: Reverting to ZooKeeper mode During the Migration
description: Reverting to ZooKeeper mode During the Migration
weight: 19
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Reverting to ZooKeeper mode During the Migration

While the cluster is still in migration mode, it is possible to revert to ZooKeeper mode. The process to follow depends on how far the migration has progressed. In order to find out how to revert, select the **final** migration step that you have **completed** in this table. 

Note that the directions given here assume that each step was fully completed, and they were done in order. So, for example, we assume that if "Enter Migration Mode on the Brokers" was completed, "Provisioning the KRaft controller quorum" was also fully completed previously. 

If you did not fully complete any step, back out whatever you have done and then follow revert directions for the last fully completed step. 

Final Migration Section Completed | Directions for Reverting | Notes  
---|---|---  
Preparing for migration |  The preparation section does not involve leaving ZooKeeper mode. So there is nothing to do in the case of a revert.  |   
Provisioning the KRaft controller quorum | 

  * Deprovision the KRaft controller quorum. 
  * Then you are done. 

|   
Enter Migration Mode on the brokers | 

  * Deprovision the KRaft controller quorum. 
  * Using `zookeeper-shell.sh`, run `rmr /controller` so that one of the brokers can become the new old-style controller. Additionally, run `get /migration` followed by `rmr /migration` to clear the migration state from ZooKeeper. This will allow you to re-attempt the migration in the future. The data read from "/migration" can be useful for debugging. 
  * On each broker, remove the `zookeeper.metadata.migration.enable`, `controller.listener.names`, and `controller.quorum.bootstrap.servers` configurations, and replace `node.id` with `broker.id`. Then perform a rolling restart of all brokers. 
  * Then you are done. 

|  It is important to perform the `zookeeper-shell.sh` step **quickly** , to minimize the amount of time that the cluster lacks a controller. Until the ` /controller` znode is deleted, you can also ignore any errors in the broker log about failing to connect to the Kraft controller. Those error logs should disappear after second roll to pure zookeeper mode.   
Migrating brokers to KRaft | 

  * On each broker, remove the `process.roles` configuration, replace the `node.id` with `broker.id` and restore the `zookeeper.connect` configuration to its previous value. If your cluster requires other ZooKeeper configurations for brokers, such as `zookeeper.ssl.protocol`, re-add those configurations as well. Then perform a rolling restart of all brokers. 
  * Deprovision the KRaft controller quorum. 
  * Using `zookeeper-shell.sh`, run `rmr /controller` so that one of the brokers can become the new old-style controller. 
  * On each broker, remove the `zookeeper.metadata.migration.enable`, `controller.listener.names`, and `controller.quorum.bootstrap.servers` configurations. Then perform a second rolling restart of all brokers. 
  * Then you are done. 

| 

  * It is important to perform the `zookeeper-shell.sh` step **quickly** , to minimize the amount of time that the cluster lacks a controller. Until the ` /controller` znode is deleted, you can also ignore any errors in the broker log about failing to connect to the Kraft controller. Those error logs should disappear after second roll to pure zookeeper mode. 
  * Make sure that on the first cluster roll, `zookeeper.metadata.migration.enable` remains set to `true`. **Do not set it to false until the second cluster roll.**

  
Finalizing the migration |  If you have finalized the ZK migration, then you cannot revert.  |  Some users prefer to wait for a week or two before finalizing the migration. While this requires you to keep the ZooKeeper cluster running for a while longer, it may be helpful in validating KRaft mode in your cluster.   
  