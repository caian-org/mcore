init:
	pip3 install pipenv --upgrade

dep: init
	pipenv install

dev: init
	pipenv install --dev

env:
	export TEST_ENVIRON=1 && export FLASK_APP=main.py && pipenv shell

run:
	cd ./src && python3 main.py

docs:
	cd ./docs && make html

test:
	cd ./src && bash build.sh && python3 tests/tests.py -v
