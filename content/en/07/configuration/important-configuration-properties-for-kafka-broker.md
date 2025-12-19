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
  
<table>  
<tr>  
<th>

name
</th>  
<th>

default
</th>  
<th>

description
</th> </tr>  
<tr>  
<td>

`brokerid`
</td>  
<td>

none
</td>  
<td>

Each broker is uniquely identified by an id. This id serves as the brokers "name", and allows the broker to be moved to a different host/port without confusing consumers.
</td> </tr>  
<tr>  
<td>

`enable.zookeeper`
</td>  
<td>

true
</td>  
<td>

enable zookeeper registration in the server
</td> </tr>  
<tr>  
<td>

`log.flush.interval`
</td>  
<td>

500
</td>  
<td>

Controls the number of messages accumulated in each topic (partition) before the data is flushed to disk and made available to consumers.
</td> </tr>  
<tr>  
<td>

`log.default.flush.scheduler.interval.ms`
</td>  
<td>

3000
</td>  
<td>

Controls the interval at which logs are checked to see if they need to be flushed to disk. A background thread will run at a frequency specified by this parameter and will check each log to see if it has exceeded its flush.interval time, and if so it will flush it.
</td> </tr>  
<tr>  
<td>

`log.default.flush.interval.ms` 
</td>  
<td>

log.default.flush.scheduler.interval.ms
</td>  
<td>

Controls the maximum time that a message in any topic is kept in memory before flushed to disk. The value only makes sense if it's a multiple of `log.default.flush.scheduler.interval .ms`
</td> </tr>  
<tr>  
<td>

`topic.flush.intervals.ms`
</td>  
<td>

none
</td>  
<td>

Per-topic overrides for `log.default.flush.interval.ms`. Controls the maximum time that a message in selected topics is kept in memory before flushed to disk. The per-topic value only makes sense if it's a multiple of `log.default.flush.scheduler.interval.ms`. E.g., topic1:1000,topic2:2000
</td> </tr>  
<tr>  
<td>

`log.retention.hours`
</td>  
<td>

168
</td>  
<td>

Controls how long a log file is retained.
</td> </tr>  
<tr>  
<td>

`topic.log.retention.hours`
</td>  
<td>

none
</td>  
<td>

Topic-specific retention time that overrides `log.retention.hours`, e.g., topic1:10,topic2:20
</td> </tr>  
<tr>  
<td>

`log.retention.size`
</td>  
<td>

-1
</td>  
<td>

the maximum size of the log before deleting it. This controls how large a log is allowed to grow
</td> </tr>  
<tr>  
<td>

`log.cleanup.interval.mins`
</td>  
<td>

10
</td>  
<td>

Controls how often the log cleaner checks logs eligible for deletion. A log file is eligible for deletion if it hasn't been modified for `log.retention.hours` hours.
</td> </tr>  
<tr>  
<td>

`log.dir`
</td>  
<td>

none
</td>  
<td>

Specifies the root directory in which all log data is kept.
</td> </tr>  
<tr>  
<td>

`log.file.size`
</td>  
<td>

1*1024*1024*1024
</td>  
<td>

Controls the maximum size of a single log file.
</td> </tr>  
<tr>  
<td>

`log.roll.hours`
</td>  
<td>

24 * 7
</td>  
<td>

The maximum time before a new log segment is rolled out
</td> </tr>  
<tr>  
<td>

`max.socket.request.bytes`
</td>  
<td>

104857600
</td>  
<td>

the maximum number of bytes in a socket request
</td> </tr>  
<tr>  
<td>

`monitoring.period.secs`
</td>  
<td>

600
</td>  
<td>

the interval in which to measure performance statistics
</td> </tr>  
<tr>  
<td>

`num.threads`
</td>  
<td>

Runtime.getRuntime().availableProcessors
</td>  
<td>

Controls the number of worker threads in the broker to serve requests.
</td> </tr>  
<tr>  
<td>

`num.partitions`
</td>  
<td>

1
</td>  
<td>

Specifies the default number of partitions per topic.
</td> </tr>  
<tr>  
<td>

`socket.send.buffer`
</td>  
<td>

102400
</td>  
<td>

the SO_SNDBUFF buffer of the socket sever sockets
</td> </tr>  
<tr>  
<td>

`socket.receive.buffer`
</td>  
<td>

102400
</td>  
<td>

the SO_RCVBUFF buffer of the socket sever sockets
</td> </tr>  
<tr>  
<td>

`topic.partition.count.map`
</td>  
<td>

none
</td>  
<td>

Override parameter to control the number of partitions for selected topics. E.g., topic1:10,topic2:20
</td> </tr>  
<tr>  
<td>

`zk.connect`
</td>  
<td>

localhost:2182/kafka
</td>  
<td>

Specifies the zookeeper connection string in the form hostname:port/chroot. Here the chroot is a base directory which is prepended to all path operations (this effectively namespaces all kafka znodes to allow sharing with other applications on the same zookeeper cluster)
</td> </tr>  
<tr>  
<td>

`zk.connectiontimeout.ms` 
</td>  
<td>

6000
</td>  
<td>

Specifies the max time that the client waits to establish a connection to zookeeper.
</td> </tr>  
<tr>  
<td>

`zk.sessiontimeout.ms` 
</td>  
<td>

6000
</td>  
<td>

The zookeeper session timeout.
</td> </tr>  
<tr>  
<td>

`zk.synctime.ms`
</td>  
<td>

2000
</td>  
<td>

Max time for how far a ZK follower can be behind a ZK leader
</td> </tr> </table>
