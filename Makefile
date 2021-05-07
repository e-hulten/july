lint:
	black .
	flake8 src/.
	mypy src/.