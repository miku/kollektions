#!/usr/bin/env python
# coding: utf-8

import hashlib

def calculate_sha1(s):
    sha1 = hashlib.sha1()
    sha1.update(s)
    return sha1.hexdigest()