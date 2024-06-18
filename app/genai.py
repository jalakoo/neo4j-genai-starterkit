from neo4j import GraphDatabase
from neo4j_genai import VectorRetriever
from langchain_openai import OpenAIEmbeddings
import os
import logging
from neo4j_genai import exceptions
from neo4j_genai.indexes import create_vector_index


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INDEX_NAME = "vector"


def get_neo4j_response(query: str):

    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        embedder = OpenAIEmbeddings(model="text-embedding-3-large")

        create_vector_index(
            driver,
            INDEX_NAME,
            label="Movie",
            property="plot",
            dimensions=1536,
            similarity_fn="euclidean",
        )

        retriever = VectorRetriever(driver, INDEX_NAME, embedder)
        response = retriever.search(query_text=query, top_k=5)
    # except exceptions.RetrieverInitializationError:
    #     # Vector index likely does not exist
    except Exception as e:
        logging.ERROR(f"Caught Error: {e}")
        # TODO:
        # Create vector index

    return response


def get_weaviate_response(query: str):
    pass


def get_pinecone_response(query: str):
    pass
