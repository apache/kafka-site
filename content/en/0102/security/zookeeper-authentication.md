---
title: ZooKeeper Authentication
description: ZooKeeper Authentication
weight: 6
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# ZooKeeper Authentication

## New clusters

To enable ZooKeeper authentication on brokers, there are two necessary steps: 

  1. Create a JAAS login file and set the appropriate system property to point to it as described above
  2. Set the configuration property `zookeeper.set.acl` in each broker to true

The metadata stored in ZooKeeper for the Kafka cluster is world-readable, but can only be modified by the brokers. The rationale behind this decision is that the data stored in ZooKeeper is not sensitive, but inappropriate manipulation of that data can cause cluster disruption. We also recommend limiting the access to ZooKeeper via network segmentation (only brokers and some admin tools need access to ZooKeeper if the new Java consumer and producer clients are used). 

## Migrating clusters

If you are running a version of Kafka that does not support security or simply with security disabled, and you want to make the cluster secure, then you need to execute the following steps to enable ZooKeeper authentication with minimal disruption to your operations: 

  1. Perform a rolling restart setting the JAAS login file, which enables brokers to authenticate. At the end of the rolling restart, brokers are able to manipulate znodes with strict ACLs, but they will not create znodes with those ACLs
  2. Perform a second rolling restart of brokers, this time setting the configuration parameter `zookeeper.set.acl` to true, which enables the use of secure ACLs when creating znodes
  3. Execute the ZkSecurityMigrator tool. To execute the tool, there is this script: `./bin/zookeeper-security-migration.sh` with `zookeeper.acl` set to secure. This tool traverses the corresponding sub-trees changing the ACLs of the znodes



It is also possible to turn off authentication in a secure cluster. To do it, follow these steps:

  1. Perform a rolling restart of brokers setting the JAAS login file, which enables brokers to authenticate, but setting `zookeeper.set.acl` to false. At the end of the rolling restart, brokers stop creating znodes with secure ACLs, but are still able to authenticate and manipulate all znodes
  2. Execute the ZkSecurityMigrator tool. To execute the tool, run this script `./bin/zookeeper-security-migration.sh` with `zookeeper.acl` set to unsecure. This tool traverses the corresponding sub-trees changing the ACLs of the znodes
  3. Perform a second rolling restart of brokers, this time omitting the system property that sets the JAAS login file

Here is an example of how to run the migration tool: 
    
    
        ./bin/zookeeper-security-migration --zookeeper.acl=secure --zookeeper.connect=localhost:2181
        

Run this to see the full list of parameters:
    
    
        ./bin/zookeeper-security-migration --help
        

## Migrating the ZooKeeper ensemble

It is also necessary to enable authentication on the ZooKeeper ensemble. To do it, we need to perform a rolling restart of the server and set a few properties. Please refer to the ZooKeeper documentation for more detail: 

  1. [Apache ZooKeeper documentation](http://zookeeper.apache.org/doc/r3.4.9/zookeeperProgrammers.html#sc_ZooKeeperAccessControl)
  2. [Apache ZooKeeper wiki](https://cwiki.apache.org/confluence/display/ZOOKEEPER/Zookeeper+and+SASL)


