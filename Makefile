init:
	pip3 install pipenv --upgrade

dep: init
	pipenv install

dev: init
	pipenv install --dev

env:
	export TEST_ENVIRON=1 && pipenv shell

run:
	cd ./src && ./main.py

docs:
	cd ./docs && make html

test:
	cd ./src && ./build.py && ./tests/tests.py -v
