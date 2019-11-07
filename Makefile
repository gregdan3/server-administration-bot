install:
	pipenv install

develop:
	pipenv install --dev
	pipenv shell

test: 
	pipenv install --dev
	pipenv run python -m pytest
