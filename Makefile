.PHONY: setup-db setup-test-db run pipeline test

setup-db:
	bash sql/setup_db.sh

setup-test-db:
	bash sql/setup_test_db.sh

run:
	python main.py

pipeline: setup-db run

test: setup-test-db
	pytest -q