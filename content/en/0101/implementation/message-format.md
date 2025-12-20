---
title: Message Format
description: Message Format
weight: 4
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


            /**
            * 1. 4 byte CRC32 of the message
            * 2. 1 byte "magic" identifier to allow format changes, value is 0 or 1
            * 3. 1 byte "attributes" identifier to allow annotations on the message independent of the version
            *    bit 0 ~ 2 : Compression codec.
            *      0 : no compression
            *      1 : gzip
            *      2 : snappy
            *      3 : lz4
            *    bit 3 : Timestamp type
            *      0 : create time
            *      1 : log append time
            *    bit 4 ~ 7 : reserved
            * 4. (Optional) 8 byte timestamp only if "magic" identifier is greater than 0
            * 5. 4 byte key length, containing length K
            * 6. K byte key
            * 7. 4 byte payload length, containing length V
            * 8. V byte payload
            */
        
