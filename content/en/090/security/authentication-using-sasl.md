---
title: Authentication using SASL
description: Authentication using SASL
weight: 3
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Authentication using SASL

  1. #### Prerequisites

    1. **Kerberos**  
If your organization is already using a Kerberos server (for example, by using Active Directory), there is no need to install a new server just for Kafka. Otherwise you will need to install one, your Linux vendor likely has packages for Kerberos and a short guide on how to install and configure it ([Ubuntu](https://help.ubuntu.com/community/Kerberos), [Redhat](https://access.redhat.com/en-US/Red_Hat_Enterprise_Linux/6/html/Managing_Smart_Cards/installing-kerberos.html)). Note that if you are using Oracle Java, you will need to download JCE policy files for your Java version and copy them to $JAVA_HOME/jre/lib/security.
    2. **Create Kerberos Principals**  
If you are using the organization's Kerberos or Active Directory server, ask your Kerberos administrator for a principal for each Kafka broker in your cluster and for every operating system user that will access Kafka with Kerberos authentication (via clients and tools). If you have installed your own Kerberos, you will need to create these principals yourself using the following commands: 
        
                    sudo /usr/sbin/kadmin.local -q 'addprinc -randkey kafka/{hostname}@{REALM}'
            sudo /usr/sbin/kadmin.local -q "ktadd -k /etc/security/keytabs/{keytabname}.keytab kafka/{hostname}@{REALM}"

    3. **Make sure all hosts can be reachable using hostnames** \- it is a Kerberos requirement that all your hosts can be resolved with their FQDNs.
  2. #### Configuring Kafka Brokers

    1. Add a suitably modified JAAS file similar to the one below to each Kafka broker's config directory, let's call it kafka_server_jaas.conf for this example (note that each broker should have its own keytab): 
        
                    KafkaServer {
                com.sun.security.auth.module.Krb5LoginModule required
                useKeyTab=true
                storeKey=true
                keyTab="/etc/security/keytabs/kafka_server.keytab"
                principal="kafka/kafka1.hostname.com@EXAMPLE.COM";
            };
        
            // Zookeeper client authentication
            Client {
               com.sun.security.auth.module.Krb5LoginModule required
               useKeyTab=true
               storeKey=true
               keyTab="/etc/security/keytabs/kafka_server.keytab"
               principal="kafka/kafka1.hostname.com@EXAMPLE.COM";
            };

    2. Pass the JAAS and optionally the krb5 file locations as JVM parameters to each Kafka broker (see [here](https://docs.oracle.com/javase/8/docs/technotes/guides/security/jgss/tutorials/KerberosReq.html) for more details): 
        
                    -Djava.security.krb5.conf=/etc/kafka/krb5.conf
            -Djava.security.auth.login.config=/etc/kafka/kafka_server_jaas.conf

    3. Make sure the keytabs configured in the JAAS file are readable by the operating system user who is starting kafka broker.
    4. Configure a SASL port in server.properties, by adding at least one of SASL_PLAINTEXT or SASL_SSL to the _listeners_ parameter, which contains one or more comma-separated values: 
        
                    listeners=SASL_PLAINTEXT://host.name:port

If SASL_SSL is used, then SSL must also be configured. If you are only configuring a SASL port (or if you want the Kafka brokers to authenticate each other using SASL) then make sure you set the same SASL protocol for inter-broker communication: 
        
                    security.inter.broker.protocol=SASL_PLAINTEXT (or SASL_SSL)

We must also configure the service name in server.properties, which should match the principal name of the kafka brokers. In the above example, principal is "kafka/kafka1.hostname.com@EXAMPLE.com", so: 
        
                    sasl.kerberos.service.name=kafka

_Important notes:_
      1. KafkaServer is a section name in JAAS file used by each KafkaServer/Broker. This section tells the broker which principal to use and the location of the keytab where this principal is stored. It allows the broker to login using the keytab specified in this section.
      2. Client section is used to authenticate a SASL connection with zookeeper. It also allows the brokers to set SASL ACL on zookeeper nodes which locks these nodes down so that only the brokers can modify it. It is necessary to have the same principal name across all brokers. If you want to use a section name other than Client, set the system property `zookeeper.sasl.client` to the appropriate name (_e.g._ , `-Dzookeeper.sasl.client=ZkClient`).
      3. ZooKeeper uses "zookeeper" as the service name by default. If you want to change this, set the system property `zookeeper.sasl.client.username` to the appropriate name (_e.g._ , `-Dzookeeper.sasl.client.username=zk`).
  3. #### Configuring Kafka Clients

SASL authentication is only supported for the new kafka producer and consumer, the older API is not supported. To configure SASL authentication on the clients: 
    1. Clients (producers, consumers, connect workers, etc) will authenticate to the cluster with their own principal (usually with the same name as the user running the client), so obtain or create these principals as needed. Then create a JAAS file for each principal. The KafkaClient section describes how the clients like producer and consumer can connect to the Kafka Broker. The following is an example configuration for a client using a keytab (recommended for long-running processes): 
        
                    KafkaClient {
                com.sun.security.auth.module.Krb5LoginModule required
                useKeyTab=true
                storeKey=true
                keyTab="/etc/security/keytabs/kafka_client.keytab"
                principal="kafka-client-1@EXAMPLE.COM";
            };

For command-line utilities like kafka-console-consumer or kafka-console-producer, kinit can be used along with "useTicketCache=true" as in: 
        
                    KafkaClient {
                com.sun.security.auth.module.Krb5LoginModule required
                useTicketCache=true;
            };

    2. Pass the JAAS and optionally krb5 file locations as JVM parameters to each client JVM (see [here](https://docs.oracle.com/javase/8/docs/technotes/guides/security/jgss/tutorials/KerberosReq.html) for more details): 
        
                    -Djava.security.krb5.conf=/etc/kafka/krb5.conf
            -Djava.security.auth.login.config=/etc/kafka/kafka_client_jaas.conf

    3. Make sure the keytabs configured in the kafka_client_jaas.conf are readable by the operating system user who is starting kafka client.
    4. Configure the following properties in producer.properties or consumer.properties: 
        
                    security.protocol=SASL_PLAINTEXT (or SASL_SSL)
            sasl.kerberos.service.name=kafka

  4. #### Incorporating Security Features in a Running Cluster

You can secure a running cluster via one or more of the supported protocols discussed previously. This is done in phases: 

     * Incrementally bounce the cluster nodes to open additional secured port(s).
     * Restart clients using the secured rather than PLAINTEXT port (assuming you are securing the client-broker connection).
     * Incrementally bounce the cluster again to enable broker-to-broker security (if this is required)
     * A final incremental bounce to close the PLAINTEXT port.

The specific steps for configuring SSL and SASL are described in sections 7.2 and 7.3. Follow these steps to enable security for your desired protocol(s). 

The security implementation lets you configure different protocols for both broker-client and broker-broker communication. These must be enabled in separate bounces. A PLAINTEXT port must be left open throughout so brokers and/or clients can continue to communicate. 

When performing an incremental bounce stop the brokers cleanly via a SIGTERM. It's also good practice to wait for restarted replicas to return to the ISR list before moving onto the next node. 

As an example, say we wish to encrypt both broker-client and broker-broker communication with SSL. In the first incremental bounce, a SSL port is opened on each node: 
    
                 listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092

We then restart the clients, changing their config to point at the newly opened, secured port: 
    
                bootstrap.servers = [broker1:9092,...]
            security.protocol = SSL
            ...etc

In the second incremental server bounce we instruct Kafka to use SSL as the broker-broker protocol (which will use the same SSL port): 
    
                listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092
            security.inter.broker.protocol=SSL

In the final bounce we secure the cluster by closing the PLAINTEXT port: 
    
                listeners=SSL://broker1:9092
            security.inter.broker.protocol=SSL

Alternatively we might choose to open multiple ports so that different protocols can be used for broker-broker and broker-client communication. Say we wished to use SSL encryption throughout (i.e. for broker-broker and broker-client communication) but we'd like to add SASL authentication to the broker-client connection also. We would achieve this by opening two additional ports during the first bounce: 
    
                listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092,SASL_SSL://broker1:9093

We would then restart the clients, changing their config to point at the newly opened, SASL & SSL secured port: 
    
                bootstrap.servers = [broker1:9093,...]
            security.protocol = SASL_SSL
            ...etc

The second server bounce would switch the cluster to use encrypted broker-broker communication via the SSL port we previously opened on port 9092: 
    
                listeners=PLAINTEXT://broker1:9091,SSL://broker1:9092,SASL_SSL://broker1:9093
            security.inter.broker.protocol=SSL

The final bounce secures the cluster by closing the PLAINTEXT port. 
    
               listeners=SSL://broker1:9092,SASL_SSL://broker1:9093
           security.inter.broker.protocol=SSL

ZooKeeper can be secured independently of the Kafka cluster. The steps for doing this are covered in section 7.5.2. 


