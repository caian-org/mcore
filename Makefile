init:
	pip3 install pipenv --upgrade

docs:
	cd ./docs && make html

dep: init
	pipenv install

dev: init
	pipenv install --dev

tests:
	cd ./src/tests && python3 start.py
