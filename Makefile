BOOTSTRAP_URL=http://downloads.buildout.org/2/bootstrap.py
OLD_SETUPTOOLS=$(shell python -c "from distutils.version import LooseVersion; import setuptools; print LooseVersion(setuptools.__version__) < LooseVersion('0.7.0')")

.PHONY: default clean very-clean

# Runs buildout
default: bin/buildout
	python bin/buildout

# Runs bootstrap
bin/buildout: bootstrap.py
	mkdir -p var/
ifeq ($(OLD_SETUPTOOLS),True)
	@echo "Found old setuptools. Using bootstrap 2.1.1"
	python bootstrap.py -v 2.1.1
else
	@echo "Found new setuptools. Using bootstrap 2.2.1"
	python bootstrap.py -v 2.2.1
endif

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
	python bin/buildout install simple-django var-directory
	python bin/nosey

clean:
	find ./ -name *.pyc -delete
	find ./ -name *.~ -delete

very-clean: clean
	@# This may vary depending where buildout sticks stuff.
	rm -f bootstrap.py
	rm -rf bin/
	rm -rf var/
