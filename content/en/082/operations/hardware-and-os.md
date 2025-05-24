---
title: Hardware and OS
description: Hardware and OS
weight: 5
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Hardware and OS

We are using dual quad-core Intel Xeon machines with 24GB of memory. 

You need sufficient memory to buffer active readers and writers. You can do a back-of-the-envelope estimate of memory needs by assuming you want to be able to buffer for 30 seconds and compute your memory need as write_throughput*30. 

The disk throughput is important. We have 8x7200 rpm SATA drives. In general disk throughput is the performance bottleneck, and more disks is more better. Depending on how you configure flush behavior you may or may not benefit from more expensive disks (if you force flush often then higher RPM SAS drives may be better). 

## OS

Kafka should run well on any unix system and has been tested on Linux and Solaris. 

We have seen a few issues running on Windows and Windows is not currently a well supported platform though we would be happy to change that. 

You likely don't need to do much OS-level tuning though there are a few things that will help performance. 

Two configurations that may be important: 

  * We upped the number of file descriptors since we have lots of topics and lots of connections. 
  * We upped the max socket buffer size to enable high-performance data transfer between data centers [described here](http://www.psc.edu/index.php/networking/641-tcp-tune). 


## Disks and Filesystem

We recommend using multiple drives to get good throughput and not sharing the same drives used for Kafka data with application logs or other OS filesystem activity to ensure good latency. As of 0.8 you can either RAID these drives together into a single volume or format and mount each drive as its own directory. Since Kafka has replication the redundancy provided by RAID can also be provided at the application level. This choice has several tradeoffs. 

If you configure multiple data directories partitions will be assigned round-robin to data directories. Each partition will be entirely in one of the data directories. If data is not well balanced among partitions this can lead to load imbalance between disks. 

RAID can potentially do better at balancing load between disks (although it doesn't always seem to) because it balances load at a lower level. The primary downside of RAID is that it is usually a big performance hit for write throughput and reduces the available disk space. 

Another potential benefit of RAID is the ability to tolerate disk failures. However our experience has been that rebuilding the RAID array is so I/O intensive that it effectively disables the server, so this does not provide much real availability improvement. 

## Application vs. OS Flush Management

Kafka always immediately writes all data to the filesystem and supports the ability to configure the flush policy that controls when data is forced out of the OS cache and onto disk using the and flush. This flush policy can be controlled to force data to disk after a period of time or after a certain number of messages has been written. There are several choices in this configuration. 

Kafka must eventually call fsync to know that data was flushed. When recovering from a crash for any log segment not known to be fsync'd Kafka will check the integrity of each message by checking its CRC and also rebuild the accompanying offset index file as part of the recovery process executed on startup. 

Note that durability in Kafka does not require syncing data to disk, as a failed node will always recover from its replicas. 

We recommend using the default flush settings which disable application fsync entirely. This means relying on the background flush done by the OS and Kafka's own background flush. This provides the best of all worlds for most uses: no knobs to tune, great throughput and latency, and full recovery guarantees. We generally feel that the guarantees provided by replication are stronger than sync to local disk, however the paranoid still may prefer having both and application level fsync policies are still supported. 

The drawback of using application level flush settings are that this is less efficient in it's disk usage pattern (it gives the OS less leeway to re-order writes) and it can introduce latency as fsync in most Linux filesystems blocks writes to the file whereas the background flushing does much more granular page-level locking. 

In general you don't need to do any low-level tuning of the filesystem, but in the next few sections we will go over some of this in case it is useful. 

## Understanding Linux OS Flush Behavior

In Linux, data written to the filesystem is maintained in [pagecache](http://en.wikipedia.org/wiki/Page_cache) until it must be written out to disk (due to an application-level fsync or the OS's own flush policy). The flushing of data is done by a set of background threads called pdflush (or in post 2.6.32 kernels "flusher threads"). 

Pdflush has a configurable policy that controls how much dirty data can be maintained in cache and for how long before it must be written back to disk. This policy is described [here](http://www.westnet.com/~gsmith/content/linux-pdflush.htm). When Pdflush cannot keep up with the rate of data being written it will eventually cause the writing process to block incurring latency in the writes to slow down the accumulation of data. 

You can see the current state of OS memory usage by doing 
    
    
      > cat /proc/meminfo
    

The meaning of these values are described in the link above. 

Using pagecache has several advantages over an in-process cache for storing data that will be written out to disk: 

  * The I/O scheduler will batch together consecutive small writes into bigger physical writes which improves throughput. 
  * The I/O scheduler will attempt to re-sequence writes to minimize movement of the disk head which improves throughput. 
  * It automatically uses all the free memory on the machine 


## Ext4 Notes

Ext4 may or may not be the best filesystem for Kafka. Filesystems like XFS supposedly handle locking during fsync better. We have only tried Ext4, though. 

It is not necessary to tune these settings, however those wanting to optimize performance have a few knobs that will help: 

  * data=writeback: Ext4 defaults to data=ordered which puts a strong order on some writes. Kafka does not require this ordering as it does very paranoid data recovery on all unflushed log. This setting removes the ordering constraint and seems to significantly reduce latency. 
  * Disabling journaling: Journaling is a tradeoff: it makes reboots faster after server crashes but it introduces a great deal of additional locking which adds variance to write performance. Those who don't care about reboot time and want to reduce a major source of write latency spikes can turn off journaling entirely. 
  * commit=num_secs: This tunes the frequency with which ext4 commits to its metadata journal. Setting this to a lower value reduces the loss of unflushed data during a crash. Setting this to a higher value will improve throughput. 
  * nobh: This setting controls additional ordering guarantees when using data=writeback mode. This should be safe with Kafka as we do not depend on write ordering and improves throughput and latency. 
  * delalloc: Delayed allocation means that the filesystem avoid allocating any blocks until the physical write occurs. This allows ext4 to allocate a large extent instead of smaller pages and helps ensure the data is written sequentially. This feature is great for throughput. It does seem to involve some locking in the filesystem which adds a bit of latency variance. 

