BOOTSTRAP_URL=http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

.PHONY: default project clean very-clean

default: bin/buildout
	python bin/buildout

bin/buildout: bootstrap.py
	mkdir -p var/
	python bootstrap.py

bootstrap.py:
	wget $(BOOTSTRAP_URL)

db:
	rm -f var/db/*.db
	python bin/django syncdb --noinput
	python bin/django loaddata src/competition/fixtures/*.yaml

clean:
	find ./ -name *.pyc -delete
	find ./ -name *.~ -delete

very-clean: clean
	@# This may vary depending where buildout sticks stuff.
	rm -f bootstrap.py
	rm -rf bin/
	rm -rf var/
