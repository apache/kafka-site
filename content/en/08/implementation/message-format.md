---
title: Message Format
description: Message Format
weight: 4
tags: ['kafka', 'docs']
aliases: 
keywords: 
type: docs
---

# Message Format
    
    
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
    
