---
title: Developer Guide
type: docs
---

## Getting the code

Our code is kept in Apache GitHub repo. You can check it out like this: 
    
    
    git clone https://github.com/apache/kafka.git kafka

Information on contributing patches can be found [here](contributing.html). 

Official releases are available [here](downloads.html). 

The source code for the web site and documentation can be checked out from Apache GitHub repo: 
    
    
    git clone -b asf-site https://github.com/apache/kafka-site.git

We are happy to received patches for the website and documentation. We think documentation is a core part of the project and welcome any improvements, suggestions, or clarifications. The procedure of contributing to the documentation can also be found [here](contributing.html). 

To setup IDEs for development, following [this guide](https://cwiki.apache.org/confluence/display/KAFKA/Developer+Setup) on the wiki. 

## How to contribute

We are always very happy to have contributions, whether for trivial cleanups or big new features.

If you don't know Java or Scala you can still contribute to the project. An important area is the [clients](https://cwiki.apache.org/confluence/display/KAFKA/Clients). We want to have high quality, well documented clients for each programming language. These, as well as the surrounding [ecosystem](https://cwiki.apache.org/confluence/display/KAFKA/Ecosystem) of integration tools that people use with Kafka®, are critical aspects of the project. 

Nor is code the only way to contribute to the project. We strongly value documentation and gladly accept improvements to the documentation. 

### Reporting An Issue

Reporting potential issues as [JIRA tickets](https://issues.apache.org/jira/browse/KAFKA) is more than welcome as a significant contribution to the project. But please be aware that JIRA tickets should not be used for FAQs: if you have a question or are simply not sure if it is really an issue or not, please [contact us](/contact.html) first before you create a new JIRA ticket. To create a new JIRA ticket, please follow the instructions in [this page](https://cwiki.apache.org/confluence/display/KAFKA/Reporting+Issues+in+Apache+Kafka). 

### Contributing A Code Change

To submit a change for inclusion, please do the following: 

  * If the change is non-trivial please include some unit tests that cover the new functionality.
  * If you are introducing a completely new feature or API it is a good idea to start a wiki and get consensus on the basic design first.
  * Make sure you have observed the recommendations in the [style guide](coding-guide.html).
  * Follow the detailed instructions in [Contributing Code Changes](https://cwiki.apache.org/confluence/display/KAFKA/Contributing+Code+Changes).
  * Note that if the change is related to user-facing protocols / interface / configs, etc, you need to make the corresponding change on the documentation as well. For wiki page changes feel free to edit the page content directly (you may need to contact us to get the permission first if it is your first time to edit on wiki); website docs live in the code repo under `docs` so that changes to that can be done in the same PR as changes to the code. Website doc change instructions are given below. 
  * It is our job to follow up on patches in a timely fashion. [Nag us](mailto:dev@kafka.apache.org) if we aren't doing our job (sometimes we drop things).



### Contributing A Change To The Website

To submit a change for inclusion please do the following: 

  * Follow the instructions in [Contributing Website Changes](https://cwiki.apache.org/confluence/display/KAFKA/Contributing+Website+Documentation+Changes).
  * It is our job to follow up on patches in a timely fashion. [Nag us](mailto:dev@kafka.apache.org) if we aren't doing our job (sometimes we drop things). If the patch needs improvement, the reviewer will mark the jira back to "In Progress" after reviewing.



### Finding A Project To Work On

The easiest way to get started working with the code base is to pick up a really easy JIRA and work on that. This will help you get familiar with the code base, build system, review process, etc. We flag these kind of starter bugs [here](https://issues.apache.org/jira/issues/?jql=project%20%3D%20KAFKA%20AND%20labels%20%3D%20newbie%20AND%20status%20%3D%20Open). 

Please request a JIRA account using [ASF's Self-serve portal](https://selfserve.apache.org/jira-account.html). After that you can assign yourself to the JIRA ticket you have started working on so others will notice. 

If your work is considered a "major change" then you would need to initiate a Kafka Improvement Proposal (KIP) along with the JIRA ticket (more details can be found [here](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals)). Please ask us to grant you the permission on wiki space in order to create a KIP wiki page. 

Once you have gotten through the basic process of checking in code, you may want to move on to a more substantial project. We try to curate this kind of project as well, and you can find these [here](https://issues.apache.org/jira/issues/?jql=project%20%3D%20KAFKA%20AND%20labels%20%3D%20project%20AND%20status%20%3D%20Open). 

### Becoming a Committer

We are always interested in adding new contributors. What we look for is a series of contributions, good taste, and an ongoing interest in the project. Kafka PMC looks at the following guidelines for promoting new committers: 

  * Made significant contributions in areas such as design, code and/or documentation. The following are some examples (list not exclusive): 
    * Submitted and completed non-trivial KIPs.
    * Fixed critical bugs (including performance improvements).
    * Made major tech-debt cleanup.
    * Made major documentation (web docs and java docs) improvements.
  * Consistently helped the community in at least one of the following areas since more than 6 months back (list not exclusive): 
    * Mailing list participation.
    * Code reviews and KIP reviews.
    * Release validations including testing and benchmarking, etc.
    * Evangelism events: technical talks, blog posts, etc.
  * Demonstrated good understanding and exercised good technical judgement on at least one component of the codebase (e.g. core, clients, connect, streams, tests) from contribution activities in the above mentioned areas.



### Collaborators

The Apache build infrastructure has provided two roles to make project management easier. These roles allow non-committers to perform some administrative actions like triaging pull requests or triggering builds. See the ASF documentation (note: you need to be logged in to the wiki): 

  * [Jenkins PR Whitelisted Users](https://cwiki.apache.org/confluence/pages/viewpage.action?spaceKey=INFRA&title=Git+-+.asf.yaml+features#Git.asf.yamlfeatures-JenkinsPRwhitelisting)
  * [Github Collaborators](https://cwiki.apache.org/confluence/pages/viewpage.action?spaceKey=INFRA&title=Git+-+.asf.yaml+features#Git.asf.yamlfeatures-AssigningexternalcollaboratorswiththetriageroleonGitHub)



In an effort to keep the Apache Kafka project running smoothly, and also to help contributors become committers, we have enabled these roles (See [the Apache Kafka Infra config](https://github.com/apache/kafka/blob/trunk/.asf.yaml)). To keep this process lightweight and fair, we keep the list of contributors full by specifying the top N non-committers (sorted by number of commits they have authored in the last 12 months), where N is the maximum size of that list (currently 10). Authorship is determined by `git shortlog`. The list will be updated as part of the major/minor release process, three to four times a year. 

## Coding guidelines

These guidelines are meant to encourage consistency and best practices amongst people working on the Kafka® code base. They should be observed unless there is a compelling reason to ignore them. 

### Basic Stuff

  * Avoid cryptic abbreviations. Single letter variable names are fine in very short methods with few variables, otherwise make them informative.
  * Clear code is preferable to comments. When possible make your naming so good you don't need comments. When that isn't possible comments should be thought of as mandatory, write them to be _read_.
  * Logging, configuration, and public APIs are our "UI". Pay special attention to them and make them pretty, consistent, and usable.
  * There is not a maximum line length (certainly not 80 characters, we don't work on punch cards any more), but be reasonable.
  * Don't be sloppy. Don't check in commented out code: we use version control, it is still there in the history. Don't leave TODOs in the code or FIXMEs if you can help it. Don't leave println statements in the code. Hopefully this is all obvious.
  * We want people to use our stuff, which means we need clear, correct documentation. User documentation should be considered a part of any user-facing the feature, just like unit tests or performance results.
  * Don't duplicate code (duh).
  * Kafka is system software, and certain things are appropriate in system software that are not appropriate elsewhere. Sockets, bytes, concurrency, and distribution are our core competency which means we will have a more "from scratch" implementation of some of these things then would be appropriate for software elsewhere in the stack. This is because we need to be exceptionally good at these things. This does not excuse fiddly low-level code, but it does excuse spending a little extra time to make sure that our filesystem structures, networking code, threading model, are all done perfectly right for our application rather than just trying to glue together ill-fitting off-the-shelf pieces (well-fitting off-the-shelf pieces are great though).



### Scala

We are following the style guide given [here](http://docs.scala-lang.org/style/) (though not perfectly). Below are some specifics worth noting: 

  * Scala is a very flexible language. Use restraint. Magic cryptic one-liners do not impress us, readability impresses us.
  * Use `val`s when possible.
  * Use private when possible for member variables.
  * Method and member variable names should be in camel case with an initial lower case character like `aMethodName`.
  * Constants should be camel case with an initial capital `LikeThis` not `LIKE_THIS`.
  * Prefer a single top-level class per file for ease of finding things.
  * Do not use semi-colons unless required.
  * Avoid getters and setters - stick to plain `val`s or `var`s instead. If (later on) you require a custom setter (or getter) for a `var` named `myVar` then add a shadow `var myVar_underlying` and override the setter (`def myVar_=`) and the getter (`def myVar = myVar_underlying`).
  * Prefer `Option` to `null` in scala APIs.
  * Use named arguments when passing in literal values if the meaning is at all unclear, for example instead of `Utils.delete(true)` prefer `Utils.delete(recursive=true)`. 
  * Indentation is 2 spaces and never tabs. One could argue the right amount of indentation, but 2 seems to be standard for scala and consistency is best here since there is clearly no "right" way.
  * Include the optional parenthesis on a no-arg method only if the method has a side-effect, otherwise omit them. For example `fileChannel.force()` and `fileChannel.size`. This helps emphasize that you are calling the method for the side effect, which is changing some state, not just getting the return value.
  * Prefer case classes to tuples in important APIs to make it clear what the intended contents are.



### Logging

  * Logging is one third of our "UI" and it should be taken seriously. Please take the time to assess the logs when making a change to ensure that the important things are getting logged and there is no junk there.
  * Logging statements should be complete sentences with proper capitalization that are written to be read by a person not necessarily familiar with the source code. It is fine to put in hacky little logging statements when debugging, but either clean them up or remove them before checking in. So logging something like "INFO: entering SyncProducer send()" is not appropriate.
  * Logging should not mention class names or internal variables.
  * There are six levels of logging `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, and `FATAL`, they should be used as follows. 
    * `INFO` is the level you should assume the software will be run in. INFO messages are things which are not bad but which the user will definitely want to know about every time they occur. 
    * `TRACE` and `DEBUG` are both things you turn on when something is wrong and you want to figure out what is going on. `DEBUG` should not be so fine grained that it will seriously effect the performance of the server. `TRACE` can be anything. Both `DEBUG` and `TRACE` statements should be wrapped in an `if(logger.isDebugEnabled)` check to avoid pasting together big strings all the time. 
    * `WARN` and `ERROR` indicate something that is bad. Use `WARN` if you aren't totally sure it is bad, and `ERROR` if you are. 
    * Use `FATAL` only right before calling `System.exit()`. 



### Monitoring

  * Monitoring is the second third of our "UI" and it should also be taken seriously.
  * We use JMX for monitoring.
  * Any new features should come with appropriate monitoring to know the feature is working correctly. This is at least as important as unit tests as it verifies production.



### Unit Tests

  * New patches should come with unit tests that verify the functionality being added.
  * Unit tests are first rate code, and should be treated like it. They should not contain code duplication, cryptic hackery, or anything like that.
  * Be aware of the methods in `kafka.utils.TestUtils`, they make a lot of the below things easier to get right.
  * Unit tests should test the least amount of code possible, don't start the whole server unless there is no other way to test a single class or small group of classes in isolation.
  * Tests should not depend on any external resources, they need to set up and tear down their own stuff. This means if you want zookeeper it needs to be started and stopped, you can't depend on it already being there. Likewise if you need a file with some data in it, you need to write it in the beginning of the test and delete it (pass or fail).
  * It is okay to use the filesystem and network in tests since that is our business but you need to clean up after yourself. There are helpers for this in `TestUtils`.
  * Do not use sleep or other timing assumptions in tests, it is always, always, always wrong and will fail intermittently on any test server with other things going on that causes delays. Write tests in such a way that they are not timing dependent. Seriously. One thing that will help this is to never directly use the system clock in code (i.e. `System.currentTimeMillis`) but instead to use the `kafka.utils.Time`. This is a trait that has a mock implementation allowing you to programmatically and deterministically cause the passage of time when you inject this mock clock instead of the system clock.
  * It must be possible to run the tests in parallel, without having them collide. This is a practical thing to allow multiple branches to CI on a single CI server. This means you can't hard code directories or ports or things like that in tests because two instances will step on each other. Again `TestUtils` has helpers for this stuff (e.g. `TestUtils.choosePort` will find a free port for you).



### Configuration

  * Configuration is the final third of our "UI".
  * Names should be thought through from the point of view of the person using the config, but often programmers choose configuration names that make sense for someone reading the code.
  * Often the value that makes most sense in configuration is _not_ the one most useful to program with. For example, let's say you want to throttle I/O to avoid using up all the I/O bandwidth. The easiest thing to implement is to give a "sleep time" configuration that let's the program sleep after doing I/O to throttle down its rate. But notice how hard it is to correctly use this configuration parameter, the user has to figure out the rate of I/O on the machine, and then do a bunch of arithmetic to calculate the right sleep time to give the desired rate of I/O on the system. It is much, much, much better to just have the user configure the maximum I/O rate they want to allow (say 5MB/sec) and then calculate the appropriate sleep time from that and the actual I/O rate. Another way to say this is that configuration should always be in terms of the quantity that the user knows, not the quantity you want to use.
  * Configuration is the answer to problems we can't solve up front for some reason--if there is a way to just choose a best value do that instead.
  * Configuration should come from the instance-level properties file. No additional sources of config (environment variables, system properties, etc) should be added as these usually inhibit running multiple instances of a broker on one machine.



### Concurrency

  * Encapsulate synchronization. That is, locks should be private member variables within a class and only one class or method should need to be examined to verify the correctness of the synchronization strategy.
  * Annotate things as `@threadsafe` when they are supposed to be and `@notthreadsafe` when they aren't to help track this stuff.
  * There are a number of gotchas with threads and threadpools: is the daemon flag set appropriately for your threads? are your threads being named in a way that will distinguish their purpose in a thread dump? What happens when the number of queued tasks hits the limit (do you drop stuff? do you block?).
  * Prefer the java.util.concurrent packages to either low-level wait-notify, custom locking/synchronization, or higher level scala-specific primitives. The util.concurrent stuff is well thought out and actually works correctly. There is a generally feeling that threads and locking are not going to be the concurrency primitives of the future because of a variety of well-known weaknesses they have. This is probably true, but they have the advantage of actually being mature enough to use for high-performance software _right now_ ; their well-known deficiencies are easily worked around by equally well known best-practices. So avoid actors, software transactional memory, tuple spaces, or anything else not written by Doug Lea and used by at least a million other productions systems. :-)



### Backwards Compatibility

  * Our policy is that the Kafka protocols and data formats should support backwards compatibility for as many releases to enable no-downtime upgrades (unless there is a _very_ compelling counter-argument). This means the server MUST be able to support requests from both old and new clients simultaneously. This compatibility needs to be retained for at least one major release (e.g. 2.0 must accept requests from 1.0 clients). A typical upgrade sequence for binary format changes would be (1) upgrade server to handle the new message format, (2) upgrade clients to use the new message format.
  * There are three things which require this binary compatibility: request objects, persistent data structure (messages and message sets), and zookeeper structures and protocols. The message binary structure has a "magic" byte to allow it to be evolved, this number should be incremented when the format is changed and the number can be checked to apply the right logic and fill in defaults appropriately. Network requests have a request id which serve a similar purpose, any change to a request object must be accompanied by a change in the request id. Any change here should be accompanied by compatibility tests that save requests or messages in the old format as a binary file which is tested for compatibility with the new code.



### Client Code

There are a few things that need to be considered in client code that are not a major concern on the server side.

  * Libraries needed by the client should be avoided whenever possible. Clients are run in someone else's code and it is very possible that they may have the same library we have, but a different and incompatible version. This will mean they can't use our client. For this reason the client should not use any libraries that are not strictly necessary.
  * We should maintain API compatibility. Any incompatible changes should be ultimately settled in the KIP design process, where the usual strategy is to retain the old APIs, mark them as deprecated and potentially remove them in some next major release.



### Streams API

Kafka's Streams API (aka Kafka Streams) uses a few more additional coding guidelines. All contributors should follow these the get a high quality and uniform code base. Some rules help to simplify PR reviews and thus make the life of all contributors easier.

  * Use `final` when possible. This holds for all class members, local variables, loop variables, and method parameters.
  * Write modular and thus testable code. Refactor if necessary!
  * Avoid large PRs (recommended is not more the 500 lines per PR). Many JIRAs requires larger code changes; thus, split the work in multiple PRs and create according sub-task on the JIRA to track the work.
  * All public APIs must have JavaDocs.
  * Verify if JavaDocs are still up to date or if they need to be updated.
  * JavaDocs: Write grammatically correct sentences and use punctuation marks correctly.
  * Use proper markup (e.g., `{@code null}`).
  * Update the documentation on the Kafka webpage (i.e., within folder `docs/`. Doc changes are not additional work (i.e., no follow up PRs) but part of the actual PR (can also be a sub-task).
  * Testing: 
    * Use self-explaining method names (e.g., `shouldNotAcceptNullAsTopicName()`).
    * Each test should cover only a single case.
    * Keep tests as short as possible (i.e., write crisp code).
    * Write tests for all possible parameter values.
    * Don't use reflections but rewrite your code (reflections indicate bad design in the first place).
    * Use annotations such as `@Test(expected = SomeException.class)` only for single line tests.
  * Code formatting (those make Github diffs easier to read and thus simplify code reviews): 
    * No line should be longer than 120 characters.
    * Use a "single parameter per line" formatting when defining methods (also for methods with only 2 parameters).
    * If a method call is longer than 120 characters, switch to a single parameter per line formatting (instead of just breaking it into two lines only).
    * For JavaDocs, start a new line for each new sentence.
    * Avoid unnecessary reformatting.
    * If reformatting is neccessary, do a minor PR (either upfront or as follow up).
  * Run `./gradlew clean checkstyleMain checkstyleTest` before opening/updating a PR.
  * Help reviewing! No need to be shy; if you can contribute code, you know enough to comment on the work of others.
