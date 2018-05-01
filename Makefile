init:
	pip3 install pipenv --upgrade

docs:
	cd ./docs && make html

dep: init
	pipenv install

dev: init
	pipenv install --dev

test:
	cd ./src && bash rebuild.sh && python3 tests/test_models.py -v
