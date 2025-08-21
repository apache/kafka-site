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

  1. #### SASL configuration for Kafka brokers

    1. Select one or more supported mechanisms to enable in the broker. `GSSAPI` and `PLAIN` are the mechanisms currently supported in Kafka.
    2. Add a JAAS config file for the selected mechanisms as described in the examples for setting up GSSAPI (Kerberos) or PLAIN.
    3. Pass the JAAS config file location as JVM parameter to each Kafka broker. For example: 
        
                    -Djava.security.auth.login.config=/etc/kafka/kafka_server_jaas.conf

    4. Configure a SASL port in server.properties, by adding at least one of SASL_PLAINTEXT or SASL_SSL to the _listeners_ parameter, which contains one or more comma-separated values: 
        
                    listeners=SASL_PLAINTEXT://host.name:port

If SASL_SSL is used, then SSL must also be configured. If you are only configuring a SASL port (or if you want the Kafka brokers to authenticate each other using SASL) then make sure you set the same SASL protocol for inter-broker communication: 
        
                    security.inter.broker.protocol=SASL_PLAINTEXT (or SASL_SSL)

    5. Enable one or more SASL mechanisms in server.properties: 
        
                    sasl.enabled.mechanisms=GSSAPI (,PLAIN)

    6. Configure the SASL mechanism for inter-broker communication in server.properties if using SASL for inter-broker communication: 
        
                    sasl.mechanism.inter.broker.protocol=GSSAPI (or PLAIN)

    7. Follow the steps in GSSAPI (Kerberos) or PLAIN to configure SASL for the enabled mechanisms. To enable multiple mechanisms in the broker, follow the steps here.
_Important notes:_
      1. `KafkaServer` is the section name in the JAAS file used by each KafkaServer/Broker. This section provides SASL configuration options for the broker including any SASL client connections made by the broker for inter-broker communication.
      2. `Client` section is used to authenticate a SASL connection with zookeeper. It also allows the brokers to set SASL ACL on zookeeper nodes which locks these nodes down so that only the brokers can modify it. It is necessary to have the same principal name across all brokers. If you want to use a section name other than Client, set the system property `zookeeper.sasl.client` to the appropriate name (_e.g._ , `-Dzookeeper.sasl.client=ZkClient`).
      3. ZooKeeper uses "zookeeper" as the service name by default. If you want to change this, set the system property `zookeeper.sasl.client.username` to the appropriate name (_e.g._ , `-Dzookeeper.sasl.client.username=zk`).
  2. #### SASL configuration for Kafka clients

SASL authentication is only supported for the new Java Kafka producer and consumer, the older API is not supported. To configure SASL authentication on the clients: 
    1. Select a SASL mechanism for authentication.
    2. Add a JAAS config file for the selected mechanism as described in the examples for setting up GSSAPI (Kerberos) or PLAIN. `KafkaClient` is the section name in the JAAS file used by Kafka clients.
    3. Pass the JAAS config file location as JVM parameter to each client JVM. For example: 
        
                    -Djava.security.auth.login.config=/etc/kafka/kafka_client_jaas.conf

    4. Configure the following properties in producer.properties or consumer.properties: 
        
                    security.protocol=SASL_PLAINTEXT (or SASL_SSL)
            sasl.mechanism=GSSAPI (or PLAIN)

    5. Follow the steps in GSSAPI (Kerberos) or PLAIN to configure SASL for the selected mechanism.
  3. #### Authentication using SASL/Kerberos

    1. ##### Prerequisites

      1. **Kerberos**  
If your organization is already using a Kerberos server (for example, by using Active Directory), there is no need to install a new server just for Kafka. Otherwise you will need to install one, your Linux vendor likely has packages for Kerberos and a short guide on how to install and configure it ([Ubuntu](https://help.ubuntu.com/community/Kerberos), [Redhat](https://access.redhat.com/en-US/Red_Hat_Enterprise_Linux/6/html/Managing_Smart_Cards/installing-kerberos.html)). Note that if you are using Oracle Java, you will need to download JCE policy files for your Java version and copy them to $JAVA_HOME/jre/lib/security.
      2. **Create Kerberos Principals**  
If you are using the organization's Kerberos or Active Directory server, ask your Kerberos administrator for a principal for each Kafka broker in your cluster and for every operating system user that will access Kafka with Kerberos authentication (via clients and tools). If you have installed your own Kerberos, you will need to create these principals yourself using the following commands: 
            
                            sudo /usr/sbin/kadmin.local -q 'addprinc -randkey kafka/{hostname}@{REALM}'
                sudo /usr/sbin/kadmin.local -q "ktadd -k /etc/security/keytabs/{keytabname}.keytab kafka/{hostname}@{REALM}"

      3. **Make sure all hosts can be reachable using hostnames** \- it is a Kerberos requirement that all your hosts can be resolved with their FQDNs.
    2. ##### Configuring Kafka Brokers

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

`KafkaServer` section in the JAAS file tells the broker which principal to use and the location of the keytab where this principal is stored. It allows the broker to login using the keytab specified in this section. See notes for more details on Zookeeper SASL configuration. 
      2. Pass the JAAS and optionally the krb5 file locations as JVM parameters to each Kafka broker (see [here](https://docs.oracle.com/javase/8/docs/technotes/guides/security/jgss/tutorials/KerberosReq.html) for more details): 
            
                            -Djava.security.krb5.conf=/etc/kafka/krb5.conf
                -Djava.security.auth.login.config=/etc/kafka/kafka_server_jaas.conf

      3. Make sure the keytabs configured in the JAAS file are readable by the operating system user who is starting kafka broker.
      4. Configure SASL port and SASL mechanisms in server.properties as described here.

For example: 
            
                            listeners=SASL_PLAINTEXT://host.name:port
                security.inter.broker.protocol=SASL_PLAINTEXT
                sasl.mechanism.inter.broker.protocol=GSSAPI
                sasl.enabled.mechanisms=GSSAPI
                      

We must also configure the service name in server.properties, which should match the principal name of the kafka brokers. In the above example, principal is "kafka/kafka1.hostname.com@EXAMPLE.com", so: 
            
                            sasl.kerberos.service.name=kafka

    3. ##### Configuring Kafka Clients

To configure SASL authentication on the clients: 
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
                sasl.mechanism=GSSAPI
                sasl.kerberos.service.name=kafka

  4. #### Authentication using SASL/PLAIN

SASL/PLAIN is a simple username/password authentication mechanism that is typically used with TLS for encryption to implement secure authentication. Kafka supports a default implementation for SASL/PLAIN which can be extended for production use as described here.

The username is used as the authenticated `Principal` for configuration of ACLs etc. 
    1. ##### Configuring Kafka Brokers

      1. Add a suitably modified JAAS file similar to the one below to each Kafka broker's config directory, let's call it kafka_server_jaas.conf for this example: 
            
                            KafkaServer {
                    org.apache.kafka.common.security.plain.PlainLoginModule required
                    username="admin"
                    password="admin-secret"
                    user_admin="admin-secret"
                    user_alice="alice-secret";
                };

This configuration defines two users (_admin_ and _alice_). The properties `username` and `password` in the `KafkaServer` section are used by the broker to initiate connections to other brokers. In this example, _admin_ is the user for inter-broker communication. The set of properties `user__userName_` defines the passwords for all users that connect to the broker and the broker validates all client connections including those from other brokers using these properties.
      2. Pass the JAAS config file location as JVM parameter to each Kafka broker: 
            
                            -Djava.security.auth.login.config=/etc/kafka/kafka_server_jaas.conf

      3. Configure SASL port and SASL mechanisms in server.properties as described here.

For example: 
            
                            listeners=SASL_SSL://host.name:port
                security.inter.broker.protocol=SASL_SSL
                sasl.mechanism.inter.broker.protocol=PLAIN
                sasl.enabled.mechanisms=PLAIN

    2. ##### Configuring Kafka Clients

To configure SASL authentication on the clients: 
      1. The `KafkaClient` section describes how the clients like producer and consumer can connect to the Kafka Broker. The following is an example configuration for a client for the PLAIN mechanism: 
            
                            KafkaClient {
                    org.apache.kafka.common.security.plain.PlainLoginModule required
                    username="alice"
                    password="alice-secret";
                };

The properties `username` and `password` in the `KafkaClient` section are used by clients to configure the user for client connections. In this example, clients connect to the broker as user _alice_. 
      2. Pass the JAAS config file location as JVM parameter to each client JVM: 
            
                            -Djava.security.auth.login.config=/etc/kafka/kafka_client_jaas.conf

      3. Configure the following properties in producer.properties or consumer.properties: 
            
                            security.protocol=SASL_SSL
                sasl.mechanism=PLAIN

    3. ##### Use of SASL/PLAIN in production

       * SASL/PLAIN should be used only with SSL as transport layer to ensure that clear passwords are not transmitted on the wire without encryption.
       * The default implementation of SASL/PLAIN in Kafka specifies usernames and passwords in the JAAS configuration file as shown here. To avoid storing passwords on disk, you can plugin your own implementation of `javax.security.auth.spi.LoginModule` that provides usernames and passwords from an external source. The login module implementation should provide username as the public credential and password as the private credential of the `Subject`. The default implementation `org.apache.kafka.common.security.plain.PlainLoginModule` can be used as an example.
       * In production systems, external authentication servers may implement password authentication. Kafka brokers can be integrated with these servers by adding your own implementation of `javax.security.sasl.SaslServer`. The default implementation included in Kafka in the package `org.apache.kafka.common.security.plain` can be used as an example to get started. 
         * New providers must be installed and registered in the JVM. Providers can be installed by adding provider classes to the normal `CLASSPATH` or bundled as a jar file and added to `_JAVA_HOME_ /lib/ext`.
         * Providers can be registered statically by adding a provider to the security properties file `_JAVA_HOME_ /lib/security/java.security`. 
                
                                    security.provider.n=providerClassName

where _providerClassName_ is the fully qualified name of the new provider and _n_ is the preference order with lower numbers indicating higher preference.
         * Alternatively, you can register providers dynamically at runtime by invoking `Security.addProvider` at the beginning of the client application or in a static initializer in the login module. For example: 
                
                                    Security.addProvider(new PlainSaslServerProvider());

         * For more details, see [JCA Reference](http://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html).
  5. #### Enabling multiple SASL mechanisms in a broker

    1. Specify configuration for the login modules of all enabled mechanisms in the `KafkaServer` section of the JAAS config file. For example: 
        
                    KafkaServer {
                com.sun.security.auth.module.Krb5LoginModule required
                useKeyTab=true
                storeKey=true
                keyTab="/etc/security/keytabs/kafka_server.keytab"
                principal="kafka/kafka1.hostname.com@EXAMPLE.COM";
        
                org.apache.kafka.common.security.plain.PlainLoginModule required
                username="admin"
                password="admin-secret"
                user_admin="admin-secret"
                user_alice="alice-secret";
            };

    2. Enable the SASL mechanisms in server.properties: 
        
                    sasl.enabled.mechanisms=GSSAPI,PLAIN

    3. Specify the SASL security protocol and mechanism for inter-broker communication in server.properties if required: 
        
                    security.inter.broker.protocol=SASL_PLAINTEXT (or SASL_SSL)
            sasl.mechanism.inter.broker.protocol=GSSAPI (or PLAIN)

    4. Follow the mechanism-specific steps in GSSAPI (Kerberos) and PLAIN to configure SASL for the enabled mechanisms.
  6. #### Modifying SASL mechanism in a Running Cluster

SASL mechanism can be modified in a running cluster using the following sequence:

    1. Enable new SASL mechanism by adding the mechanism to `sasl.enabled.mechanisms` in server.properties for each broker. Update JAAS config file to include both mechanisms as described here. Incrementally bounce the cluster nodes.
    2. Restart clients using the new mechanism.
    3. To change the mechanism of inter-broker communication (if this is required), set `sasl.mechanism.inter.broker.protocol` in server.properties to the new mechanism and incrementally bounce the cluster again.
    4. To remove old mechanism (if this is required), remove the old mechanism from `sasl.enabled.mechanisms` in server.properties and remove the entries for the old mechanism from JAAS config file. Incrementally bounce the cluster again.


