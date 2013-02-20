BOOTSTRAP_URL=http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

.PHONY: default clean very-clean

# Runs buildout
default: bin/buildout
	python bin/buildout

# Runs bootstrap
bin/buildout: bootstrap.py
	mkdir -p var/
	python bootstrap.py

# Gets bootstrap
bootstrap.py:
	wget $(BOOTSTRAP_URL)

# Destroys existing test database and creates a new one
db:
	rm -f var/db/*.db
	python bin/django syncdb --noinput
	python bin/django migrate
	python bin/django loaddata src/competition/fixtures/*.yaml

test: bin/buildout
	python bin/buildout install simple-django
	python bin/nosey

clean:
	find ./ -name *.pyc -delete
	find ./ -name *.~ -delete

very-clean: clean
	@# This may vary depending where buildout sticks stuff.
	rm -f bootstrap.py
	rm -rf bin/
	rm -rf var/
