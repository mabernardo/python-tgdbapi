init:
	pip3 install -r requirements.txt

test:
	nosetests --with-coverage --cover-tests --cover-erase --cover-package=tgdbapi 
