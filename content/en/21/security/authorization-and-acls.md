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

Kafka ships with a pluggable Authorizer and an out-of-box authorizer implementation that uses zookeeper to store all the acls. The Authorizer is configured by setting `authorizer.class.name` in server.properties. To enable the out of the box implementation use: 
    
    
    authorizer.class.name=kafka.security.auth.SimpleAclAuthorizer

Kafka acls are defined in the general format of "Principal P is [Allowed/Denied] Operation O From Host H on any Resource R matching ResourcePattern RP". You can read more about the acl structure in KIP-11 and resource patterns in KIP-290. In order to add, remove or list acls you can use the Kafka authorizer CLI. By default, if no ResourcePatterns match a specific Resource R, then R has no associated acls, and therefore no one other than super users is allowed to access R. If you want to change that behavior, you can include the following in server.properties. 
    
    
    allow.everyone.if.no.acl.found=true

One can also add super users in server.properties like the following (note that the delimiter is semicolon since SSL user names may contain comma). Default PrincipalType string "User" is case sensitive. 
    
    
    super.users=User:Bob;User:Alice

By default, the SSL user name will be of the form "CN=writeuser,OU=Unknown,O=Unknown,L=Unknown,ST=Unknown,C=Unknown". One can change that by setting a customized PrincipalBuilder in server.properties like the following. 
    
    
    principal.builder.class=CustomizedPrincipalBuilderClass

By default, the SASL user name will be the primary part of the Kerberos principal. One can change that by setting `sasl.kerberos.principal.to.local.rules` to a customized rule in server.properties. The format of `sasl.kerberos.principal.to.local.rules` is a list where each rule works in the same way as the auth_to_local in [Kerberos configuration file (krb5.conf)](http://web.mit.edu/Kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html). This also support additional lowercase rule, to force the translated result to be all lower case. This is done by adding a "/L" to the end of the rule. check below formats for syntax. Each rules starts with RULE: and contains an expression as the following formats. See the kerberos documentation for more details. 
    
    
            RULE:[n:string](regexp)s/pattern/replacement/
            RULE:[n:string](regexp)s/pattern/replacement/g
            RULE:[n:string](regexp)s/pattern/replacement//L
            RULE:[n:string](regexp)s/pattern/replacement/g/L
        

An example of adding a rule to properly translate user@MYDOMAIN.COM to user while also keeping the default rule in place is: 
    
    
    sasl.kerberos.principal.to.local.rules=RULE:[1:$1@$0](.*@MYDOMAIN.COM)s/@.*//,DEFAULT

## Command Line Interface

Kafka Authorization management CLI can be found under bin directory with all the other CLIs. The CLI script is called **kafka-acls.sh**. Following lists all the options that the script supports: 

Option | Description | Default | Option type  
---|---|---|---  
\--add | Indicates to the script that user is trying to add an acl. |  | Action  
\--remove | Indicates to the script that user is trying to remove an acl. |  | Action  
\--list | Indicates to the script that user is trying to list acls. |  | Action  
\--authorizer | Fully qualified class name of the authorizer. | kafka.security.auth.SimpleAclAuthorizer | Configuration  
\--authorizer-properties | key=val pairs that will be passed to authorizer for initialization. For the default authorizer the example values are: zookeeper.connect=localhost:2181 |  | Configuration  
\--bootstrap-server | A list of host/port pairs to use for establishing the connection to the Kafka cluster. Only one of --bootstrap-server or --authorizer option must be specified. |  | Configuration  
\--command-config | A property file containing configs to be passed to Admin Client. This option can only be used with --bootstrap-server option. |  | Configuration  
\--cluster | Indicates to the script that the user is trying to interact with acls on the singular cluster resource. |  | ResourcePattern  
\--topic [topic-name] | Indicates to the script that the user is trying to interact with acls on topic resource pattern(s). |  | ResourcePattern  
\--group [group-name] | Indicates to the script that the user is trying to interact with acls on consumer-group resource pattern(s) |  | ResourcePattern  
\--resource-pattern-type [pattern-type] | Indicates to the script the type of resource pattern, (for --add), or resource pattern filter, (for --list and --remove), the user wishes to use.  
When adding acls, this should be a specific pattern type, e.g. 'literal' or 'prefixed'.  
When listing or removing acls, a specific pattern type filter can be used to list or remove acls from a specific type of resource pattern, or the filter values of 'any' or 'match' can be used, where 'any' will match any pattern type, but will match the resource name exactly, and 'match' will perform pattern matching to list or remove all acls that affect the supplied resource(s).  
WARNING: 'match', when used in combination with the '--remove' switch, should be used with care.  | literal | Configuration  
\--allow-principal | Principal is in PrincipalType:name format that will be added to ACL with Allow permission. Default PrincipalType string "User" is case sensitive.   
You can specify multiple --allow-principal in a single command. |  | Principal  
\--deny-principal | Principal is in PrincipalType:name format that will be added to ACL with Deny permission. Default PrincipalType string "User" is case sensitive.   
You can specify multiple --deny-principal in a single command. |  | Principal  
\--principal | Principal is in PrincipalType:name format that will be used along with --list option. Default PrincipalType string "User" is case sensitive. This will list the ACLs for the specified principal.   
You can specify multiple --principal in a single command. |  | Principal  
\--allow-host | IP address from which principals listed in --allow-principal will have access. |  if --allow-principal is specified defaults to * which translates to "all hosts" | Host  
\--deny-host | IP address from which principals listed in --deny-principal will be denied access. | if --deny-principal is specified defaults to * which translates to "all hosts" | Host  
\--operation | Operation that will be allowed or denied.  
Valid values are : Read, Write, Create, Delete, Alter, Describe, ClusterAction, All | All | Operation  
\--producer |  Convenience option to add/remove acls for producer role. This will generate acls that allows WRITE, DESCRIBE and CREATE on topic. |  | Convenience  
\--consumer |  Convenience option to add/remove acls for consumer role. This will generate acls that allows READ, DESCRIBE on topic and READ on consumer-group. |  | Convenience  
\--force |  Convenience option to assume yes to all queries and do not prompt. |  | Convenience  
  
## Examples

  * **Adding Acls**  
Suppose you want to add an acl "Principals User:Bob and User:Alice are allowed to perform Operation Read and Write on Topic Test-Topic from IP 198.51.100.0 and IP 198.51.100.1". You can do that by executing the CLI with following options: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Bob --allow-principal User:Alice --allow-host 198.51.100.0 --allow-host 198.51.100.1 --operation Read --operation Write --topic Test-topic

By default, all principals that don't have an explicit acl that allows access for an operation to a resource are denied. In rare cases where an allow acl is defined that allows access to all but some principal we will have to use the --deny-principal and --deny-host option. For example, if we want to allow all users to Read from Test-topic but only deny User:BadBob from IP 198.51.100.3 we can do so using following commands: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:* --allow-host * --deny-principal User:BadBob --deny-host 198.51.100.3 --operation Read --topic Test-topic

Note that ``--allow-host`` and ``deny-host`` only support IP addresses (hostnames are not supported). Above examples add acls to a topic by specifying --topic [topic-name] as the resource pattern option. Similarly user can add acls to cluster by specifying --cluster and to a consumer group by specifying --group [group-name]. You can add acls on any resource of a certain type, e.g. suppose you wanted to add an acl "Principal User:Peter is allowed to produce to any Topic from IP 198.51.200.0" You can do that by using the wildcard resource '*', e.g. by executing the CLI with following options: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Peter --allow-host 198.51.200.1 --producer --topic *

You can add acls on prefixed resource patterns, e.g. suppose you want to add an acl "Principal User:Jane is allowed to produce to any Topic whose name starts with 'Test-' from any host". You can do that by executing the CLI with following options: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Jane --producer --topic Test- --resource-pattern-type prefixed

Note, --resource-pattern-type defaults to 'literal', which only affects resources with the exact same name or, in the case of the wildcard resource name '*', a resource with any name.
  * **Removing Acls**  
Removing acls is pretty much the same. The only difference is instead of --add option users will have to specify --remove option. To remove the acls added by the first example above we can execute the CLI with following options: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --remove --allow-principal User:Bob --allow-principal User:Alice --allow-host 198.51.100.0 --allow-host 198.51.100.1 --operation Read --operation Write --topic Test-topic 

If you wan to remove the acl added to the prefixed resource pattern above we can execute the CLI with following options: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --remove --allow-principal User:Jane --producer --topic Test- --resource-pattern-type Prefixed

  * **List Acls**  
We can list acls for any resource by specifying the --list option with the resource. To list all acls on the literal resource pattern Test-topic, we can execute the CLI with following options: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --list --topic Test-topic

However, this will only return the acls that have been added to this exact resource pattern. Other acls can exist that affect access to the topic, e.g. any acls on the topic wildcard '*', or any acls on prefixed resource patterns. Acls on the wildcard resource pattern can be queried explicitly: 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --list --topic *

However, it is not necessarily possible to explicitly query for acls on prefixed resource patterns that match Test-topic as the name of such patterns may not be known. We can list _all_ acls affecting Test-topic by using '--resource-pattern-type match', e.g. 
    
        bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --list --topic Test-topic --resource-pattern-type match

This will list acls on all matching literal, wildcard and prefixed resource patterns.
  * **Adding or removing a principal as producer or consumer**  
The most common use case for acl management are adding/removing a principal as producer or consumer so we added convenience options to handle these cases. In order to add User:Bob as a producer of Test-topic we can execute the following command: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Bob --producer --topic Test-topic

Similarly to add Alice as a consumer of Test-topic with consumer group Group-1 we just have to pass --consumer option: 
    
         bin/kafka-acls.sh --authorizer-properties zookeeper.connect=localhost:2181 --add --allow-principal User:Bob --consumer --topic Test-topic --group Group-1 

Note that for consumer option we must also specify the consumer group. In order to remove a principal from producer or consumer role we just need to pass --remove option. 
  * **AdminClient API based acl management**  
Users having Alter permission on ClusterResource can use AdminClient API for ACL management. kafka-acls.sh script supports AdminClient API to manage ACLs without interacting with zookeeper/authorizer directly. All the above examples can be executed by using **\--bootstrap-server** option. For example: 
    
                    bin/kafka-acls.sh --bootstrap-server localhost:9092 --command-config /tmp/adminclient-configs.conf --add --allow-principal User:Bob --producer --topic Test-topic
                bin/kafka-acls.sh --bootstrap-server localhost:9092 --command-config /tmp/adminclient-configs.conf --add --allow-principal User:Bob --consumer --topic Test-topic --group Group-1
                bin/kafka-acls.sh --bootstrap-server localhost:9092 --command-config /tmp/adminclient-configs.conf --list --topic Test-topic



