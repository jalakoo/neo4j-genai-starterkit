# Neo4j GenAI Starter Kit

This kit provides a simple [FastAPI](https://fastapi.tiangolo.com/) backend service connected to a [Neo4j](https://neo4j.com/) database using the [Neo4j GenAI Python Package](https://github.com/neo4j/neo4j-genai-python).

## Requirements

- [Poetry](https://python-poetry.org/) for virtual enviroment management

## Usage

```
poetry install

poetry run uvicorn app.server:app --reload --port=8000
```

or

```
pipenv shell
pipenv install
pipenv run uvicorn app.server:app --reload --port=8000
```
