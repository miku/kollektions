README.de
=========

Einsendung für http://www.coding-contest.de/ 05/2012.

Arbeitstitel: kollektions.

Live-Demo
---------

Eine Live-Demo steht (eventuell) unter

	http://139.18.19.118:5000/

zur Verfügung.


Installation
------------

siehe INSTALL.md


Konzept
-------

Da viele Features noch ausstehen sei hier nur das Konzept kurz erklärt.

Mit kollektions kann man Bücherlisten anlegen. Man kann Leuten "folgen",
wie auf Twitter und sehen, welche Bücher diese in ihrer Sammplung haben.

Noch nicht implementiert sind
.............................

* Löschen eines Buches über Webinterface (über API ist es möglich)
* Taggen von Büchern
* Kommentare zu Büchern
* seitenweite Suche


Implementiert sind
..................


* API (add, list, delete). Mit der API können Bücher per ISBN hinzugefügt
  werden. Man übergibt den Parameter 'key=...' den Webservice-Key
  (der im Profil zu finden ist) und die 'isbn=...' (ISBN-10 oder ISBN-13).

  Wird das Buch via Open Library gefunden, werden die Metadaten des Buches
  von Open Library abgefragt (http://openlibrary.org/api/books ...) und
  lokal in CouchDB als dem jeweiligen Nutzer zugeordnetes Dokument
  gespeichert. 

  Hinzufügen eines Buches:

	curl -XPUT http://localhost:5000/api/v1/books -d \
		'key=ede6d17e-12ba-4516-8b51-768058773db4&isbn=0486653552'

  Auflistung der eigenen Bücher:

	curl -XGET 'http://localhost:5000/api/v1/books?key=ede6d17e-12ba-4516-8b51-768058773db4'

  Löschen eines Buches (über die system-interne, von CouchDB vergeben ID):

	curl -XDELETE http://localhost:5000/api/v1/books -d \
		'key=ede6d17e-12ba-4516-8b51-768058773db4&id=200a8cfe4f3b3820b07a6dbc1c00950b'  


* Hinzufügen eine Buches im Web-Interface über Eingabe einer ISBN.

  Da nur Open Library nach Metadaten abgefragt wird, sind viele Titel
  leider noch nicht automatisch verfügbar.  


* Eine (wenn auch magere) Detailansicht eines Buches. Ein Coverphoto wird
  angezeigt, falls vorhanden.


* Ein Newsfeed, der die aktuellen Ereignisse anzeigt.


* Eine Follow/Unfollow Funktion für andere Mitglieder.
  Ereignisse von Usern, denen man folgt, werden im eigenen Newsfeed angezeigt.

  Im Moment muß man den anderen Nutzer per URL aufrufen um den Follow-Button
  zu finden.

  Also falls ich die user id 1 habe, und jemand, der mich interessiert die id 2,
  so muß ich per Hand auf

  	  http://localhost:5000/users/2

  gehen, um den Follow-Button zu sehen.


* Fluid-Layout down to mobile (via twitter bootstrap 2.0)


Technisch
---------

Python/Flask/SQLAlchemy-Stack mit CouchDB und ElasticSearch für die Buch-Metadaten.

Das RDBMS speichert die Nutzerdaten, den "Social Graph" und den Newsfeed. 
Die NO-SQL Seite speichert die Metadaten für die Bücher. CouchDB und Elasticsearch
haben flexible Schemen und skalieren. Auch wenn das für den Stand der Implementierung
an diesem Sonntag Overkill ist, so ist es für weitere Entwicklungen sinnvoll.

----

Hope you like it :)
