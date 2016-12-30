.PHONY: install test

ifeq ($(strip $(VIRTUAL_ENV)),)
$(error 'Virtual Env not activated')
endif

install:
	pip install -r requirements.txt

test:
	nosetests --with-coverage --cover-tests --cover-html --cover-erase --cover-package=tgdbapi
