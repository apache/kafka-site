---
title: Message Format
description: 
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
    	 * A message. The format of an N byte message is the following: 
    	 * 
    	 * If magic byte is 0 
    	 * 
    	 * 1. 1 byte "magic" identifier to allow format changes 
    	 * 
    	 * 2. 4 byte CRC32 of the payload 
    	 * 
    	 * 3. N - 5 byte payload 
    	 * 
    	 * If magic byte is 1 
    	 * 
    	 * 1. 1 byte "magic" identifier to allow format changes 
    	 * 
    	 * 2. 1 byte "attributes" identifier to allow annotations on the message independent of the version (e.g. compression enabled, type of codec used) 
    	 * 
    	 * 3. 4 byte CRC32 of the payload 
    	 * 
    	 * 4. N - 6 byte payload 
    	 * 
    	 */
    
