#!/usr/bin/env bash
# start ES in foreground; run this script from the project's root dir
elasticsearch -f -Xmx2g -Xms2g -D es.config=config/elasticsearch.yml