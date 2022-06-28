black:
	poetry run black ppds/**/*.py 

isort:
	poetry run isort --profile black ppds/**/*.py 

autoflake:
	poetry run autoflake --exclude=.venv/* ppds/**/*.py 

.PHONY: format
format:
	make black
	make isort
	make autoflake

.PHONY: app
app:
	poetry run streamlit run app/app.py