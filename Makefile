
## jinja_tornado Makefile

default: build

clean:
	rm -rf ./jinja_tornado*.egg-info
	rm -rf ./build/
	rm -rf ./dist/

install-build-requirements:
	@#pip install -r ./requirements-dev.txt
	pip install wheel twine

build: clean
	python setup.py check -r -s
	python setup.py build

dist: build
	python setup.py sdist bdist_wheel

register:
	python setup.py register

release:
	@# $(MAKE) register
	twine upload dist/*

build-release: dist release
