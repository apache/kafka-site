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

  1. #### JAAS configuration

Kafka uses the Java Authentication and Authorization Service ([JAAS](https://docs.oracle.com/javase/8/docs/technotes/guides/security/jaas/JAASRefGuide.html)) for SASL configuration.

    1. ##### JAAS configuration for Kafka brokers

`KafkaServer` is the section name in the JAAS file used by each KafkaServer/Broker. This section provides SASL configuration options for the broker including any SASL client connections made by the broker for inter-broker communication. If multiple listeners are configured to use SASL, the section name may be prefixed with the listener name in lower-case followed by a period, e.g. `sasl_ssl.KafkaServer`.

`Client` section is used to authenticate a SASL connection with zookeeper. It also allows the brokers to set SASL ACL on zookeeper nodes which locks these nodes down so that only the brokers can modify it. It is necessary to have the same principal name across all brokers. If you want to use a section name other than Client, set the system property `zookeeper.sasl.clientconfig` to the appropriate name (_e.g._ , `-Dzookeeper.sasl.clientconfig=ZkClient`).

ZooKeeper uses "zookeeper" as the service name by default. If you want to change this, set the system property `zookeeper.sasl.client.username` to the appropriate name (_e.g._ , `-Dzookeeper.sasl.client.username=zk`).

Brokers may also configure JAAS using the broker configuration property `sasl.jaas.config`. The property name must be prefixed with the listener prefix including the SASL mechanism, i.e. `listener.name.{listenerName}.{saslMechanism}.sasl.jaas.config`. Only one login module may be specified in the config value. If multiple mechanisms are configured on a listener, configs must be provided for each mechanism using the listener and mechanism prefix. For example, 
        
                        listener.name.sasl_ssl.scram-sha-256.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
                    username="admin" \
                    password="admin-secret";
                listener.name.sasl_ssl.plain.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
                    username="admin" \
                    password="admin-secret" \
                    user_admin="admin-secret" \
                    user_alice="alice-secret";

If JAAS configuration is defined at different levels, the order of precedence used is: 
       * Broker configuration property `listener.name.{listenerName}.{saslMechanism}.sasl.jaas.config`
       * `{listenerName}.KafkaServer` section of static JAAS configuration`
       * `KafkaServer` section of static JAAS configuration`
Note that ZooKeeper JAAS config may only be configured using static JAAS configuration. 

See GSSAPI (Kerberos), PLAIN or SCRAM for example broker configurations.

    2. ##### JAAS configuration for Kafka clients

Clients may configure JAAS using the client configuration property sasl.jaas.config or using the static JAAS config file similar to brokers.

      1. ###### JAAS configuration using client configuration property

Clients may specify JAAS configuration as a producer or consumer property without creating a physical configuration file. This mode also enables different producers and consumers within the same JVM to use different credentials by specifying different properties for each client. If both static JAAS configuration system property `java.security.auth.login.config` and client property `sasl.jaas.config` are specified, the client property will be used.

See GSSAPI (Kerberos), PLAIN or SCRAM for example configurations.

      2. ###### JAAS configuration using static config file

To configure SASL authentication on the clients using static JAAS config file: 
        1. Add a JAAS config file with a client login section named `KafkaClient`. Configure a login module in `KafkaClient` for the selected mechanism as described in the examples for setting up GSSAPI (Kerberos), PLAIN or SCRAM. For example, GSSAPI credentials may be configured as: 
                
                                        KafkaClient {
                        com.sun.security.auth.module.Krb5LoginModule required
                        useKeyTab=true
                        storeKey=true
                        keyTab="/etc/security/keytabs/kafka_client.keytab"
                        principal="kafka-client-1@EXAMPLE.COM";
                    };

        2. Pass the JAAS config file location as JVM parameter to each client JVM. For example: 
                
                                    -Djava.security.auth.login.config=/etc/kafka/kafka_client_jaas.conf

  2. #### SASL configuration

SASL may be used with PLAINTEXT or SSL as the transport layer using the security protocol SASL_PLAINTEXT or SASL_SSL respectively. If SASL_SSL is used, then SSL must also be configured.

    1. ##### SASL mechanisms

Kafka supports the following SASL mechanisms: 
       * GSSAPI (Kerberos)
       * PLAIN
       * SCRAM-SHA-256
       * SCRAM-SHA-512
    2. ##### SASL configuration for Kafka brokers

      1. Configure a SASL port in server.properties, by adding at least one of SASL_PLAINTEXT or SASL_SSL to the _listeners_ parameter, which contains one or more comma-separated values: 
            
                            listeners=SASL_PLAINTEXT://host.name:port

If you are only configuring a SASL port (or if you want the Kafka brokers to authenticate each other using SASL) then make sure you set the same SASL protocol for inter-broker communication: 
            
                            security.inter.broker.protocol=SASL_PLAINTEXT (or SASL_SSL)

      2. Select one or more supported mechanisms to enable in the broker and follow the steps to configure SASL for the mechanism. To enable multiple mechanisms in the broker, follow the steps here.
    3. ##### SASL configuration for Kafka clients

SASL authentication is only supported for the new Java Kafka producer and consumer, the older API is not supported.

To configure SASL authentication on the clients, select a SASL mechanism that is enabled in the broker for client authentication and follow the steps to configure SASL for the selected mechanism.

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
      4. Configure SASL port and SASL mechanisms in server.properties as described here. For example: 
            
                            listeners=SASL_PLAINTEXT://host.name:port
                    security.inter.broker.protocol=SASL_PLAINTEXT
                    sasl.mechanism.inter.broker.protocol=GSSAPI
                    sasl.enabled.mechanisms=GSSAPI
                        

We must also configure the service name in server.properties, which should match the principal name of the kafka brokers. In the above example, principal is "kafka/kafka1.hostname.com@EXAMPLE.com", so: 
            
                            sasl.kerberos.service.name=kafka

    3. ##### Configuring Kafka Clients

To configure SASL authentication on the clients: 
      1. Clients (producers, consumers, connect workers, etc) will authenticate to the cluster with their own principal (usually with the same name as the user running the client), so obtain or create these principals as needed. Then configure the JAAS configuration property for each client. Different clients within a JVM may run as different users by specifiying different principals. The property `sasl.jaas.config` in producer.properties or consumer.properties describes how clients like producer and consumer can connect to the Kafka Broker. The following is an example configuration for a client using a keytab (recommended for long-running processes): 
            
                            sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
                    useKeyTab=true \
                    storeKey=true  \
                    keyTab="/etc/security/keytabs/kafka_client.keytab" \
                    principal="kafka-client-1@EXAMPLE.COM";

For command-line utilities like kafka-console-consumer or kafka-console-producer, kinit can be used along with "useTicketCache=true" as in: 
            
                            sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
                    useTicketCache=true;

JAAS configuration for clients may alternatively be specified as a JVM parameter similar to brokers as described here. Clients use the login section named `KafkaClient`. This option allows only one user for all client connections from a JVM.
      2. Make sure the keytabs configured in the JAAS configuration are readable by the operating system user who is starting kafka client.
      3. Optionally pass the krb5 file locations as JVM parameters to each client JVM (see [here](https://docs.oracle.com/javase/8/docs/technotes/guides/security/jgss/tutorials/KerberosReq.html) for more details): 
            
                            -Djava.security.krb5.conf=/etc/kafka/krb5.conf

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

      3. Configure SASL port and SASL mechanisms in server.properties as described here. For example: 
            
                            listeners=SASL_SSL://host.name:port
                    security.inter.broker.protocol=SASL_SSL
                    sasl.mechanism.inter.broker.protocol=PLAIN
                    sasl.enabled.mechanisms=PLAIN

    2. ##### Configuring Kafka Clients

To configure SASL authentication on the clients: 
      1. Configure the JAAS configuration property for each client in producer.properties or consumer.properties. The login module describes how the clients like producer and consumer can connect to the Kafka Broker. The following is an example configuration for a client for the PLAIN mechanism: 
            
                            sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
                    username="alice" \
                    password="alice-secret";

The options `username` and `password` are used by clients to configure the user for client connections. In this example, clients connect to the broker as user _alice_. Different clients within a JVM may connect as different users by specifying different user names and passwords in `sasl.jaas.config`.

JAAS configuration for clients may alternatively be specified as a JVM parameter similar to brokers as described here. Clients use the login section named `KafkaClient`. This option allows only one user for all client connections from a JVM.

      2. Configure the following properties in producer.properties or consumer.properties: 
            
                            security.protocol=SASL_SSL
                sasl.mechanism=PLAIN

    3. ##### Use of SASL/PLAIN in production

       * SASL/PLAIN should be used only with SSL as transport layer to ensure that clear passwords are not transmitted on the wire without encryption.
       * The default implementation of SASL/PLAIN in Kafka specifies usernames and passwords in the JAAS configuration file as shown here. To avoid storing passwords on disk, you can plug in your own implementation of `javax.security.auth.spi.LoginModule` that provides usernames and passwords from an external source. The login module implementation should provide username as the public credential and password as the private credential of the `Subject`. The default implementation `org.apache.kafka.common.security.plain.PlainLoginModule` can be used as an example.
       * In production systems, external authentication servers may implement password authentication. Kafka brokers can be integrated with these servers by adding your own implementation of `javax.security.sasl.SaslServer`. The default implementation included in Kafka in the package `org.apache.kafka.common.security.plain` can be used as an example to get started. 
         * New providers must be installed and registered in the JVM. Providers can be installed by adding provider classes to the normal `CLASSPATH` or bundled as a jar file and added to `_JAVA_HOME_ /lib/ext`.
         * Providers can be registered statically by adding a provider to the security properties file `_JAVA_HOME_ /lib/security/java.security`. 
                
                                    security.provider.n=providerClassName

where _providerClassName_ is the fully qualified name of the new provider and _n_ is the preference order with lower numbers indicating higher preference.
         * Alternatively, you can register providers dynamically at runtime by invoking `Security.addProvider` at the beginning of the client application or in a static initializer in the login module. For example: 
                
                                    Security.addProvider(new PlainSaslServerProvider());

         * For more details, see [JCA Reference](http://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html).
  5. #### Authentication using SASL/SCRAM

Salted Challenge Response Authentication Mechanism (SCRAM) is a family of SASL mechanisms that addresses the security concerns with traditional mechanisms that perform username/password authentication like PLAIN and DIGEST-MD5. The mechanism is defined in [RFC 5802](https://tools.ietf.org/html/rfc5802). Kafka supports [SCRAM-SHA-256](https://tools.ietf.org/html/rfc7677) and SCRAM-SHA-512 which can be used with TLS to perform secure authentication. The username is used as the authenticated `Principal` for configuration of ACLs etc. The default SCRAM implementation in Kafka stores SCRAM credentials in Zookeeper and is suitable for use in Kafka installations where Zookeeper is on a private network. Refer to Security Considerations for more details.

    1. ##### Creating SCRAM Credentials

The SCRAM implementation in Kafka uses Zookeeper as credential store. Credentials can be created in Zookeeper using `kafka-configs.sh`. For each SCRAM mechanism enabled, credentials must be created by adding a config with the mechanism name. Credentials for inter-broker communication must be created before Kafka brokers are started. Client credentials may be created and updated dynamically and updated credentials will be used to authenticate new connections.

Create SCRAM credentials for user _alice_ with password _alice-secret_ : 
        
                    > bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-256=[iterations=8192,password=alice-secret],SCRAM-SHA-512=[password=alice-secret]' --entity-type users --entity-name alice
                

The default iteration count of 4096 is used if iterations are not specified. A random salt is created and the SCRAM identity consisting of salt, iterations, StoredKey and ServerKey are stored in Zookeeper. See [RFC 5802](https://tools.ietf.org/html/rfc5802) for details on SCRAM identity and the individual fields. 

The following examples also require a user _admin_ for inter-broker communication which can be created using: 
        
                    > bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-256=[password=admin-secret],SCRAM-SHA-512=[password=admin-secret]' --entity-type users --entity-name admin
                

Existing credentials may be listed using the _\--describe_ option: 
        
                    > bin/kafka-configs.sh --zookeeper localhost:2181 --describe --entity-type users --entity-name alice
                

Credentials may be deleted for one or more SCRAM mechanisms using the _\--delete_ option: 
        
                    > bin/kafka-configs.sh --zookeeper localhost:2181 --alter --delete-config 'SCRAM-SHA-512' --entity-type users --entity-name alice
                

    2. ##### Configuring Kafka Brokers

      1. Add a suitably modified JAAS file similar to the one below to each Kafka broker's config directory, let's call it kafka_server_jaas.conf for this example: 
            
                            KafkaServer {
                    org.apache.kafka.common.security.scram.ScramLoginModule required
                    username="admin"
                    password="admin-secret";
                };

The properties `username` and `password` in the `KafkaServer` section are used by the broker to initiate connections to other brokers. In this example, _admin_ is the user for inter-broker communication.
      2. Pass the JAAS config file location as JVM parameter to each Kafka broker: 
            
                            -Djava.security.auth.login.config=/etc/kafka/kafka_server_jaas.conf

      3. Configure SASL port and SASL mechanisms in server.properties as described here.`

For example: 
            
                            listeners=SASL_SSL://host.name:port
                security.inter.broker.protocol=SASL_SSL
                sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256 (or SCRAM-SHA-512)
                sasl.enabled.mechanisms=SCRAM-SHA-256 (or SCRAM-SHA-512)

    3. ##### Configuring Kafka Clients

To configure SASL authentication on the clients: 
      1. Configure the JAAS configuration property for each client in producer.properties or consumer.properties. The login module describes how the clients like producer and consumer can connect to the Kafka Broker. The following is an example configuration for a client for the SCRAM mechanisms: 
            
                           sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
                    username="alice" \
                    password="alice-secret";

The options `username` and `password` are used by clients to configure the user for client connections. In this example, clients connect to the broker as user _alice_. Different clients within a JVM may connect as different users by specifying different user names and passwords in `sasl.jaas.config`.

JAAS configuration for clients may alternatively be specified as a JVM parameter similar to brokers as described here. Clients use the login section named `KafkaClient`. This option allows only one user for all client connections from a JVM.

      2. Configure the following properties in producer.properties or consumer.properties: 
            
                            security.protocol=SASL_SSL
                sasl.mechanism=SCRAM-SHA-256 (or SCRAM-SHA-512)

    4. ##### Security Considerations for SASL/SCRAM

       * The default implementation of SASL/SCRAM in Kafka stores SCRAM credentials in Zookeeper. This is suitable for production use in installations where Zookeeper is secure and on a private network.
       * Kafka supports only the strong hash functions SHA-256 and SHA-512 with a minimum iteration count of 4096. Strong hash functions combined with strong passwords and high iteration counts protect against brute force attacks if Zookeeper security is compromised.
       * SCRAM should be used only with TLS-encryption to prevent interception of SCRAM exchanges. This protects against dictionary or brute force attacks and against impersonation if Zookeeper is compromised.
       * The default SASL/SCRAM implementation may be overridden using custom login modules in installations where Zookeeper is not secure. See here for details.
       * For more details on security considerations, refer to [RFC 5802](https://tools.ietf.org/html/rfc5802#section-9). 
  6. #### Enabling multiple SASL mechanisms in a broker

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
        
                    sasl.enabled.mechanisms=GSSAPI,PLAIN,SCRAM-SHA-256,SCRAM-SHA-512

    3. Specify the SASL security protocol and mechanism for inter-broker communication in server.properties if required: 
        
                    security.inter.broker.protocol=SASL_PLAINTEXT (or SASL_SSL)
            sasl.mechanism.inter.broker.protocol=GSSAPI (or one of the other enabled mechanisms)

    4. Follow the mechanism-specific steps in GSSAPI (Kerberos), PLAIN and SCRAM to configure SASL for the enabled mechanisms.
  7. #### Modifying SASL mechanism in a Running Cluster

SASL mechanism can be modified in a running cluster using the following sequence:

    1. Enable new SASL mechanism by adding the mechanism to `sasl.enabled.mechanisms` in server.properties for each broker. Update JAAS config file to include both mechanisms as described here. Incrementally bounce the cluster nodes.
    2. Restart clients using the new mechanism.
    3. To change the mechanism of inter-broker communication (if this is required), set `sasl.mechanism.inter.broker.protocol` in server.properties to the new mechanism and incrementally bounce the cluster again.
    4. To remove old mechanism (if this is required), remove the old mechanism from `sasl.enabled.mechanisms` in server.properties and remove the entries for the old mechanism from JAAS config file. Incrementally bounce the cluster again.
  8. #### Authentication using Delegation Tokens

Delegation token based authentication is a lightweight authentication mechanism to complement existing SASL/SSL methods. Delegation tokens are shared secrets between kafka brokers and clients. Delegation tokens will help processing frameworks to distribute the workload to available workers in a secure environment without the added cost of distributing Kerberos TGT/keytabs or keystores when 2-way SSL is used. See [KIP-48](https://cwiki.apache.org/confluence/display/KAFKA/KIP-48+Delegation+token+support+for+Kafka) for more details.

Typical steps for delegation token usage are:

    1. User authenticates with the Kafka cluster via SASL or SSL, and obtains a delegation token. This can be done using AdminClient APIs or using `kafka-delegation-token.sh` script.
    2. User securely passes the delegation token to Kafka clients for authenticating with the Kafka cluster.
    3. Token owner/renewer can renew/expire the delegation tokens.
    1. ##### Token Management

A master key/secret is used to generate and verify delegation tokens. This is supplied using config option `delegation.token.master.key`. Same secret key must be configured across all the brokers. If the secret is not set or set to empty string, brokers will disable the delegation token authentication.

In current implementation, token details are stored in Zookeeper and is suitable for use in Kafka installations where Zookeeper is on a private network. Also currently, master key/secret is stored as plain text in server.properties config file. We intend to make these configurable in a future Kafka release.

A token has a current life, and a maximum renewable life. By default, tokens must be renewed once every 24 hours for up to 7 days. These can be configured using `delegation.token.expiry.time.ms` and `delegation.token.max.lifetime.ms` config options.

Tokens can also be cancelled explicitly. If a token is not renewed by the token’s expiration time or if token is beyond the max life time, it will be deleted from all broker caches as well as from zookeeper.

    2. ##### Creating Delegation Tokens

Tokens can be created by using AdminClient APIs or using `kafka-delegation-token.sh` script. Delegation token requests (create/renew/expire/describe) should be issued only on SASL or SSL authenticated channels. Tokens can not be requests if the initial authentication is done through delegation token. `kafka-delegation-token.sh` script examples are given below.

Create a delegation token: 
        
                    > bin/kafka-delegation-tokens.sh --bootstrap-server localhost:9092 --create   --max-life-time-period -1 --command-config client.properties --renewer-principal User:user1
                

Renew a delegation token: 
        
                    > bin/kafka-delegation-tokens.sh --bootstrap-server localhost:9092 --renew    --renew-time-period -1 --command-config client.properties --hmac ABCDEFGHIJK
                

Expire a delegation token: 
        
                    > bin/kafka-delegation-tokens.sh --bootstrap-server localhost:9092 --expire   --expiry-time-period -1   --command-config client.properties  --hmac ABCDEFGHIJK
                

Existing tokens can be described using the --describe option: 
        
                    > bin/kafka-delegation-tokens.sh --bootstrap-server localhost:9092 --describe --command-config client.properties  --owner-principal User:user1
                

    3. ##### Token Authentication

Delegation token authentication piggybacks on the current SASL/SCRAM authentication mechanism. We must enable SASL/SCRAM mechanism on Kafka cluster as described in here.

Configuring Kafka Clients:

      1. Configure the JAAS configuration property for each client in producer.properties or consumer.properties. The login module describes how the clients like producer and consumer can connect to the Kafka Broker. The following is an example configuration for a client for the token authentication: 
            
                           sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
                    username="tokenID123" \
                    password="lAYYSFmLs4bTjf+lTZ1LCHR/ZZFNA==" \
                    tokenauth="true";

The options `username` and `password` are used by clients to configure the token id and token HMAC. And the option `tokenauth` is used to indicate the server about token authentication. In this example, clients connect to the broker using token id: _tokenID123_. Different clients within a JVM may connect using different tokens by specifying different token details in `sasl.jaas.config`.

JAAS configuration for clients may alternatively be specified as a JVM parameter similar to brokers as described here. Clients use the login section named `KafkaClient`. This option allows only one user for all client connections from a JVM.

    4. ##### Procedure to manually rotate the secret:

We require a re-deployment when the secret needs to be rotated. During this process, already connected clients will continue to work. But any new connection requests and renew/expire requests with old tokens can fail. Steps are given below.

      1. Expire all existing tokens.
      2. Rotate the secret by rolling upgrade, and
      3. Generate new tokens

We intend to automate this in a future Kafka release.

    5. ##### Notes on Delegation Tokens

       * Currently, we only allow a user to create delegation token for that user only. Owner/Renewers can renew or expire tokens. Owner/renewers can always describe their own tokens. To describe others tokens, we need to add DESCRIBE permission on Token Resource.


