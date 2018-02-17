.PHONY: install test apidoc

ifeq ($(strip $(VIRTUAL_ENV)),)
$(error 'Virtual Env not activated')
endif

install:
	pip install -r requirements.txt

apidoc:
	sphinx-apidoc -o ./docs . ./setup.py

test:
	nosetests --with-coverage --cover-tests --cover-html --cover-erase --cover-package=tgdbapi
