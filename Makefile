init:
	pip3 install pipenv --upgrade

dep: init
	pipenv install

dev: init
	pipenv install --dev

docs:
	cd ./docs && make html

test:
	cd ./src && bash build.sh && python3 tests/test_models.py -v
