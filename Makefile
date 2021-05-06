lint:
	black .
	flake8 src/.
	echo "Code formatted successfully!"