---
title: Security Overview
description: Security Overview
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Security Overview

In release 0.9.0.0, the Kafka community added a number of features that, used either separately or together, increases security in a Kafka cluster. These features are considered to be of beta quality. The following security measures are currently supported: 

  1. Authentication of connections to brokers from clients (producers and consumers), other brokers and tools, using either SSL or SASL (Kerberos). SASL/PLAIN can also be used from release 0.10.0.0 onwards.
  2. Authentication of connections from brokers to ZooKeeper
  3. Encryption of data transferred between brokers and clients, between brokers, or between brokers and tools using SSL (Note that there is a performance degradation when SSL is enabled, the magnitude of which depends on the CPU type and the JVM implementation.)
  4. Authorization of read / write operations by clients
  5. Authorization is pluggable and integration with external authorization services is supported

It's worth noting that security is optional - non-secured clusters are supported, as well as a mix of authenticated, unauthenticated, encrypted and non-encrypted clients. The guides below explain how to configure and use the security features in both clients and brokers. 
