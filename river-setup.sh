#!/usr/bin/env bash
# setup ES CouchDB river
# http://www.elasticsearch.org/guide/reference/river/

curl -XPUT 'localhost:9200/_river/kollektions/_meta' -d '{
    "type" : "couchdb",
    "couchdb" : {
        "host" : "localhost",
        "port" : 5984,
        "db" : "kollektions",
        "filter" : null
    },
    "index" : {
        "index" : "kollektions",
        "type" : "dummy",
        "bulk_size" : "100",
        "bulk_timeout" : "10ms"
    }
}'
