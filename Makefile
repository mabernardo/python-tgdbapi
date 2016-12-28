.PHONY: create clean install test

create:
	python3 -m venv .venv

clean:
	rm -rf .venv

ifneq ($(strip $(VIRTUAL_ENV)),)

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	nosetests --with-coverage --cover-tests --cover-html --cover-erase --cover-package=tgdbapi

else

install: ;@echo 'Virtual Env not activated'

test: install

endif
