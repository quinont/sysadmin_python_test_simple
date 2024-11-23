install:
	pip3 install -r src/requirements.txt

test:
	PYTHONPATH=./src python3 -m pytest tests/ -v
	PYTHONPATH=./src python3 -m pytest tests/ --cov . --cov-fail-under 80

