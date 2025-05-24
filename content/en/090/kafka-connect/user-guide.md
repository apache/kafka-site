---
title: User Guide
description: User Guide
weight: 2
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# User Guide

The quickstart provides a brief example of how to run a standalone version of Kafka Connect. This section describes how to configure, run, and manage Kafka Connect in more detail. 

## Running Kafka Connect

Kafka Connect currently supports two modes of execution: standalone (single process) and distributed. In standalone mode all work is performed in a single process. This configuration is simpler to setup and get started with and may be useful in situations where only one worker makes sense (e.g. collecting log files), but it does not benefit from some of the features of Kafka Connect such as fault tolerance. You can start a standalone process with the following command: 
    
    
    > bin/connect-standalone.sh config/connect-standalone.properties connector1.properties [connector2.properties ...]
    

The first parameter is the configuration for the worker. This includes settings such as the Kafka connection parameters, serialization format, and how frequently to commit offsets. The provided example should work well with a local cluster running with the default configuration provided by `config/server.properties`. It will require tweaking to use with a different configuration or production deployment. The remaining parameters are connector configuration files. You may include as many as you want, but all will execute within the same process (on different threads). Distributed mode handles automatic balancing of work, allows you to scale up (or down) dynamically, and offers fault tolerance both in the active tasks and for configuration and offset commit data. Execution is very similar to standalone mode: 
    
    
    > bin/connect-distributed.sh config/connect-distributed.properties
    

The difference is in the class which is started and the configuration parameters which change how the Kafka Connect process decides where to store configurations, how to assign work, and where to store offsets. In particular, the following configuration parameters are critical to set before starting your cluster: 

  * `group.id` (default `connect-cluster`) - unique name for the cluster, used in forming the Connect cluster group; note that this **must not conflict** with consumer group IDs
  * `config.storage.topic` (default `connect-configs`) - topic to use for storing connector and task configurations; note that this should be a single partition, highly replicated topic
  * `offset.storage.topic` (default `connect-offsets`) - topic to use for ; this topic should have many partitions and be replicated

Note that in distributed mode the connector configurations are not passed on the command line. Instead, use the REST API described below to create, modify, and destroy connectors. 

## Configuring Connectors

Connector configurations are simple key-value mappings. For standalone mode these are defined in a properties file and passed to the Connect process on the command line. In distributed mode, they will be included in the JSON payload for the request that creates (or modifies) the connector. Most configurations are connector dependent, so they can't be outlined here. However, there are a few common options: 

  * `name` \- Unique name for the connector. Attempting to register again with the same name will fail.
  * `connector.class` \- The Java class for the connector
  * `tasks.max` \- The maximum number of tasks that should be created for this connector. The connector may create fewer tasks if it cannot achieve this level of parallelism.

Sink connectors also have one additional option to control their input: 
  * `topics` \- A list of topics to use as input for this connector

For any other options, you should consult the documentation for the connector. 

## REST API

Since Kafka Connect is intended to be run as a service, it also supports a REST API for managing connectors. By default this service runs on port 8083. The following are the currently supported endpoints: 

  * `GET /connectors` \- return a list of active connectors
  * `POST /connectors` \- create a new connector; the request body should be a JSON object containing a string `name` field and a object `config` field with the connector configuration parameters
  * `GET /connectors/{name}` \- get information about a specific connector
  * `GET /connectors/{name}/config` \- get the configuration parameters for a specific connector
  * `PUT /connectors/{name}/config` \- update the configuration parameters for a specific connector
  * `GET /connectors/{name}/tasks` \- get a list of tasks currently running for a connector
  * `DELETE /connectors/{name}` \- delete a connector, halting all tasks and deleting its configuration


