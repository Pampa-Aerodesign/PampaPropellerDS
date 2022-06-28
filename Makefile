black:
	poetry run black app/*.py

isort:
	poetry run isort --profile black app/*.py

autoflake:
	poetry run autoflake --exclude=app.py,performance.py app/*.py 

.PHONY: format
format:
	make black
	make isort
	make autoflake

.PHONY: app
app:
	poetry run streamlit run app/app.py