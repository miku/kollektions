#!/usr/bin/env bash
# teardown ES CouchDB river
# http://www.elasticsearch.org/guide/reference/river/
curl -XDELETE 'localhost:9200/_river/kollektions/'