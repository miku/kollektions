INSTALL
=======

Clone the repo
--------------

    git clone git@github.com:miku/kollektions.git
    cd kollektions


Create a virtual environment
----------------------------

    mkvirtualenv --no-site-packages kollektions


Install all required packages at once
-------------------------------------

    pip install -r requirements.txt


Create the SQL database
-----------------------

    python runserver.py --create-db


Install the CouchDB and Elasticsearch
-------------------------------------

On MAC OS X with homebrew this is just:

	brew install elasticsearch couchdb

On Linux elasticsearch is bit more painfull, as [this gist](https://gist.github.com/1190526)
shows - but it works.

CouchDB is easier on Linux:

	apt-get install couchdb

apt-get installation automatically starts CouchDB.

To start elasticsearch, use the provided

	sh runes.sh

script, which uses the shipped configuration and runs ES in foreground.


Install the CouchDB-Elasticsearch bridge
----------------------------------------

See also: https://github.com/elasticsearch/elasticsearch-river-couchdb

It's main just running one command (*plugin* comes with ES):

	bin/plugin -install elasticsearch/elasticsearch-river-couchdb/1.1.0


Register the River (Bridge between CouchDB and ElasticSearch)
-------------------------------------------------------------

To enable the river, run

	sh river-setup.sh

and to stop it:

	sh river-delete.sh

Default ports (5984 for CouchDB and 9200 for Elasticsearch are assumed!)


Verify
------

You can verify the running Couch and ES with curl:

	# CouchDB
	curl http://localhost:5984/

	# Elasticsearch
	curl http://localhost:9200/_status


Start the development server
----------------------------

    python runserver.py


Go to [http://localhost:5000](http://localhost:5000) and signup for an account.

