---
title: Important configuration properties for Kafka broker
description: Important configuration properties for Kafka broker
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Important configuration properties for Kafka broker: 

More details about server configuration can be found in the scala class `kafka.server.KafkaConfig`.

name | default | description  
---|---|---  
`brokerid` | none | Each broker is uniquely identified by an id. This id serves as the brokers "name", and allows the broker to be moved to a different host/port without confusing consumers.  
`enable.zookeeper` | true | enable zookeeper registration in the server  
`log.flush.interval` | 500 | Controls the number of messages accumulated in each topic (partition) before the data is flushed to disk and made available to consumers.  
`log.default.flush.scheduler.interval.ms` | 3000 | Controls the interval at which logs are checked to see if they need to be flushed to disk. A background thread will run at a frequency specified by this parameter and will check each log to see if it has exceeded its flush.interval time, and if so it will flush it.  
`log.default.flush.interval.ms` | log.default.flush.scheduler.interval.ms | Controls the maximum time that a message in any topic is kept in memory before flushed to disk. The value only makes sense if it's a multiple of `log.default.flush.scheduler.interval .ms`  
`topic.flush.intervals.ms` | none | Per-topic overrides for `log.default.flush.interval.ms`. Controls the maximum time that a message in selected topics is kept in memory before flushed to disk. The per-topic value only makes sense if it's a multiple of `log.default.flush.scheduler.interval.ms`. E.g., topic1:1000,topic2:2000  
`log.retention.hours` | 168 | Controls how long a log file is retained.  
`topic.log.retention.hours` | none | Topic-specific retention time that overrides `log.retention.hours`, e.g., topic1:10,topic2:20  
`log.retention.size` | -1 | the maximum size of the log before deleting it. This controls how large a log is allowed to grow  
`log.cleanup.interval.mins` | 10 | Controls how often the log cleaner checks logs eligible for deletion. A log file is eligible for deletion if it hasn't been modified for `log.retention.hours` hours.  
`log.dir` | none | Specifies the root directory in which all log data is kept.  
`log.file.size` | 1*1024*1024*1024 | Controls the maximum size of a single log file.  
`log.roll.hours` | 24 * 7 | The maximum time before a new log segment is rolled out  
`max.socket.request.bytes` | 104857600 | the maximum number of bytes in a socket request  
`monitoring.period.secs` | 600 | the interval in which to measure performance statistics  
`num.threads` | Runtime.getRuntime().availableProcessors | Controls the number of worker threads in the broker to serve requests.  
`num.partitions` | 1 | Specifies the default number of partitions per topic.  
`socket.send.buffer` | 102400 | the SO_SNDBUFF buffer of the socket sever sockets  
`socket.receive.buffer` | 102400 | the SO_RCVBUFF buffer of the socket sever sockets  
`topic.partition.count.map` | none | Override parameter to control the number of partitions for selected topics. E.g., topic1:10,topic2:20  
`zk.connect` | localhost:2182/kafka | Specifies the zookeeper connection string in the form hostname:port/chroot. Here the chroot is a base directory which is prepended to all path operations (this effectively namespaces all kafka znodes to allow sharing with other applications on the same zookeeper cluster)  
`zk.connectiontimeout.ms` | 6000 | Specifies the max time that the client waits to establish a connection to zookeeper.  
`zk.sessiontimeout.ms` | 6000 | The zookeeper session timeout.  
`zk.synctime.ms` | 2000 | Max time for how far a ZK follower can be behind a ZK leader  
  