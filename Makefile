.PHONY: setup-db setup-test-db run pipeline test

setup-db:
	bash sql/setup_db.sh

setup-test-db:
	bash sql/setup_test_db.sh

run:
	python main.py

pipeline: setup-db
	python main.py

test: setup-test-db
	python -m pytest -q