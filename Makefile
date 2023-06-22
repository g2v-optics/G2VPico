
.PHONY: \
	test_all \
	clean

clean:
	rm -Rf ./__pycache__

test: all

all:
	python -m unittest discover -s test -p 'test_*.py'

verbose:
	python -m unittest discover -s test -p 'test_*.py' -v
