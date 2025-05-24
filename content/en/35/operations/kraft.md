---
title: KRaft
description: KRaft
weight: 10
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# KRaft

## Configuration

### Process Roles

In KRaft mode each Kafka server can be configured as a controller, a broker, or both using the `process.roles` property. This property can have the following values:

  * If `process.roles` is set to `broker`, the server acts as a broker.
  * If `process.roles` is set to `controller`, the server acts as a controller.
  * If `process.roles` is set to `broker,controller`, the server acts as both a broker and a controller.
  * If `process.roles` is not set at all, it is assumed to be in ZooKeeper mode.



Kafka servers that act as both brokers and controllers are referred to as "combined" servers. Combined servers are simpler to operate for small use cases like a development environment. The key disadvantage is that the controller will be less isolated from the rest of the system. For example, it is not possible to roll or scale the controllers separately from the brokers in combined mode. Combined mode is not recommended in critical deployment environments.

### Controllers

In KRaft mode, specific Kafka servers are selected to be controllers (unlike the ZooKeeper-based mode, where any server can become the Controller). The servers selected to be controllers will participate in the metadata quorum. Each controller is either an active or a hot standby for the current active controller.

A Kafka admin will typically select 3 or 5 servers for this role, depending on factors like cost and the number of concurrent failures your system should withstand without availability impact. A majority of the controllers must be alive in order to maintain availability. With 3 controllers, the cluster can tolerate 1 controller failure; with 5 controllers, the cluster can tolerate 2 controller failures.

All of the servers in a Kafka cluster discover the quorum voters using the `controller.quorum.voters` property. This identifies the quorum controller servers that should be used. All the controllers must be enumerated. Each controller is identified with their `id`, `host` and `port` information. For example:
    
    
    controller.quorum.voters=id1@host1:port1,id2@host2:port2,id3@host3:port3

If a Kafka cluster has 3 controllers named controller1, controller2 and controller3, then controller1 may have the following configuration:
    
    
    process.roles=controller
    node.id=1
    listeners=CONTROLLER://controller1.example.com:9093
    controller.quorum.voters=1@controller1.example.com:9093,2@controller2.example.com:9093,3@controller3.example.com:9093

Every broker and controller must set the `controller.quorum.voters` property. The node ID supplied in the `controller.quorum.voters` property must match the corresponding id on the controller servers. For example, on controller1, node.id must be set to 1, and so forth. Each node ID must be unique across all the servers in a particular cluster. No two servers can have the same node ID regardless of their `process.roles` values. 

## Storage Tool

The `kafka-storage.sh random-uuid` command can be used to generate a cluster ID for your new cluster. This cluster ID must be used when formatting each server in the cluster with the `kafka-storage.sh format` command. 

This is different from how Kafka has operated in the past. Previously, Kafka would format blank storage directories automatically, and also generate a new cluster ID automatically. One reason for the change is that auto-formatting can sometimes obscure an error condition. This is particularly important for the metadata log maintained by the controller and broker servers. If a majority of the controllers were able to start with an empty log directory, a leader might be able to be elected with missing committed data.

## Debugging

### Metadata Quorum Tool

The `kafka-metadata-quorum` tool can be used to describe the runtime state of the cluster metadata partition. For example, the following command displays a summary of the metadata quorum:
    
    
      > bin/kafka-metadata-quorum.sh --bootstrap-server  broker_host:port describe --status
    ClusterId:              fMCL8kv1SWm87L_Md-I2hg
    LeaderId:               3002
    LeaderEpoch:            2
    HighWatermark:          10
    MaxFollowerLag:         0
    MaxFollowerLagTimeMs:   -1
    CurrentVoters:          [3000,3001,3002]
    CurrentObservers:       [0,1,2]

### Dump Log Tool

The `kafka-dump-log` tool can be used to debug the log segments and snapshots for the cluster metadata directory. The tool will scan the provided files and decode the metadata records. For example, this command decodes and prints the records in the first log segment:
    
    
      > bin/kafka-dump-log.sh --cluster-metadata-decoder --files metadata_log_dir/__cluster_metadata-0/00000000000000000000.log

This command decodes and prints the recrods in the a cluster metadata snapshot:
    
    
      > bin/kafka-dump-log.sh --cluster-metadata-decoder --files metadata_log_dir/__cluster_metadata-0/00000000000000000100-0000000001.checkpoint

### Metadata Shell

The `kafka-metadata-shell` tool can be used to interactively inspect the state of the cluster metadata partition:
    
    
      > bin/kafka-metadata-shell.sh  --snapshot metadata_log_dir/__cluster_metadata-0/00000000000000000000.log
    >> ls /
    brokers  local  metadataQuorum  topicIds  topics
    >> ls /topics
    foo
    >> cat /topics/foo/0/data
    {
      "partitionId" : 0,
      "topicId" : "5zoAlv-xEh9xRANKXt1Lbg",
      "replicas" : [ 1 ],
      "isr" : [ 1 ],
      "removingReplicas" : null,
      "addingReplicas" : null,
      "leader" : 1,
      "leaderEpoch" : 0,
      "partitionEpoch" : 0
    }
    >> exit
      

## Deploying Considerations

  * Kafka server's `process.role` should be set to either `broker` or `controller` but not both. Combined mode can be used in development environments, but it should be avoided in critical deployment environments.
  * For redundancy, a Kafka cluster should use 3 controllers. More than 3 controllers is not recommended in critical environments. In the rare case of a partial network failure it is possible for the cluster metadata quorum to become unavailable. This limitation will be addressed in a future release of Kafka.
  * The Kafka controllers store all the metadata for the cluster in memory and on disk. We believe that for a typical Kafka cluster 5GB of main memory and 5GB of disk space on the metadata log director is sufficient.



## Missing Features

The following features are not fully implemented in KRaft mode:

  * Supporting JBOD configurations with multiple storage directories
  * Modifying certain dynamic configurations on the standalone KRaft controller
  * Delegation tokens



## ZooKeeper to KRaft Migration

**ZooKeeper to KRaft migration is considered an Early Access feature and is not recommended for production clusters.**

The following features are not yet supported for ZK to KRaft migrations:

  * Downgrading to ZooKeeper mode during or after the migration
  * Other features not yet supported in KRaft



Please report issues with ZooKeeper to KRaft migration using the [project JIRA](https://issues.apache.org/jira/projects/KAFKA) and the "kraft" component. 
