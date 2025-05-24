---
title: "Project Security"
type: docs
---

# Kafka security

The Apache Software Foundation takes security issues very seriously. Apache Kafka® specifically offers security features and is responsive to issues around its features. If you have any concern around Kafka Security or believe you have uncovered a vulnerability, we suggest that you get in touch via the e-mail address [security@kafka.apache.org](mailto:security@kafka.apache.org?Subject=\[SECURITY\] My security issue). In the message, try to provide a description of the issue and ideally a way of reproducing it. The security team will get back to you after assessing the description. 

Note that this security address should be used only for undisclosed vulnerabilities. Dealing with fixed issues or general questions on how to use the security features should be handled regularly via the user and the dev lists. **Please report any security problems to the project security address before disclosing it publicly.**

The ASF Security team maintains a page with a description of how vulnerabilities are handled, check their [Web page](http://www.apache.org/security/) for more information. 

For a list of security issues fixed in released versions of Apache Kafka, see [CVE list](/cve-list). 

## Advisories for dependencies

Many organizations use 'security scanning' tools to detect components for which advisories exist. While we generally encourage using such tools, since they are an important way users are notified of risks, our experience is that they produce a lot of false positives: when a dependency of Kafka contains a vulnerability, it is likely Kafka is using it in a way that is not affected. As such, we do not consider the fact that an advisory has been published for a Kafka dependency sensitive. Only when additional analysis suggests Kafka may be affected by the problem, we ask you to report this finding privately through [security@kafka.apache.org](mailto:security@kafka.apache.org?Subject=\[SECURITY\] My security issue). 

When handling such warnings, you can: 

  * Check if our [DependencyCheck suppressions](https://github.com/apache/kafka/blob/trunk/gradle/resources/dependencycheck-suppressions.xml) contain any information on this advisory. 
  * See if there is any discussion on this advisory in the [issue tracker](https://issues.apache.org/jira/browse/KAFKA)
  * Do your own analysis on whether this advisory affects Kafka. 
    * If it seems it might, report this finding privately through [security@kafka.apache.org](mailto:security@kafka.apache.org?Subject=\[SECURITY\] My security issue). 
    * If it seems not to, [contribute](/contributing.html) a section to our [DependencyCheck suppressions](https://github.com/apache/kafka/blob/trunk/gradle/resources/dependencycheck-suppressions.xml) explaining why it is not affected.  

