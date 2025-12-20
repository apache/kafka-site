---
title: Broker Configs
description: Broker Configs
weight: 1
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->


The essential configurations are the following: 

  * `broker.id`
  * `log.dirs`
  * `zookeeper.connect` 
Topic-level configurations and defaults are discussed in more detail below. {{< include-html file="/static/10/generated/kafka_config.html" >}} 

More details about broker configuration can be found in the scala class `kafka.server.KafkaConfig`.
