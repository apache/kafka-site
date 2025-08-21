---
title: Authorization and ACLs
description: Authorization and ACLs
weight: 4
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Authorization and ACLs

Kafka ships with a pluggable Authorizer and an out-of-box authorizer implementation that uses zookeeper to store all the acls. Kafka acls are defined in the general format of "Principal P is [Allowed/Denied] Operation O From Host H On Resource R". You can read more about the acl structure on KIP-11. In order to add, remove or list acls you can use the Kafka authorizer CLI. By default, if a Resource R has no associated acls, no one other than super users is allowed to access R. If you want to change that behavior, you can include the following in broker.properties. 
    
    
    allow.everyone.if.no.acl.found=true

One can also add super users in broker.properties like the following (note that the delimiter is semicolon since SSL user names may contain comma). 
    
    
    super.users=User:Bob;User:Alice

By default, the SSL user name will be of the form "CN=writeuser,OU=Unknown,O=Unknown,L=Unknown,ST=Unknown,C=Unknown". One can change that by setting a customized PrincipalBuilder in broker.properties like the following. 
    
    
    principal.builder.class=CustomizedPrincipalBuilderClass

By default, the SASL user name will be the primary part of the Kerberos principal. One can change that by setting `sasl.kerberos.principal.to.local.rules` to a customized rule in broker.properties. The format of `sasl.kerberos.principal.to.local.rules` is a list where each rule works in the same way as the auth_to_local in [Kerberos configuration file (krb5.conf)](http://web.mit.edu/Kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html). Each rules starts with RULE: and contains an expression in the format [n:string](regexp)s/pattern/replacement/g. See the kerberos documentation for more details. An example of adding a rule to properly translate user@MYDOMAIN.COM to user while also keeping the default rule in place is: 
    
    
    sasl.kerberos.principal.to.local.rules=RULE:[1:$1@$0](.*@MYDOMAIN.COM)s/@.*//,DEFAULT

## Command Line Interface

Kafka Authorization management CLI can be found under bin directory with all the other CLIs. The CLI script is called **kafka-acls.sh**. Following lists all the options that the script supports: 

Option | Description | Default | Option type  
---|---|---|---  
--add | Indicates to the script that user is trying to add an acl. |  | Action  
--remove | Indicates to the script that user is trying to remove an acl. |  | Action  
--list | Indicates to the script that user is trying to list acls. |  | Action  
--authorizer | Fully qualified class name of the authorizer. | kafka.security.auth.SimpleAclAuthorizer | Configuration  
--authorizer-properties | key=val pairs that will be passed to authorizer for initialization. For the default authorizer the example values are: zookeeper.connect=localhost:2181 |  | Configuration  
--cluster | Specifies cluster as resource. |  | Resource  
--topic [topic-name] | Specifies the topic as resource. |  | Resource  
--group [group-name] | Specifies the consumer-group as resource. |  | Resource  
--allow-principal | Principal is in PrincipalType:name format that will be added to ACL with Allow permission.   
You can specify multiple --allow-principal in a single command. |  | Principal  
--deny-principal | Principal is in PrincipalType:name format that will be added to ACL with Deny permission.   
You can specify multiple --deny-principal in a single command. |  | Principal  
--allow-host | IP address from which principals listed in --allow-principal will have access. |  if --allow-principal is specified defaults to * which translates to "all hosts" | Host  
--deny-host | IP address from which principals listed in --deny-principal will be denied access. | if --deny-principal is specified defaults to * which translates to "all hosts" | Host  
--operation | Operation that will be allowed or denied.  
Valid values are : Read, Write, Create, Delete, Alter, Describe, ClusterAction, All | All | Operation  
--producer |  Convenience option to add/remove acls for producer role. This will generate acls that allows WRITE, DESCRIBE on topic and CREATE on cluster. |  | Convenience  
--consumer |  Convenience option to add/remove acls for consumer role. This will generate acls that allows READ, DESCRIBE on topic and READ on consumer-group. |  | Convenience  
--force |  Convenience option to assume yes to all queries and do not prompt. |  | Convenience  
  
## Examples

  * **Adding Acls**  
Suppose you want to add an acl "Principals User:Bob and User:Alice are allowed to perform Operation Read and Write on Topic Test-Topic from IP 198.51.100.0 and IP 198.51.100.1". You can do that by executing the CLI with following options: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Bob --allow-principal User:Alice --allow-host 198.51.100.0 --allow-host 198.51.100.1 --operation Read --operation Write --topic Test-topic

By default, all principals that don't have an explicit acl that allows access for an operation to a resource are denied. In rare cases where an allow acl is defined that allows access to all but some principal we will have to use the --deny-principal and --deny-host option. For example, if we want to allow all users to Read from Test-topic but only deny User:BadBob from IP 198.51.100.3 we can do so using following commands: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:* --allow-host * --deny-principal User:BadBob --deny-host 198.51.100.3 --operation Read --topic Test-topic

Note that ``--allow-host`` and ``deny-host`` only support IP addresses (hostnames are not supported). Above examples add acls to a topic by specifying --topic [topic-name] as the resource option. Similarly user can add acls to cluster by specifying --cluster and to a consumer group by specifying --group [group-name].
  * **Removing Acls**  
Removing acls is pretty much the same. The only difference is instead of --add option users will have to specify --remove option. To remove the acls added by the first example above we can execute the CLI with following options: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --remove --allow-principal User:Bob --allow-principal User:Alice --allow-host 198.51.100.0 --allow-host 198.51.100.1 --operation Read --operation Write --topic Test-topic 

  * **List Acls**  
We can list acls for any resource by specifying the --list option with the resource. To list all acls for Test-topic we can execute the CLI with following options: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --list --topic Test-topic

  * **Adding or removing a principal as producer or consumer**  
The most common use case for acl management are adding/removing a principal as producer or consumer so we added convenience options to handle these cases. In order to add User:Bob as a producer of Test-topic we can execute the following command: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Bob --producer --topic Test-topic

Similarly to add Alice as a consumer of Test-topic with consumer group Group-1 we just have to pass --consumer option: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Bob --consumer --topic Test-topic --group Group-1 

Note that for consumer option we must also specify the consumer group. In order to remove a principal from producer or consumer role we just need to pass --remove option. 


