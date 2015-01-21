.PHONY: all test coverage coveralls flake8 dist clean

all:	flake8 test coverage

test:
	py.test -v -s

coverage:
	coverage run --source application -m py.test && coverage report

coveralls:
	py.test --cov application tests/ --cov-report=term --cov-report=html

flake8:
	flake8 application tests

dist:
	python3 setup.py sdist upload

init:
	pip3 install -r requirements.txt
	pip3 install -r requirements_test.txt

clean:
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
	-rm -rf dist
	-rm -rf build
	-rm -rf tiddlyweb.egg-info
